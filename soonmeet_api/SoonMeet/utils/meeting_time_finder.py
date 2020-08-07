from datetime import datetime, timezone, timedelta

MINUTES_IN_DAY = 1440


class MeetingTimeFinder:
    """ Module responsible for finding proposed meeting start and an end. Contains utils related to Calendar Events. """

    def __init__(self, start_datetime=datetime.now(timezone.utc)):
        """
        Initializes object.
        :param start_datetime: datetime to start seeking from
        """
        self.current_datetime = start_datetime
        self.current_date = start_datetime.date()

    def cut_time_before_today_midnight(self, event_list):
        """
        If events started before self.current_date start date will be changed to self.current_date at midnight.
        :param event_list: list of tuples (start_time, end_time)
        :return: list of tuples (start_time, end_time)
        """
        cut_event_list = []

        for start, end in event_list:
            if start.date() < self.current_date:
                start = start.replace(
                    year=self.current_date.year,
                    month=self.current_date.month,
                    day=self.current_date.day,
                    hour=0,
                    minute=0,
                    microsecond=0)
            cut_event_list.append((start, end))
        return cut_event_list

    @staticmethod
    def split_events_to_days(event_list):
        """
        If event takes place in more than one day, function will split it to 1-day events.
        :param event_list: list of tuples (start_time, end_time)
        :return: list of tuples (start_time, end_time)
        """
        split_events = []

        for start, end in event_list:
            if start.date() == end.date():
                split_events.append((start, end))
            else:
                while start.date() + timedelta(days=1) <= end.date():
                    split_events.append(
                        (start, start.replace(
                            hour=23,
                            minute=59,
                            second=59,
                            microsecond=0
                        ))
                    )
                    start += timedelta(days=1)
                    start = start.replace(
                        hour=0,
                        minute=0,
                        second=0,
                        microsecond=0
                    )
                split_events.append((start, end))

        return split_events

    @staticmethod
    def map_times_to_start_dates(events):
        """
        Puts tuples of start and end to dictionary where keys are start dates.
        :param events:
        :return:
        """
        mapped_events_to_dates = {}
        for start_time, end_time in events:
            if start_time.date() not in mapped_events_to_dates.keys():
                mapped_events_to_dates[start_time.date()] = []
            mapped_events_to_dates[start_time.date()].append((start_time, end_time))

        return mapped_events_to_dates

    @staticmethod
    def __minutes_from_midnight(time: datetime):
        return time.hour * 60 + time.minute

    def find(self, future_events: list, meeting_minutes_length: int, minutes_from_now: int = 30,
             max_days_to_meet: int = 30):
        """
        Propose meeting time for event.
        :param future_events: tuple[datetime, datetime]: events that will end in future
        :param meeting_minutes_length: length of meeting in minutes
        :param minutes_from_now: not sooner that specified minutes from now
        :param max_days_to_meet: max days after today to top looking
        :return: tuple[datetime, datetime]: event start and event date

        Algorithm based on operation on sets. For reference check thesis.
        Code should be more simplified.
        """
        meeting_time_found = False

        events = self.cut_time_before_today_midnight(future_events)
        events = self.split_events_to_days(events)
        mapped_events = self.map_times_to_start_dates(events)
        checked_day = self.current_date
        left_minutes_from_now = set()
        while not meeting_time_found:
            free_minutes = {i for i in range(MINUTES_IN_DAY)}

            if checked_day == self.current_date:  # subtract passed time today
                today_range = self.current_datetime.hour * 60 + self.current_datetime.minute + minutes_from_now
                if today_range > MINUTES_IN_DAY:
                    left_minutes_from_now = {i for i in range(today_range - MINUTES_IN_DAY)}
                    today_range = MINUTES_IN_DAY

                free_minutes -= {i for i in range(today_range)}

            if checked_day == self.current_date + timedelta(days=1) and left_minutes_from_now:
                free_minutes -= left_minutes_from_now

            if checked_day in mapped_events.keys():  # subtract minutes derived from events
                for start, end in mapped_events[checked_day]:
                    free_minutes -= {
                        i for i in range(self.__minutes_from_midnight(start),
                                         self.__minutes_from_midnight(end) if end.second == 0
                                         else self.__minutes_from_midnight(end) + 1
                                         )
                    }

            if not free_minutes:
                checked_day += timedelta(days=1)
                continue

            for minute in sorted(free_minutes):
                check_range = minute + meeting_minutes_length
                meeting_datetime_next_day = None

                if check_range > MINUTES_IN_DAY:
                    meeting_minutes_length_next_day = check_range - MINUTES_IN_DAY
                    check_range = meeting_minutes_length_next_day
                    next_day = checked_day + timedelta(days=1)

                    free_minutes_next_day = {i for i in range(meeting_minutes_length_next_day)}
                    if next_day in mapped_events.keys():
                        for start, end in mapped_events[next_day]:
                            free_minutes_next_day -= {
                                i for i in range(self.__minutes_from_midnight(start),
                                                 self.__minutes_from_midnight(end)
                                                 )
                            }

                    if free_minutes_next_day >= {i for i in range(meeting_minutes_length_next_day)}:
                        next_day_hour = meeting_minutes_length_next_day // 60
                        next_day_minute = meeting_minutes_length_next_day - (next_day_hour * 60)

                        meeting_datetime_next_day = datetime(next_day.year, next_day.month, next_day.day,
                                                             next_day_hour % 24, next_day_minute
                                                             )

                        if next_day_hour == 24:
                            meeting_minutes_length_next_day += timedelta(days=1)

                    else:
                        continue  # no sense to check because no place for tomorrow

                if free_minutes >= {i for i in range(minute, check_range)}:  # issuperset
                    start_hour = minute // 60
                    start_minute = minute - (start_hour * 60)
                    end_hour = check_range // 60
                    end_minute = check_range - (end_hour * 60)

                    checked_day_start = checked_day
                    if start_hour == 24:
                        checked_day_start += timedelta(days=1)
                        start_hour = 0

                    start_datetime = datetime(checked_day_start.year, checked_day_start.month, checked_day_start.day,
                                              start_hour % 24, start_minute
                                              )

                    if meeting_datetime_next_day:
                        end_datetime = meeting_datetime_next_day
                    else:
                        checked_day_end = checked_day
                        if end_hour == 24:
                            checked_day_end += timedelta(days=1)
                            end_hour = 0

                        end_datetime = datetime(checked_day_end.year, checked_day_end.month, checked_day_end.day,
                                                end_hour % 24, end_minute
                                                )

                    return start_datetime, end_datetime

            checked_day += timedelta(days=1)
            if checked_day >= self.current_date + timedelta(days=max_days_to_meet):
                return f'No time found. Meeting would take place later than {max_days_to_meet} days.'
