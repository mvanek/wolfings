goog.require('goog.dom');
goog.require('wolf.set');
goog.require('wolf.Status');
goog.provide('wolf.start');
wolf.start = function( uid ) {
    var status;

    wolf.set( 'user', uid );

    status = new wolf.Status( goog.dom.getElement('statusContainer') );
};

goog.provide('wolf.setup_coupons');
goog.require('wolf.coupon.Coupon');
goog.require('goog.dom.query');
wolf.setup_coupons = function() {
    var couponNodes,
        i;

    couponNodes = goog.dom.query('.coupon');
    for ( i=0; i<couponNodes.length; i++ )
    {
        new wolf.coupon.Coupon( couponNodes[i] );
    }
};

goog.exportSymbol('wolf.start');
goog.exportSymbol('wolf.setup_coupons');
