function biz_id() {
    var path = window.location.pathname.split('/');
    return path[ path.length-3 ];
}

function put_business() {
    jQuery.ajax({
        type: 'PUT',
        url: '/api/business/' + biz_id(),
        processData: false,
        contentType: 'text/json',
        data: JSON.stringify({
            name: document.forms['update']['name'].value
        })
    }).done(function( res ) {
        window.location = res.slice(4);
    })
}

function post_coupon() {
    jQuery.ajax({
        type: 'POST',
        url: '/api/coupon/',
        processData: false,
        contentType: 'text/json',
        data: JSON.stringify({
            name: document.forms['newcoup']['name'].value,
            business: toInt(biz_id())
        })
    }).done(function( res ) {
        window.location = res.slice(4);
    })
}
