var Wolf = function Wolf() {
    return this;
}


Wolf.prototype.get_nearby = function ( lat, lon, callback ) {
    $.ajax({
        type: 'GET',
        url: '/api/business',
        data: {
            lat: toFloat( lat ),
            lon: toFloat( lon )
        }
    }).done( callback );
}


Wolf.prototype.get_business = function ( id, callback ) {
    $.ajax({
        type: 'GET',
        url: '/api/business/' + id
    }).done( callback );
}
