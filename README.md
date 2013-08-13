# API Specification:

## /api/location
### Methods
- GET:      all     Returns business ID's close to the location
- PUT:      root    Undefined
- POST:     owner   Undefined
- DELETE:   root    Undefined

### Parameters
- zip: A US zipcode
- lat: Lattitude, -90 < lat < +90. Must also use lon.
- lon: Longitude, -90 < lon < +90. Must also use lat.


## /api/business/[business id]
### Methods
- GET:      all     Returns business model
- PUT:      root    Creates new business model
- POST:     owner   Updates business model
- DELETE:   root    Deletes model

### Parameters
None.
