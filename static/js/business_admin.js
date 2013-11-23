WOLFINGS.import('utils');

function biz_id() {
    var path = window.location.pathname.split('/');
    return WOLFINGS.utils.toInt( path[ path.length-3 ] );
}

function coup_id() {
    var path = window.location.pathname.split('/');
    return WOLFINGS.utils.toInt( path[ path.length-3 ] );
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

function delete_coupon() {
    jQuery.ajax({
        type: 'DELETE',
        url: '/api/coupon/' + coup_id(),
        processData: false
    }).done(function( res ) {
        window.location = '/';
    })
}

function put_coupon() {
    var start, end;
    start = new Date(
        document.forms['update']['start_date'].value + ' ' + 
        document.forms['update']['start_hour'].value + ':' +
        document.forms['update']['start_min'].value
    );
    end = new Date(
        document.forms['update']['end_date'].value + ' ' + 
        document.forms['update']['end_hour'].value + ':' +
        document.forms['update']['end_min'].value
    );
    jQuery.ajax({
        type: 'PUT',
        url: '/api/coupon/' + coup_id(),
        processData: false,
        contentType: 'text/json',
        data: JSON.stringify({
            name: document.forms['update']['name'].value,
            start: start,
            end: end
        })
    }).done(function( res ) {
        window.location = res.slice(4);
    })
}

function put_admins() {
    var admins, adminList;
    admins = [];
    adminList = document.forms['admins'];
    for ( i = 0; i < adminList.length; i++ ) {
        if ( adminList[i].type != 'checkbox' || !adminList[i].checked )
            continue;
        admins.push( adminList[i].name.slice(1) );
    }
    jQuery.ajax({
        type: 'PUT',
        url: '/api/business/' + biz_id(),
        processData: false,
        contentType: 'text/json',
        data: JSON.stringify({
            admins: admins
        })
    }).done(function( res ) {
        window.location = window.location;
    })
}

function post_coupon() {
    var form,
        startDateString,
        endDateString;

    form = document.forms['newcoup'];
    startDateString = form['start_date'].value + ' ' +
                      form['start_hour'].value + ':' +
                      form['start_min'].value;
    endDateString = form['end_date'].value + ' ' +
                    form['end_hour'].value + ':' +
                    form['end_min'].value;

    jQuery.ajax({
        type: 'POST',
        url: '/api/coupon/',
        processData: false,
        contentType: 'text/json',
        data: JSON.stringify({
            business: biz_id(),
            name: form['name'].value,
            description: form['description'].value,
            start: new Date( startDateString ),
            end: new Date( endDateString )
        })
    }).done(function( res ) {
        window.location = window.location;
    })
}

function lookup_admin() {
    var form,
        dest;

    form = document.forms['adminsearch'];
    dest = document.getElementById('admin_list');
    jQuery.ajax({
        type: 'GET',
        url: '/api/user/',
        data: {
            id: form['name'].value,
            name: form['name'].value,
            email: form['name'].value,
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
                post_admin( JSON.parse( res ), dest );
            });
        }
    })
}

function lookup_user() {
    var form,
        dest,
        data,
        name, address, city, zip, phone;

    form = document.forms['user'];
    dest = document.getElementById('user_list');
    name = form['name'].value;
    if ( name = form['name'].value )
        data['name'] = name
    if ( address = form['address'].value )
        data['address'] = name
    if ( city = form['city'].value )
        data['city'] = name
    if ( zip = form['zip'].value )
        data['zip'] = name
    if ( phone = form['phone'].value )
        data['phone'] = name
    jQuery.ajax({
        type: 'GET',
        url: '/api/user/',
        data: data
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
                post_user( JSON.parse( res ), dest );
            });
        }
    })
}

function post_admin( user, dest ) {
    var i,
        e,
        name, add,
        admins,
        adminList;

    admins = [];
    adminList = document.forms['admins'];
    for ( i = 0; i < adminList.length; i++ ) {
        if ( adminList[i].type != 'checkbox' )
            continue;
        admins.push( adminList[i].name.slice(1) );
    }
    if ( admins.indexOf( user.id ) < 0 )
        admins.push( user.id );
    WOLFINGS.log( admins );

    addButton = document.createElement('button');
    addButton.innerHTML = 'Add';
    addButton.addEventListener('click', function() {
        jQuery.ajax({
            type: 'PUT',
            url: '/api/business/' + biz_id(),
            processData: false,
            contentType: 'text/json',
            data: JSON.stringify({
                admins: admins
            })
        }).done(function( res ) {
            window.location = window.location;
        })
    }, false);
    name = document.createElement('span');
    name.innerHTML = user.name;
    e = document.createElement('div');
    e.appendChild( addButton );
    e.appendChild( name );
    dest.appendChild( e );
}

function post_user( user, dest ) {
    var e,
        get_coupons;
    get_coupons = document.createElement('button');
    get_coupons.innerHTML = user.name;
    get_coupons.addEventListener('click', function() {
        jQuery.ajax({
            type: 'GET',
            url: '/api/user/' + user.id + '/coupons/',
            data: {
                business: biz_id()
            }
        }).done(function( res ) {
            var c = document.createElement('div');
            c.innerHTML = res;
            e.appendChild( c );
        });
    }, false);
    e = document.createElement('div');
    e.appendChild( get_coupons );
    dest.appendChild(e);
}
