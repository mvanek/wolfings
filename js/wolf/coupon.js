goog.require('goog.dom');
goog.require('goog.dom.classlist');
goog.require('goog.events');
goog.require('goog.net.XhrIo');
goog.require('goog.string');
goog.require('goog.date');
goog.require('goog.date.DateTime');
goog.require('goog.date.Interval');
goog.require('wolf.get');

goog.provide('wolf.coupon');
goog.provide('wolf.coupon.Coupon');
goog.provide('wolf.coupon.Timer');

wolf.coupon.Timer = function( node ) {
    var delta,
        interval;
    if ( !node ) return undefined;
    this.node = node;
    goog.Timer.call( this, 1000 );
    delta = goog.dom.getTextContent( this.node ).split(':');
    this.h = +delta[0];
    this.m = +delta[1];
    this.s = +delta[2];
    interval = new goog.date.Interval( 0, 0, 0, this.h, this.m, this.s );
    this.target = new goog.date.DateTime();
    this.target.add( interval );
};
goog.inherits(wolf.coupon.Timer, goog.Timer);

wolf.coupon.Timer.prototype.dispatchTick = function() {
    this.updateTimeleft();
    goog.dom.setTextContent( this.node, this.toString() );
    if ( !this.h && !this.m && !this.s ) {
        this.dispose();
    }
};

wolf.coupon.Timer.prototype.updateTimeleft = function() {
    var clone,
        dt,
        interval;
    clone = this.target.clone();
    dt = new goog.date.DateTime();
    interval = new goog.date.Interval( dt.getUTCFullYear(), dt.getUTCMonth(), dt.getUTCDate(), dt.getUTCHours(), dt.getUTCMinutes(), dt.getUTCSeconds() );
    clone.add( interval.getInverse() );
    this.h = clone.getUTCHours();
    this.m = clone.getUTCMinutes();
    this.s = clone.getUTCSeconds();
};

wolf.coupon.Timer.prototype.toString = function() {
    return this.h+':'+this.m+':'+this.s;
};


wolf.coupon.Coupon = function( node ) {
    var timeleft;
    if ( !node ) return undefined;
    this.node = node;
    this.couponId = this.node.id.slice(1);
    timeleft = goog.dom.getElementByClass( 'tval', this.node );
    if ( timeleft ) {
        this.timer = new wolf.coupon.Timer( timeleft );
    }
    this.buttons = goog.dom.getElementsByTagNameAndClass( 'button', null, this.node );
};

wolf.coupon.Coupon.prototype.init = function() {
    var method,
        i;
    for ( i=0; i<this.buttons.length; i++) {
        if ( goog.dom.classlist.contains(this.buttons[i], 'claim') ) {
            this.button = this.buttons[i];
            method = this.claim;
        } else if ( goog.dom.classlist.contains(this.buttons[i], 'trash') ) {
            method = this.trash;
        } else if ( goog.dom.classlist.contains(this.buttons[i], 'edit') ) {
            method = this.edit;
        } else {
            continue;
        }
        goog.events.listen(
            this.buttons[i],
            goog.events.EventType.CLICK,
            method,
            true,
            this
        );
    }
    if ( this.timer ) {
        this.timer.start();
    }
};

wolf.coupon.Coupon.prototype.url = function() {
    return '/coupon/'+this.couponId;
};

wolf.coupon.Coupon.prototype.claim = function() {
    var url,
        userId,
        button;

    button = this.button;
    userId = wolf.get('user');
    url = '/api/user/'+userId+'/coupons/';
    goog.net.XhrIo.send( url, function( e ) {
        if ( e.target.isSuccess() && button ) {
            button.innerHTML = 'CLAIMED';
            button.className = 'inactive';
        }
    }, 'POST', 'coupon='+goog.string.urlEncode(this.couponId));
};

wolf.coupon.Coupon.prototype.trash = function() {
    var url,
        userId,
        el;

    el = this.node;
    userId = wolf.get('user');
    url = '/api/user/'+userId+'/coupons/'+this.couponId;
    goog.net.XhrIo.send( url, function( e ) {
        if ( e.target.isSuccess() ) {
            goog.dom.removeNode( el );
        }
    }, 'DELETE');
};

wolf.coupon.Coupon.prototype.edit = function() {
    window.location.href = '/coupon/'+this.couponId+'/edit/';
};
