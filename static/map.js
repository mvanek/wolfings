/* 
 * Implements the Map object, which handles all map-related stuff,
 * including markers and events
 */
var Map = function Map( settings ) {
    var parent = this;

    google.maps.visualRefresh = true;
    this.settings = settings;
    this.markers = [];
    this.map = this.init_map( settings.container );

    this.nearby();

    return this;
}


/* Adds map to the DOM, and adds event listeners for the map itself */
Map.prototype.init_map = function( container ) {
    var map, parent;

    parent = this;

    map = new google.maps.Map(container, {
        center: this.settings.here,
        zoom: 13,
        mapTypeID: google.maps.MapTypeId.ROADMAP
    });

    google.maps.event.addDomListener(map, 'dragend', function() {
        parent.nearby();
    });

    return map
}


Map.prototype.add_marker = function( name, lat, lon ) {
    var marker;

    marker = new google.maps.Marker({
        map: this.map,
        position: new google.maps.LatLng( lat, lon ),
        title: name
    });
    google.maps.event.addDomListener(marker, 'click', function() {
        var w;
        w = new google.maps.InfoWindow({
            content: name
        });
        w.open( this.map, this );
        google.maps.event.addDomListener(w, 'closeclick', function() {
            this.close();
        });
    }, false);
    this.markers.push( marker );
}


Map.prototype.nearby = function() {
    var here,
        map,
        B;

    map = this;
    here = this.map.getCenter();

    B = new BusinessCollection({
        lat: toFloat(here.lat()),
        lon: toFloat(here.lng())
    });
    B.get(function( businesses ) {
        var m,
            i;

        while ( m = map.markers.pop() ) {
            m.setMap( null );
        }
        for ( i = 0; i < businesses.length; i++ ) {
            businesses[i].get(function( b ) {
                map.add_marker( b.name, b.lat, b.lon );
            });
        }
    });
}
