var WOLFINGS = (function() {
    var obj,
        namespace;

    obj = function() {}

    obj.prototype.get = function( key ) {
        return this.namespace[ key ];
    }

    obj.prototype.set = function( key, value ) {
        return this.namespace[ key ] = value;
    }

    
    obj.prototype.import = function( path, callback ) {
        var script;
        
        script = document.createElement('script');
        script.src = path;
        document.appendChild( script );
        callback();
    }


    obj.prototype.api = (function() {
        var api = function() {}

        api.prototype.user = (function() {
            var user = function() {}

            user.prototype.claim_coupon = function( user_id, coupon_id, callback ) {
                jQuery.ajax({
                    type: 'POST',
                    url: '/api/user/'+user_id+'/coupons/',
                    data: {
                        coupon: coupon_id
                    }
                }).done( callback( res ) );
            }

            user.prototype.trash_coupon = function( user_id, coupon_id , callback ) {
                jQuery.ajax({
                    type: 'DELETE',
                    url: '/api/user/'+user_id+'/coupons/'+coupon_id
                }).done( callback( res ) );
            }

            return new user();
        })();

        return new api();
    })();


    obj.prototype.handlers = (function() {
        var handlers = function() {}

        handlers.prototype.click_claim_coupon = function( e ) {
            var user_id,
                coupon_id;
            coupon = e.target.parentNode.parentNode;
            coupon_id = coupon.id.slice(1);
            user_id = WOLFINGS.get('user_id');
            WOLFINGS.api.user.claim_coupon( user_id, coupon_id, function() {
                e.target.innerHTML = 'CLAIMED';
                e.target.className = 'inactive';
            });
        }

        handlers.prototype.click_trash_coupon = function( e ) {
            var coupon,
                coupon_id,
                user_id;

            coupon = e.target.parentNode.parentNode;
            coupon_id = coupon.id.slice(1);
            user_id = WOLFINGS.get('user_id');
            WOLFINGS.api.user.trash_coupon( user_id, coupon_id, function() {
               $( coupon ).remove();
            });
        }

        return new handlers();
    })();


    return new obj();
})();
