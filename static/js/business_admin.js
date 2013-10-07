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

function lookup_user() {
    var form;

    form = document.forms['user'];
    jQuery.ajax({
        type: 'GET',
        url: '/api/user/',
        data: {
            name: form['name'].value,
            address: form['address'].value,
            city: form['city'].value,
            zip: form['zip'].value,
            phone: form['phone'].value
        }
    }).done(function( res ) {
        var user_ids,
            i;

        user_ids = res.split('\n');
        for ( i = 0; i < user_ids.length; i++ ) {
            if ( !user_ids[i] ) {
                continue;
            }

            jQuery.ajax({
                type: 'GET',
                url: '/api/user/' + user_ids[i]
            }).done(function( res ) {
                post_user( JSON.parse( res ) );
            });
        }
    })
}

function post_user( user ) {
    var dest,
        e,
        get_coupons;
    get_coupons = document.createElement('button');
    get_coupons.innerHTML = user.name;
    get_coupons.addEventListener('click', function() {
        jQuery.ajax({
            type: 'GET',
            url: '/api/user/' + user.id + '/coupons/',
            data: {
                business: window.location.pathname.split('/')[2]
            }
        }).done(function( res ) {
            var c = document.createElement('div');
            c.innerHTML = res;
            e.appendChild( c );
        });
    }, false);
    e = document.createElement('div');
    e.appendChild( get_coupons );
    dest = document.getElementById('user_list');
    dest.appendChild(e);
}
