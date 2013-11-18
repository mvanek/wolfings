WOLFINGS.import('api.user');
WOLFINGS.self_import('handlers', {
    coupon: {
        click_claim_coupon: function( node ) {
            node.addEventListener('click', function( e ) {
                var coupon,
                    coupon_id,
                    user_id;

                coupon = node.parentNode.parentNode;
                coupon_id = coupon.id.slice(1);
                user_id = WOLFINGS.get('user_id');
                WOLFINGS.api.user.claim_coupon( user_id, coupon_id, function() {
                    node.innerHTML = 'CLAIMED';
                    node.className = 'inactive';
                });
            });
        },

        click_trash_coupon: function( node ) {
            node.addEventListener('click', function( e ) {
                var coupon,
                    coupon_id,
                    user_id;

                coupon = node.parentNode.parentNode;
                coupon_id = coupon.id.slice(1);
                user_id = WOLFINGS.get('user_id');
                WOLFINGS.api.user.trash_coupon( user_id, coupon_id, function() {
                    jQuery( coupon ).remove();
                });
            });
        },

        click_edit_coupon: function( node ) {
            node.addEventListener('click', function( e ) {
                var coupon,
                    coupon_id;

                coupon = node.parentNode.parentNode;
                coupon_id = coupon.id.slice(1);
                window.location.href = '/coupon/' + coupon_id + '/edit/';
            });
        }
    }
});
