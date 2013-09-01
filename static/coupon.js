var CouponCollection,
    Coupon,
    temp;

temp = (function() {
    var CouponCollection,
        Coupon;

    Coupon = function( id ) {
        this.id = toInt( id );
        if ( !this.id ) {
            return undefined;
        }
        return this;
    }

    Coupon.prototype.get = function( callback ) {
        $.ajax({
            type: 'GET',
            url: '/api/coupon/' + this.id
        }).done(function( res ) {
            callback( JSON.parse( res ) );
        });
    }


    CouponCollection = function( query ) {
        this.query = query;
        return this;
    }

    CouponCollection.prototype.get = function( callback ) {
        $.ajax({
            type: 'GET',
            url: '/api/coupon',
            data: this.query
        }).done(function( res ) {
            var cids,
                coupons;

            cids = res.split('\n');
            coupons = [];
            for ( i = 0; i < coupons.length; i++ ) {
                if ( cids[i] ) {
                    coupons.push( Coupon( cids[i] ) );
                }
            }
            callback( coupons );
        });
    }

    return [CouponCollection, Coupon];
})();

CouponCollection = temp[0];
Coupon = temp[1];
