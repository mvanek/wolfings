goog.require('goog.dom');
goog.require('goog.fx.easing');
goog.require('goog.fx.dom');
goog.require('goog.style');
goog.require('goog.async.Delay');
goog.require('goog.events');
goog.require('goog.events.EventType');

goog.provide('wolf.Status');

wolf.Status = function( el ) {
    if ( !el ) {
        return undefined;
    }
    this.container = el;
    this.el = goog.dom.getFirstElementChild( this.container );
    this.button = goog.dom.getFirstElementChild( this.el );
    this.h = goog.style.getSize( this.container ).height;
}

wolf.Status.prototype.init = function() {
    this.expanded = true;
    goog.events.listen( this.button, goog.events.EventType.CLICK, this.slideUp, true, this );
};

wolf.Status.prototype.slideUp = function() {
    var anim;
    if ( !this.expanded ) return false;
    anim = new goog.fx.dom.ResizeHeight(
        this.container,
        this.h, 0,
        1000,
        goog.fx.easing.easeOut
    );
    anim.play();
    this.expanded = false;
}

wolf.Status.prototype.slideDown = function() {
    var anim;
    if ( this.expanded ) return false;
    anim = new goog.fx.dom.ResizeHeight(
        this.container,
        0, this.h,
        1000,
        goog.fx.easing.easeOut
    );
    anim.play();
    this.expanded = true;
}

wolf.Status.prototype.toggle = function() {
    if ( this.expanded ) {
        this.slideUp();
    } else {
        this.slideDown();
    }
}

wolf.Status.prototype.set = function( text ) {
    this.slideUp();
    goog.dom.setTextContent( this.el, text );
    this.slideDown();
}

wolf.Status.prototype.hideAfterTimeout = function( timeout ) {
    var delay, status;
    status = this;
    delay = new goog.async.Delay(function() {
        status.slideUp();
        delay.dispose();
    }, timeout);
    delay.start();
}
