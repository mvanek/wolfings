WOLFINGS.self_import( 'utils', (function() {
    var _numconv,
        _slide;
    _numconv = function( fn, val, def ) {
        if ( !def ) {
            def = undefined;
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

    return {
        toInt: function( val, def ) {
            return _numconv( parseInt, val, def );
        },
        toFloat: function( val, def ) {
            return _numconv( parseFloat, val, def );
        },
        slideDown: function( e ) {
            return _slide( e, String( 0 - e.getBoundingClientRect().height ) + 'px', '0px' );
        },
        slideUp: function( e ) {
            return _slide( e, '0px', String( 0 - e.getBoundingClientRect().height ) + 'px' );
        }
    }
})());
