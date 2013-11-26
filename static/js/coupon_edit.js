(function() {
    function pad(v,z) {
        return (new Array( z ).join('0') + v).substr(-z);
    }
    function localizeInput( name ) {
        var form,
            dtString, dateString, hourString, minString, localeString,
            locale,
            dt;
        form         = document.forms['update'];
        dateString   = form[ name + '_date' ].value.split('/');
        hourString   = form[ name + '_hour' ].value;
        minString    = form[ name + '_min' ].value;
        localeString = form[ name + '_locale' ].value.substr(-6);
        if ( dateString.length === 3 ) {
            dtString = pad( dateString[2], 4 ) + '-' +
                       pad( dateString[0], 2 ) + '-' +
                       pad( dateString[1], 2 ) + 'T' +
                       pad( hourString, 2 ) + ':' +
                       pad( minString, 2 ) + localeString;
        }
        dt = new Date( dtString );
        locale = dt.getTimezoneOffset();
        localeString = 'UTC';
        if ( locale < 0 ) {
            localeString += '+';
            locale = -locale;
        } else {
            localeString += '-';
        }
        localeString += pad( locale/60, 2 ) + ':' + pad( locale%60, 2 );
        form[ name + '_locale' ].value = localeString;
        if ( dateString.length === 3 ) {
            form[ name + '_date' ].value = ( dt.getMonth() + 1 ) + '/' + dt.getDate() + '/' + dt.getFullYear();
            form[ name + '_hour' ].value = dt.getHours();
            form[ name + '_min' ].value  = dt.getMinutes();
        }
    }

    jQuery( document ).ready(function() {
        localizeInput('start');
        localizeInput('end');
    });
})();