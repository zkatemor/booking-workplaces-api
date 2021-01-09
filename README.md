# Booking Workplaces API with Basic Auth

## Technology
- Python3
- Django
- PostgreSQL
- Heroku (https://booking-workplaces.herokuapp.com/)

## How to

1. Create PostgreSQL database

2. Starting a project from IDE. Create .env file by example.
    
        virtualenv venv
        
        source venv/bin/activate
        
        pip install -r requirements.txt
        
        python manage.py makemigrations
        
        python manage.py migrate

4. Run server
        
        python manage.py runserver

## API Documentation

### Auth

Basic Auth (see .env_example for USERNAME & PASSWORD)

### Booking workplaces for a certain period of time

`POST` /api/workplaces/:id/booking

**Body (json)**

- *description* (string) is required
- *datetime_from* (string datetime ISO) is required
- *datetime_to* (string datetime ISO) is required

**Example:**
```json
{
    "description":"description1",
    "datetime_from":"2021-01-16T10:10:00Z",
    "datetime_to":"2021-01-16T11:10:00Z"
}
```

**Response**

- `422 Unprocessable Entity` 

```json
{
    "error": "description is required"
}
```

- `404 Not Found` 

```json
{
    "error": "Not found workplace"
}
```

- `403 Forbidden` 

```json
{
    "detail": "Authentication credentials were not provided."
}
```

- `201 OK` 

```json
{
    "result": {
        "description": "description1",
        "workplace": {
            "id": 1,
            "name": "test1"
        },
        "datetime_from": "2021-01-16T10:10:00Z",
        "datetime_to": "2021-01-16T11:10:00Z"
    }
}
```

### View the list of workplaces

`GET` /api/workplaces

**In Path**
- *id* (integer) is required

**Query Params**

- *datetime_from* (string datetime ISO) is not required
- *datetime_to* (string datetime ISO) is not required

**Response**

- `422 Unprocessable Entity` 

!!! if there is one query param, then the second is required !!!

```json
{
    "error": "The time period is not fully indicated."
}
```

- `403 Forbidden` 

```json
{
    "detail": "Authentication credentials were not provided."
}
```

- `20O OK` 

```json
{
    "result": [
        {
            "id": 1,
            "name": "test1"
        },
        {
            "id": 2,
            "name": "test2"
        }
    ]
}
```

### Viewing the list of reservations by workplace id

`GET` /api/workplaces/:id/booking

**In Path**
- *id* (integer) is required

**Response**

- `404 Not Found` 

```json
{
    "error": "Not found workplace"
}
```

- `403 Forbidden` 

```json
{
    "detail": "Authentication credentials were not provided."
}
```

- `20O OK` 

```json
{
    "result": [
        {
            "description": "description1",
            "workplace": {
                "id": 1,
                "name": "test1"
            },
            "datetime_from": "2021-01-11T10:10:00Z",
            "datetime_to": "2021-01-12T11:10:00Z"
        },
        {
            "description": "description2",
            "workplace": {
                "id": 1,
                "name": "test1"
            },
            "datetime_from": "2021-01-16T10:10:00Z",
            "datetime_to": "2021-01-16T11:10:00Z"
        }
    ]
}
```

### Other - CRUD for api/workplaces

`POST` /api/workplaces

`PUT` /api/workplaces

`DELETE` /api/workplaces

### A posted documentation for Postman (booking_workplaces.postman_collection.json)