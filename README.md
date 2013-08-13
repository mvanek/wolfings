# API Specification:

## /api/location
### Methods
- GET:
    - Access: all
    - Action: Returns business ID's close to the location
- PUT:
    - Access: root
    - Action: Undefined
- POST:
    - Access: owner
    - Action: Undefined
- DELETE:
    - Access: root
    - Action: Undefined

### Parameters
- zip: A US zipcode
- lat: Lattitude, -90 < lat < +90. Must also use lon.
- lon: Longitude, -90 < lon < +90. Must also use lat.


## /api/business/[business id]
### Methods
- GET:
    - Access: all
    - Action: Returns business model
- PUT:
    - Access: root
    - Action: Creates new business model
- POST:
    - Access: owner
    - Action: Updates business model
- DELETE:
    - Access: root
    - Action: Deletes model

### Parameters
None.
