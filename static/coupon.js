/* 
 * CouponCollection
 *  CouponCollection(filter:Object)
 *      Constructor
 *      parameters:
 *          filter: An object on which to filter searched coupons. Valid values:
 *              - business: The integer ID of the business that offers the coupon
 *  get(callback:function)
 *      Fetches the list of coupons defined in the constructor, and passes the
 *      array of coupon ID's to the callback
 *      parameters:
 *          callback(coupon:Object): Called for each coupon
 *
 * Coupon
 *  Coupon(id:string|int)
 *      Constructor
 *      parameters:
 *          id: the coupon ID
 *  get(callback:function)
 *      Fetches the coupon defined in the constructor, and passes the
 *      object representing it to the callback
 *      parameters:
 *          callback(coupon:Object): Called when the server responds
 */
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
            i;

        cids = res.split('\n');
        for ( i = 0; i < cids.length; i++ ) {
            c = new Coupon( cids[ i ] );
            c.get( callback );
        }
    });
}
