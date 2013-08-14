# API Specification:

## /api/location
### GET
- Access: all
- Parameters: Must use one of the following
    - zip
        - Required
        - Type:     int
        - Domain:   0 < zip < 1,000,000,000
        - Desc:     US ZIP code
    - lat
        - Required
        - Type:     float
        - Domain:   -90 < lat < 90
        - Desc:     Lattitude. If used, must also define lon.
    - lon
        - Required
        - Type:     float
        - Domain:   -90 < lon < 90
        - Desc:     Longitude. If used, must also define lat.
    - radius
        - Optional
        - Type:     int
        - Domain:   0 < int < inf
        - Desc:     Max distance from location that should be searched
- Return value
    - Success: Array of business objects
    - Failure: Appropriate 400 status code

### PUT
Undefined

### POST
Undefined

### DELETE
Undefined


## /api/business/[business id]
### GET
- Action: Retrieves business model
- Access level: all
- Return value
    - Success: Business object
    - Failure: Appropriate 400 status code

### PUT
- Action: Creates new business model
- Access level: root
- Parameters
    - name
        - Required
        - Type:     string
        - Domain:   All strings
        - Desc:     The display name of the business
    - owners
        - Required
        - Type:     array of strings
        - Domain:   All strings
        - Desc:     Lists the users allowed to modify the business's properties.
    - lat
        - Required
        - Type:     float
        - Domain:   -90 < lat < 90
        - Desc:     Lattitude of business. If used, must also define lon.
        - For root only
    - lon
        - Required
        - Type:     float
        - Domain:   -90 < lon < 90
        - Desc:     Longitude of business. If used, must also define lat.
        - For root only
- Return value
    - Success: Status code 200
    - Failure: Appropriate 400 status code

### POST
- Action: Updates existing business model
- Access level: owners
- Parameters
    - id
        - Optional
        - Type:     string
        - Domain:   All strings
        - Desc:     The new business ID
    - name
        - Optional
        - Type:     string
        - Domain:   All strings
        - Desc:     The display name of the business
    - owners
        - Optional
        - Type:     array of strings
        - Domain:   All strings
        - Desc:     Lists the users allowed to modify the business's properties.
    - lat
        - Optional
        - Type:     float
        - Domain:   -90 < lat < 90
        - Desc:     Lattitude of business. If used, must also define lon.
        - For root only
    - lon
        - Optional
        - Type:     float
        - Domain:   -90 < lon < 90
        - Desc:     Longitude of business. If used, must also define lat.
        - For root only
- Return value
    - Success: Status code 200
    - Failure: Appropriate 400 status code

### DELETE
- Action: Deletes existing business model
- Access level: root
- Return value
    - Success: Status code 200
    - Failure: Appropriate 400 status code
