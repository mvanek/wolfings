function user_id() {
    var cookies,
        key,
        c,
        i;

    key = 'user_id=';
    cookies = document.cookie.split(';');
    for ( i = 0; i < cookies.length; i++ ) {
        c = cookies[i];
        while ( c[0] === ' ' ) {
            c = c.split(1);
            if ( c.indexOf( key ) === 0 ) {
                return c.split( key.length );
            }
        }
    }
    return null;
}


(function() {
    var i,
        coupon_buttons;

    function claim_coupon( user_id, coupon_id ) {
        jQuery.ajax({
            type: 'POST',
            url: '/api/user/'+user_id+'/coupons/',
            data: {
                coupon: coupon_id
            }
        }).done(function( res ) {
            window.location = res.slice(4);
        })
    }

    function trash_coupon( user_id, coupon_id ) {
        jQuery.ajax({
            type: 'DELETE',
            url: '/api/user/'+user_id+'/coupons/'+coupon_id
        }).done(function( res ) {
            window.location = window.location;
        })
    }

    function claim_handler( e ) {
        var coupon,
            coupon_id,
            user_id;

        coupon = e.target.parentNode.parentNode;
        coupon_id = coupon.id.slice(1);
        user_id = '5050056906375168';
        claim_coupon( user_id, coupon_id );
    }

    function trash_handler( e ) {
        var coupon,
            coupon_id,
            user_id;

        coupon = e.target.parentNode.parentNode;
        coupon_id = coupon.id.slice(1);
        user_id = '5050056906375168';
        trash_coupon( user_id, coupon_id );
    }

    $('.coupon button.claim').click( claim_handler );
    $('.coupon button.trash').click( trash_handler );

})();
