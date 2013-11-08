function user_id() {
    var path = window.location.pathname.split('/');
    return toInt( path[ path.length-3 ] );
}

function put_user() {
    jQuery.ajax({
        type: 'PUT',
        url: '/api/user/' + user_id(),
        processData: false,
        contentType: 'text/json',
        data: JSON.stringify({
            name: document.forms['update']['name'].value
        })
    }).done(function( res ) {
        window.location = res.slice(4);
    })
}
