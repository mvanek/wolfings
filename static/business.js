/* 
 * BusinessCollection
 *  BusinessCollection(filter:Object)
 *      Constructor
 *      parameters:
 *          filter: filters the searched businesses. Valid values:
 *              - lat, lon: The location near which to search
 *  get(callback:function)
 *      Fetches the list of businesses defined in the constructor, and passes the
 *      array of business ID's to the callback
 *      parameters:
 *          callback(businesses:Array): Called when the server responds
 *
 * Business
 *  Business(id:string|int)
 *      Constructor
 *      parameters:
 *          id: the business ID
 *  get(callback:function)
 *      Fetches the business defined in the constructor, and passes the
 *      object representing it to the callback
 *      parameters:
 *          callback(business:Object): Called when the server responds
 */
var BusinessCollection,
    Business,
    temp;

temp = (function() {
    var BusinessCollection,
        Business;

    function verify( query ) {
        if ( query['lat'] ) {
            if ( !query['lon'] ) {
                return false;
            }
        } else {
            if ( query['lon'] ) {
                return false;
            }
        }
        return true;
    }


    Business = function( id ) {
        this.id = toInt( id );
        if ( !this.id ) {
            return undefined;
        }
        return this;
    }

    Business.prototype.get = function( callback ) {
        $.ajax({
            type: 'GET',
            url: '/api/business/' + this.id
        }).done(function( res ) {
            callback( JSON.parse( res ) );
        });
    }


    BusinessCollection = function( query ) {
        if ( !verify( query ) ) {
            return undefined;
        }
        this.query = query;
        return this;
    }

    BusinessCollection.prototype.get = function( callback ) {
        $.ajax({
            type: 'GET',
            url: '/api/business',
            data: this.query
        }).done(function( res ) {
            var bids,
                businesses;

            bids = res.split('\n');
            businesses = [];
            for ( i = 0; i < bids.length; i++ ) {
                if ( bids[i] ) {
                    businesses.push( new Business( bids[i] ) );
                }
            }
            callback( businesses );
        });
    }

    return [BusinessCollection, Business];
})();

BusinessCollection = temp[0];
Business = temp[1];
