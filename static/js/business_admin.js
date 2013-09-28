function biz_id() {
    var path = window.location.pathname.split('/');
    return toInt( path[ path.length-3 ] );
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
    var form,
        startDateString,
        endDateString;

    form = document.forms['newcoup'];
    startDateString = form['sdate'].value + ' ' +
                      form['shour'].value + ':' +
                      form['smin'].value;
    endDateString = form['edate'].value + ' ' +
                    form['ehour'].value + ':' +
                    form['emin'].value;

    jQuery.ajax({
        type: 'POST',
        url: '/api/coupon/',
        processData: false,
        contentType: 'text/json',
        data: JSON.stringify({
            business: biz_id(),
            name: document.forms['newcoup']['name'].value,
            start: new Date( startDateString ),
            end: new Date( endDateString )
        })
    }).done(function( res ) {
        window.location = res.slice(4);
    })
}
