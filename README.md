# API Specification:


## /api/business
### GET
- Action: Retrieves a collection of business entities
- Access level: all
- Parameters
    - name: Filters results by the business name
        - Type: string
        - Domain: all strings
    - lat, lon: Filters results by proximity to location
        - Type: float
        - Domain: -90.0 < lat,lon < 90.0
- Return value: JSON array of objects containing keys 'name' and 'id'

### POST
- Action: Creates a new business entity
- Access level: root
- Parameters
    - name: Filters results by the business name
        - Type: string
        - Domain: all strings
    - lat: Latitude of the business location
        - Type: float
        - Domain: -90.0 < lat < 90.0
    - lon: Longitude of the business location 
        - Type: float
        - Domain: -90.0 < lon < 90.0
- Return value: URI of new entity


## /api/business/{id}
### GET
- Action: Retrieves business entity
- Access level: all
- Parameters
    none
- Return value: JSON object representing business entity

### PUT
- Action: Creates new business entity at specified numeric ID. There is an entity with this ID, it will be replaced.
- Access level: root
- Parameters
    - name: Filters results by the business name
        - Type: string
        - Domain: all strings
    - lat: Latitude of the business location
        - Type: float
        - Domain: -90.0 < lat < 90.0
    - lon: Longitude of the business location 
        - Type: float
        - Domain: -90.0 < lon < 90.0
- Return value: Status code '200 OK'

### DELETE
- Action: Deletes existing business model
- Access level: root
- Parameters
    none
- Return value: Status code '204 No Content'


## /api/user/[user id]
### GET
- Action: Retrieves user model
- Access level: all
- Return value
    - Success: User object
    - Failure: Appropriate 400 status code

### PUT
- Action: Creates new user model
- Access level: root
- Parameters
    - name
        - Required
        - Type:     string
        - Domain:   All strings
        - Desc:     The display name of the user
- Return value
    - Success: Status code '200 OK'
    - Failure: Appropriate 400 status code

### POST
- Action: Updates existing user model
- Access level: owner
- Parameters
    - name
        - Optional
        - Type:     string
        - Domain:   All strings
        - Desc:     The display name of the user
- Return value
    - Success: Status code '200 OK'
    - Failure: Appropriate 400 status code

### DELETE
- Action: Deletes existing user model
- Access level: root
- Return value
    - Success: Status code '200 OK'
    - Failure: Appropriate 400 status code. Deleting a nonexistent model will not raise an error.
