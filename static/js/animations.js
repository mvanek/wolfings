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

    _slide = function( e ) {
        /* Run animation */
        e.style.animationName = '';         /* Unbind already-run animation */
        e.offsetWidth = e.offsetWidth;      /* Trigger reflow */
        e.style.animationName = 'slide';    /* Rebind */
        e.style.maxHeight = '0px';
        e.style.overflow = 'hidden';
        return true;
    }

    toInt = function( val, def ) {
        return _numconv( parseInt, val, def );
    }
    toFloat = function( val, def ) {
        return _numconv( parseFloat, val, def );
    }
    slideDown = function( e ) {
        return _slide( e );
    }
    slideUp = function( e ) {
        return _slide( e );
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
    delete_stylesheet(2);
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