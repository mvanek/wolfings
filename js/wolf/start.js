
goog.provide('wolf.start');

goog.require('goog.locale.timeZoneDetection');
goog.require('wolf.set');
goog.require('wolf.Status');
goog.require('wolf.coupon.Coupon');
goog.require('goog.dom');
goog.require('goog.ui.registry');
wolf.start = function( uid ) {
    var status;

    wolf.set( 'user', uid );

    status = new wolf.Status( goog.dom.getElement('statusContainer') );
    status.init();

    goog.ui.registry.reset();
    goog.ui.registry.setDecoratorByClassName('goog-time-picker', function() {
        return new wolf.ui.DateTimePicker();
    });
};


goog.provide('wolf.setup_coupons');

goog.require('goog.dom.query');
wolf.setup_coupons = function() {
    var couponNodes,
        coupon,
        i;

    couponNodes = goog.dom.query('.coupon');
    for ( i=0; i<couponNodes.length; i++ )
    {
        coupon = new wolf.coupon.Coupon( couponNodes[i] );
        coupon.init();
    }
};


goog.provide('wolf.setup_coupon_edit');

goog.require('goog.ui.DatePicker');
goog.require('goog.dom.forms');
goog.require('wolf.ui.DateTimePicker');
wolf.setup_coupon_edit = function() {
    var DateTimePickers,
        dateTimeInput,
        dateTimeInputName,
        controller,
        defaultDateTime,
        i;

    // Set up DateTimePickers
    DateTimePickers = goog.dom.getElementsByClass('goog-time-picker');
    for ( i=0; i<DateTimePickers.length; i++ )
    {
        dateTimeInputName = DateTimePickers[i].id.substring( 0, DateTimePickers[i].id.length - 6 );
        dateTimeInput = goog.dom.query( 'input[name=' + dateTimeInputName + ']' )[0];
        defaultDateTime = new Date( dateTimeInput.value );
        controller = new wolf.ui.DateTimePicker( new goog.date.DateTime(
            defaultDateTime.getFullYear(), defaultDateTime.getMonth(), defaultDateTime.getDate(),
            defaultDateTime.getHours(), defaultDateTime.getMinutes()
        ));
        (function( controller, dateTimeInput ) {
            controller.listen( wolf.ui.DateTimePicker.Events.CHANGE, function( e ) {
                var utcIsoString;

                utcIsoString = controller.getDateTime().toUTCIsoString( true, true );
                // Replace the space with a T to make the string ISO 8601-compliant
                utcIsoString = utcIsoString.substr(0, 10) + 'T' + utcIsoString.substr(11);
                goog.dom.forms.setValue( dateTimeInput, utcIsoString );
            });
        })( controller, dateTimeInput );
        controller.decorate( DateTimePickers[i] );
    }
    wolf.ui.DateTimePicker.prototype.renderDateTime_ = function() {
};



};

goog.exportSymbol('wolf.start');
goog.exportSymbol('wolf.setup_coupons');
goog.exportSymbol('wolf.setup_coupon_edit');
