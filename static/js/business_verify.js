(function() {
    function pad(v,z) {
        return (new Array(z).join('0') + v).substr(-z);
    }
    function setLocale( selectNode ) {
        var localeString,
            locale,
            dt;
        dt = new Date();
        locale = dt.getTimezoneOffset();
        localeString = 'UTC';
        if ( locale < 0 ) {
            localeString += '+';
            locale = -locale;
        } else {
            localeString += '-';
        }
        localeString += pad( locale/60, 2 ) + ':' + pad( locale%60, 2 );
        selectNode.value = localeString;
    }

    jQuery( document ).ready(function() {
        setLocale( document.forms['newcoup']['start_locale'] );
        setLocale( document.forms['newcoup']['end_locale'] );
    });
})();