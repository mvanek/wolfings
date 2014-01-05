(function() {
    goog.provide('wolf.set');
    goog.provide('wolf.get');

    var data = {};

    wolf.set = function( key, value ) {
        data[ key ] = value;
    }
    wolf.get = function( key ) {
        return data[ key ];
    }

    goog.exportSymbol('wolf.set', wolf.set);
    goog.exportSymbol('wolf.get', wolf.get);
})();
