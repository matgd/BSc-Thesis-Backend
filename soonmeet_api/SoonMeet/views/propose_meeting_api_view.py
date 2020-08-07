from datetime import datetime, timezone

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.validators import ValidationError

from SoonMeet.models.calendar_event import CalendarEvent
from SoonMeet.models.event_date import EventDate
from ..utils.meeting_time_finder import MeetingTimeFinder


class ProposeMeetingApiView(APIView):
    """
    Endpoint responsible for proposing time of meetings.
    Accepts authorized POST requests.
    --- PARAMETERS ---
    participants - MANDATORY - list[int] - list of users IDs (excluding authorized user)
    minutes - MANDATORY - int - desired length of meeting in minutes
    omit_event_dates - list[int] - list of event_dates' IDs that will be excluded during search (useful for REJECTED invitations)
    min_buffer_minutes - int - proposed time cannot include next given minutes
    ---- RESPONSE ----
    organizer - ID of user initiating proposal
    participants - list of participating users (including organizer)
    start_time - proposal start of meeting
    end_time - proposal end of meeting
    min_buffer_minutes - given buffer
    """
    authentication_classes = [TokenAuthentication]
    parser_classes = [JSONParser]

    @staticmethod
    def __validate_post_request(request_data):
        if not isinstance(request_data, dict):
            raise ValidationError('JSON object containing keys of "participants" and "minutes" is required.')
        if 'participants' not in request_data.keys():
            raise ValidationError('The field "participants" is missing.')
        if 'minutes' not in request_data.keys():
            raise ValidationError('The field "minutes" is missing.')
        if not isinstance(request_data['participants'], list):
            raise ValidationError('Participants should be list of profile IDs.')
        if not request_data['participants']:
            raise ValidationError('Participant list is empty.')
        if not all(isinstance(item, int) for item in request_data['participants']):
            raise ValidationError('Participant list is not a list of integers.')
        if not isinstance(request_data['minutes'], int):
            raise ValidationError('Minutes have to be type of integer.')
        if request_data['minutes'] < 1:
            raise ValidationError('Minutes cannot be less or equal 0.')
        if request_data['minutes'] > 1439:
            raise ValidationError('Minutes cannot exceed 1439.')
        if 'omit_event_dates' in request_data.keys():
            if not isinstance(request_data['omit_event_dates'], list):
                raise ValidationError('Event dates are not list of integers (Event Dates IDs).')
            if not all(isinstance(item, int) for item in request_data['omit_event_dates']):
                raise ValidationError('Events dates are not integers!')
        if 'min_buffer_minutes' in request_data.keys():
            if not isinstance(request_data['min_buffer_minutes'], int):
                raise ValidationError('Buffer time has to be an integer.')
            if request_data['min_buffer_minutes'] < 1 or request_data['min_buffer_minutes'] > 1439:
                raise ValidationError('Buffer time can be only between 1 and 1439 included.')

    @staticmethod
    def __determine_meeting_time(now, future_events, meeting_length, buffer_time):
        events = MeetingTimeFinder(now).find(future_events,
                                             meeting_minutes_length=meeting_length,
                                             minutes_from_now=buffer_time
                                             )
        return events

    def post(self, request, format=None):
        if request.user.id is None:
            return Response({'error': 'Not authenticated'}, status.HTTP_403_FORBIDDEN)

        self.__validate_post_request(request.data)

        logged_user_event_endings = [
            (ce.event_date.start_date, ce.event_date.end_date)
            for ce in CalendarEvent.objects.filter(user=request.user.id)
            if ce.event_date.end_date > datetime.now(timezone.utc)
        ]

        friends_event_endings = []
        for participant_id in request.data['participants']:
            friends_event_endings += [
                (ce.event_date.start_date, ce.event_date.end_date)
                for ce in CalendarEvent.objects.filter(user=participant_id)
                if ce.event_date.end_date > datetime.now(timezone.utc)
            ]

        omitted_events = []
        if 'omit_event_dates' in request.data.keys():
            for ed_id in request.data['omit_event_dates']:
                event_date = EventDate.objects.get(pk=ed_id)
                if event_date.end_date > datetime.now(timezone.utc):
                    omitted_events.append((event_date.start_date, event_date.end_date))

        future_events = logged_user_event_endings + friends_event_endings + omitted_events

        min_buffer = 30
        if 'min_buffer_minutes' in request.data.keys():
            min_buffer = request.data['min_buffer_minutes']

        proposed_start, proposed_end = self.__determine_meeting_time(datetime.now(timezone.utc),
                                                                     future_events,
                                                                     request.data['minutes'],
                                                                     min_buffer
                                                                     )

        return Response({
                'organizer': request.user.id,
                'participants': [request.user.id] + request.data['participants'],
                'start_time': proposed_start,
                'end_time': proposed_end,
                'min_buffer_minutes': min_buffer
            })
