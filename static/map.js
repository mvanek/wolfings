var Map = function Map( container ) {
    var parent = this;

    google.maps.visualRefresh = true;
    this.settings = {
        here: new google.maps.LatLng( 35.960162, -86.802699 ),
        api_key: 'AIzaSyBO7uBiTXNj8U1aDVQR5snr4XDd3xitHRE'
    }
    this.markers = [];
    this.wolf = new Wolf();
    this.map = this.init_map( container );

    this.nearby();

    return this;
}


Map.prototype.init_map = function( container ) {
    var map, parent;

    parent = this;

    map = new google.maps.Map(container, {
        center: this.settings.here,
        zoom: 13,
        mapTypeID: google.maps.MapTypeId.ROADMAP
    });

    google.maps.event.addDomListener(map, 'center_changed', function() {
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
        w.open(this.map, this);
        google.maps.event.addDomListener(w, 'closeclick', function() {
            this.close();
        });
    }, false);
    this.markers.push( marker );
}


Map.prototype.nearby = function() {
    var here,
        wolf,
        map;

    map = this;
    wolf = this.wolf;
    here = this.map.getCenter();

    wolf.get_nearby( here.lat(), here.lng(), function( data ) {

        var res,
            m;

        while ( m = map.markers.pop() ) {
            m.setMap( null );
        }

        res = data.split('\n');
        for ( i = 0; i < res.length - 1; i++ ) {
            wolf.get_business( res[i], function( data ) {

                var res;
                res = JSON.parse( data );
                map.add_marker( res.name, res.lat, res.lon );

            });
        }

    });
}
