/**
 * @fileoverview Time picker implementation.
 *
 * @author Wolfings, LLC
 */

goog.provide('wolf.ui.DateTimePicker');

goog.require('goog.dom.forms');
goog.require('goog.i18n.TimeZone');
goog.require('goog.string');
goog.require('goog.ui.Component');
goog.require('goog.ui.DatePicker');
goog.require('goog.ui.DatePickerEvent');



/**
 * DateTimePicker widget. Allows a single time to be selected from a dropdown.
 *
 * @param {goog.date.DateTime|DateTime=} opt_dateTime DateTime to initialize
 *     the time picker with, defaults to the current datetime.
 * @param {goog.dom.DomHelper=} opt_domHelper Optional DOM helper.
 * @constructor
 * @extends {goog.ui.Component}
 */
wolf.ui.DateTimePicker = function( opt_dateTime, opt_domHelper ) {
    goog.base( this, opt_domHelper );
    this.dateTime_ = opt_dateTime || new goog.date.DateTime();
};
goog.inherits( wolf.ui.DateTimePicker, goog.ui.Component );


/**
 * Constants for event names
 *
 * @type {Object}
 */
wolf.ui.DateTimePicker.Events = {
  CHANGE: 'change',
  SELECT: 'select'
};


/** @override */
wolf.ui.DateTimePicker.prototype.createDom = function() {
    goog.base( this, 'createDom' );
    this.decorateInternal( this.dom_.createElement('div') );
};


/** @override */
wolf.ui.DateTimePicker.prototype.decorateInternal = function( element ) {
    goog.base( this, 'decorateInternal', element );

    this.datePickerElement_ = this.dom_.createElement('div');
    this.userInputElement_ = this.dom_.createElement('input');

    goog.dom.setProperties( this.userInputElement_, {
        'placeholder': 'Time (HH:MM pm)'
    });

    this.datePicker_ = new goog.ui.DatePicker( this.dateTime_ );
    this.datePicker_.setShowWeekNum( false );
    this.datePicker_.setAllowNone( false );
    this.datePicker_.setShowToday( false );
    this.datePicker_.render( this.datePickerElement_ );

    this.renderTime_();

    element.appendChild( this.datePickerElement_ );
    element.appendChild( this.userInputElement_ );

    return element;
};


/** @override */
wolf.ui.DateTimePicker.prototype.enterDocument = function() {
    goog.base( this, 'enterDocument' );

    this.getHandler().listen( this.userInputElement_, goog.events.EventType.FOCUSOUT, this.onFocusOut_ );

    this.datePicker_.listen( goog.ui.DatePicker.Events.SELECT, function( e ) {
        var selectEvent;

        selectEvent = new goog.ui.DatePickerEvent(
            wolf.ui.DateTimePicker.Events.SELECT,
            this, this.dateTime_
        );
        this.dispatchEvent( selectEvent );
    }, false, this );

    this.datePicker_.listen( goog.ui.DatePicker.Events.CHANGE, function( e ) {
        var changeEvent;

        changeEvent = new goog.ui.DatePickerEvent(
            wolf.ui.DateTimePicker.Events.CHANGE,
            this, this.dateTime_
        );
        this.dispatchEvent( changeEvent );
    }, false, this );
};


wolf.ui.DateTimePicker.prototype.getDateTime = function() {
    return this.dateTime_;
};


wolf.ui.DateTimePicker.prototype.onFocusOut_ = function( e ) {
    this.updateTime_();
};


wolf.ui.DateTimePicker.prototype.parseUserInput_ = function() {
    var re, matches,
        hour,
        minute,
        period;

    // Parse user input
    re = /^(\d\d?)(?::(\d\d))?(?: ?([AaPp])[Mm])?$/;
    if ( !(matches = re.exec( this.userInputElement_.value )) ) {
        return null;
    }
    hour = +matches[1];
    minute = +matches[2] || 0;
    period = (matches[3] || 'A').toUpperCase();
    if ( hour < 0 || hour > 23 || minute < 0 || minute > 59 ) {
        return null;
    }
    if ( hour === 12 && period === 'A' ) {
        hour = 0;
    }
    if ( hour < 12 && period == 'P' ) {
        hour += 12;
    }
    
    return {
        'hours': hour,
        'minutes': minute
    };
};


wolf.ui.DateTimePicker.prototype.renderTime_ = function() {
    goog.dom.forms.setValue( this.userInputElement_, this.dateTime_.toUsTimeString() );
};


wolf.ui.DateTimePicker.prototype.updateTime_ = function() {
    var parsedInput,
        selectEvent,
        changeEvent;

    if ( parsedInput = this.parseUserInput_() ) {
        this.dateTime_.setHours( parsedInput.hours );
        this.dateTime_.setMinutes( parsedInput.minutes );

        this.renderTime_();

        selectEvent = new goog.ui.DatePickerEvent(
            wolf.ui.DateTimePicker.Events.SELECT,
            this, this.dateTime_
        );
        this.dispatchEvent( selectEvent );

        changeEvent = new goog.ui.DatePickerEvent(
            wolf.ui.DateTimePicker.Events.CHANGE,
            this, this.dateTime_
        );
        this.dispatchEvent( changeEvent );
    }
};
