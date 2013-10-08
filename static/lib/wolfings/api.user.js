WOLFINGS.self_import( 'api', {
    user: {
        claim_coupon: function( user_id, coupon_id, callback ) {
            jQuery.ajax({
                type: 'POST',
                url: '/api/user/'+user_id+'/coupons/',
                data: {
                    coupon: coupon_id
                }
            }).done( callback );
        },

        trash_coupon: function( user_id, coupon_id , callback ) {
            jQuery.ajax({
                type: 'DELETE',
                url: '/api/user/'+user_id+'/coupons/'+coupon_id
            }).done( callback );
        }
    }
});
