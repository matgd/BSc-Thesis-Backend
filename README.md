# BSc-Thesis-Backend
## Public code
Notice!

Code in this repository is only for showing my skill and level of knowledge regarding used languages and technologies. It probably won't run due to missing content.  

Keep in mind the majority of work was done from August 2019 to December 2019. There are some things that I would do differently (i.e. improve code style) or add (i.e. missing docstrings, tests) after gaining experience. 
### Praca dyplomowa.  

  
### REST API, technologie:  
 * Python 3.7
 * Django REST Framework
 * PostgreSQL 10
 * nginx
 * OpenSSL
 * AWS EC2 (Ubuntu 18.04)
 * AWS RDS (PostgreSQL 10)
 * Travis-CI
 * bash

### Struktura API
#### API ViewSets (dostępne pod /api)
```
/api/profile/
/api/profile_pagination/
/api/friend_invitation/
/api/event_type/
/api/event_date/
/api/calendar_event/
/api/meeting_invitation/
```
#### API APIViews (ukryte)
```
/api/login/
/api/friend_list/
/api/pending_friend_invites/
/api/propose_meeting/
/api/user_email_password/
```

#### Uwagi do niektórych endpointów
```
/api/pending_friend_invites/
```
Metoda PATCH może być stosowana tylko i wyłącznie dla statusu zaproszenia. Metoda PUT niedozwolona.
<hr>  
  
```
/api/event_date/
```
Możliwe jest filtrowanie daty początku lub końca dzięki dodaniu do argumentu odpowiedniego postfiksu:
* __lte
* __lt
* __gte
* __gt  
  
Dla przykładu:  
```
GET /api/event_date/?start_date__lte=2019-10-01/
```  
  
<hr>  
  
```
/api/profile_pagination/
```
Sterowanie poprzez paremetry *limit* i *offset*.

Dla przykładu:
```
GET /api/profile_pagination/?limit=5&offset=10/
```
<hr>  

```
/api/propose_meeting/
```  
Akceptuje tylko autoryzowane zapytanie POST.
Przykładowe zapytania: 
```
{
	"participants": [23,22],
	"minutes": 15
}
```  
```
{
	"participants": [23,22],
	"minutes": 15,
	"omit_event_dates": [78],
	"min_buffer_minutes": 1200
}
```  
Przykładowa odpowiedź:  
```
{
    "organizer": 20,
    "participants": [
        20,
        23,
        22
    ],
    "start_time": "2019-10-08T06:18:00",
    "end_time": "2019-10-08T06:33:00",
    "min_buffer_minutes": 1200
}
```
<hr>  

*Stan na dzień:  
 niedziela, 1 grudnia 2019*
