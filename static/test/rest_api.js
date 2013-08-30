var toFloat, toInt,
    slideUp, slideDown;
(function() {
    var _numconv,
        _slide;
    _numconv = function( fn, val, def ) {
        if ( !def ) {
            def = '';
        }
        if ( isNaN( val = fn(val) ) ) {
            return def;
        }
        return val;
    }

    _slide = function( e, from, to ) {
        var rule, old_from, old_to;
        rule = document.styleSheets[ 1 ].cssRules[ 0 ];
        old_from = rule.cssRules[ 0 ].style.marginTop;
        old_to = rule.cssRules[ 1 ].style.marginTop;
        rule.cssRules[ 0 ].style.marginTop = from;
        rule.cssRules[ 1 ].style.marginTop = to;
        if ( from == old_from ) {
            return false;
        }
        e.style.animationDuration = '200ms';
        /* Run animation */
        e.style.animationName = '';         /* Unbind already-run animation */
        e.offsetWidth = e.offsetWidth;      /* Trigger reflow */
        e.style.animationName = 'slide';    /* Rebind */
        e.style.marginTop = to;
        return true;
    }

    toInt = function( val, def ) {
        return _numconv( parseInt, val, def );
    }
    toFloat = function( val, def ) {
        return _numconv( parseFloat, val, def );
    }
    slideDown = function( e ) {
        return _slide( e, String( 0 - e.getBoundingClientRect().height ) + 'px', '0px' );
    }
    slideUp = function( e ) {
        return _slide( e, '0px', String( 0 - e.getBoundingClientRect().height ) + 'px' );
    }
})();


function delete_stylesheet( num ) {
    while ( true ) {
        try {
            document.styleSheets[ num ].deleteRule( 0 );
        } catch ( ex ) {
            break;
        }
    }
}

/* Posts data into response and animates the pulldown */
function post_res( status, data ) {
    var msg;

    document.getElementById('status').innerHTML = status;
    msg = document.getElementById('msg');
    msg.innerHTML = '';
    try {
        msg.appendChild( data );
    } catch ( ex ) {
        msg.innerHTML = data;
    }
    delete_stylesheet( 2 );
    slideDown( document.getElementById('res') );
}

/* Pulls up before posting the data */
function repost_res( status, data ) {
    var res, h;

    res = document.getElementById('res');
    if ( slideUp( res ) ) {
        res.addEventListener('animationend', h = function() {
            res.removeEventListener( 'animationend', h );
            post_res( status, data );
        }, false);
    } else {
        post_res( status, data );
    }
}


function success_res( data, textStatus, xhr ) {
    repost_res(textStatus, data);
}


function fail_res(xhr, textStatus, errorThrown) {
    var i,
        table, row, cell,
        post_msg;

    table = document.createElement('table');
    for ( i in xhr ) {
        row = document.createElement('tr');

        cell = document.createElement('td');
        cell.innerHTML = i;
        row.appendChild( cell );

        cell = document.createElement('td');
        cell.innerHTML = xhr[ i ];
        row.appendChild( cell );

        table.appendChild( row );
    }

    repost_res( textStatus, table );
}


function get_biz() {
    $.ajax({
        type: 'GET',
        url: '/api/business',
        data: {
            name: document.forms['get_biz']['name'].value,
            lat: toFloat( document.forms['get_biz']['lat'].value ),
            lon: toFloat( document.forms['get_biz']['lon'].value )
        },
    }).done( success_res ).fail( fail_res );
}


function post_biz() {
    $.ajax({
        type: 'POST',
        url: '/api/business',
        data: {
            name: document.forms['post_biz']['name'].value,
            lat: toFloat( document.forms['post_biz']['lat'].value ),
            lon: toFloat( document.forms['post_biz']['lon'].value )
        },
    }).done( success_res ).fail( fail_res );
}


function get_bizid() {
    $.ajax({
        type: 'GET',
        url: '/api/business/' + document.forms['get_bizid']['id'].value
    }).done( success_res ).fail( fail_res );
}


