/* Executes after page load */
(function() {
var main,
    req;

function append_template( type, c, dest ) {
    dust.render( type, c, function( err, out ) {
        if ( out ) {
            dest.innerHTML += out
        } else {
            console.log( err );
        }
    } );
}

main = document.getElementById('main');
if ( !main ) {
    console.log('Couldn\'t find container.');
    return undefined;
}

req = new BusinessCollection();
req.get(function( b ) {
    console.log( b );
    append_template( 'business', b, main );
});

/*
req = new CouponCollection();
req.get(function( c ) {
    append_template( 'coupon', c, main );
});
*/

})();
