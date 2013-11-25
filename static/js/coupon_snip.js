WOLFINGS.import('utils', function() {
    function CountdownTimer( node ) {
        var time,
            h,m,s,
            timer;

        time = node.innerHTML.split(':');
        s = WOLFINGS.utils.toInt( time[ time.length - 1 ] );
        m = WOLFINGS.utils.toInt( time[ time.length - 2 ] );
        h = WOLFINGS.utils.toInt( time[ time.length - 3 ] );

        function tick() {
            if ( s === 0 ) {
                if ( m === 0 ) {
                    if ( h === 0 ) {
                        window.clearInterval( timer );
                    }
                    h -= 1;
                    m = 60;
                }
                m -= 1;
                s = 60;
            }
            s -= 1;

            node.innerHTML = ( '00' + h ).substr(-2) + ':' +
                             ( '00' + m ).substr(-2) + ':' +
                             ( '00' + s ).substr(-2);
        }
        timer = window.setInterval( tick, 1000 );
    }

    jQuery( document ).ready(function() {
        var tnodes, i;
        tnodes = jQuery('.tval');
        for ( i=0; i<tnodes.length; i++ ) {
            CountdownTimer( tnodes[i] );
        }
    });
});

function localize( dtnode ) {
    dt = new Date( dtnode.innerHTML );
    dtnode.innerHTML = dt.toLocaleString();
}

jQuery( document ).ready(function() {
    var dtnodes, i;
    dtnodes = jQuery('.datetime');
    for ( i=0; i<dtnodes.length; i++ ) {
        localize( dtnodes[i] );
    }
})