function put_bizid() {
    $.ajax({
        type: 'PUT',
        url: '/api/business/' + document.forms['put_bizid']['id'].value,
        processData: false,
        contentType: 'text/json',
        data: JSON.stringify({
            name: document.forms['put_bizid']['name'].value,
            lat: toFloat( document.forms['put_bizid']['lat'].value ),
            lon: toFloat( document.forms['put_bizid']['lon'].value )
        })
    }).done( success_res ).fail( fail_res );
}


function delete_bizid() {
    $.ajax({
        type: 'DELETE',
        url: '/api/business/' + document.forms['delete_bizid']['id'].value
    }).done( success_res ).fail( fail_res );
}


function get_coup() {
    $.ajax({
        type: 'GET',
        url: '/api/coupon',
        data: {
            user: parseInt(document.forms['get_coup']['user'].value),
            business: parseInt(document.forms['get_coup']['business'].value)
        }
    }).done( success_res ).fail( fail_res );
}


function post_coup() {
    $.ajax({
        type: 'POST',
        url: '/api/coupon',
        data: {
            name: document.forms['post_coup']['name'].value,
            business: parseInt(document.forms['post_coup']['business'].value)
        }
    }).done( success_res ).fail( fail_res );
}


function get_coupid() {
    $.ajax({
        type: 'GET',
        url: '/api/coupon/' + document.forms['get_coupid']['id'].value
    }).done( success_res ).fail( fail_res );
}


function put_coupid() {
    $.ajax({
        type: 'PUT',
        url: '/api/coupon/' + document.forms['put_coupid']['id'].value,
        processData: false,
        contentType: 'text/json',
        data: JSON.stringify({
            name: document.forms['put_coupid']['name'].value,
            business: parseInt(document.forms['put_coupid']['business'].value)
        })
    }).done( success_res ).fail( fail_res );
}


function delete_coupid() {
    $.ajax({
        type: 'DELETE',
        url: '/api/coupon/' + document.forms['delete_coupid']['id'].value
    }).done( success_res ).fail( fail_res );
}


function get_user() {
    $.ajax({
        type: 'GET',
        url: '/api/user'
    }).done( success_res ).fail( fail_res );
}

function post_user() {
    $.ajax({
        type: 'POST',
        url: '/api/user',
        data: {
            name: document.forms['post_user']['name'].value
        }
    }).done( success_res ).fail( fail_res );
}


function get_userid() {
    $.ajax({
        type: 'GET',
        url: '/api/user/' + document.forms['get_userid']['id'].value
    }).done( success_res ).fail( fail_res );
}


function post_userid() {
    $.ajax({
        type: 'POST',
        url: '/api/user/' + document.forms['post_userid']['id'].value,
        data: {
            coupon: parseInt(document.forms['post_userid']['coupon'].value)
        }
    }).done( success_res ).fail( fail_res );
}


function put_userid() {
    $.ajax({
        type: 'PUT',
        url: '/api/user/' + document.forms['put_userid']['id'].value,
        processData: false,
        contentType: 'text/json',
        data: JSON.stringify({
            name: document.forms['put_userid']['name'].value
        })
    }).done( success_res ).fail( fail_res );
}


function delete_userid() {
    $.ajax({
        type: 'DELETE',
        url: '/api/user/' + document.forms['delete_userid']['id'].value
    }).done( success_res ).fail( fail_res );
}


function api_init() {
    $.ajax({
        type: 'GET',
        url: '/api/init'
    }).done( success_res ).fail( fail_res );
}


function api_reinit() {
    $.ajax({
        type: 'GET',
        url: '/api/reinit'
    }).done( success_res ).fail( fail_res );
}


jQuery( document ).ready(function() {
    var e;
    document.getElementById('clear').addEventListener('click', function() {
        slideUp( document.getElementById('res') );
    }, false)
    e = document.getElementById('res');
    e.style.marginTop = String( 0 - e.getBoundingClientRect().height ) + 'px';
});
