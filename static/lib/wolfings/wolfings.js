// Array Remove - By John Resig (MIT Licensed)
Array.prototype.remove = function(from, to) {
  var rest = this.slice((to || from) + 1 || this.length);
  this.length = from < 0 ? this.length + from : from;
  return this.push.apply(this, rest);
};


var WOLFINGS = (function() {
    var obj,
        modules,
        loading,
        namespace;

    modules = [];
    loading = {};
    namespace = {};

    obj = function() {}
    obj.prototype.api = {};
    obj.prototype.utils = {};
    obj.prototype.handlers = {};


    obj.prototype.get = function( key ) {
        return namespace[ key ];
    }
    obj.prototype.set = function( key, value ) {
        return namespace[ key ] = value;
    }

    
    obj.prototype.import = function( path, callback ) {
        var script,
            onload;

        if ( modules.indexOf( path ) > -1 ) {
            return callback();
        }

        if ( loading[ path ] ) {
            script = loading[ path ];
            onload = (function( f ) {
                return function() {
                    f();
                    if ( callback ) {
                        callback();
                    }
                }
            })( script.onload );
        } else {
            var append_script;
            script = document.createElement('script');
            script.src = '/static/lib/wolfings/' + path + '.js';
            loading[ path ] = script;
            onload = function() {
                modules.push( path );
                delete loading[ path ];
                if ( callback ) {
                    callback();
                }
            }
            append_script = function() {
                if ( document.body ) {
                    document.body.appendChild( script );
                } else {
                    window.setTimeout(append_script, 0);
                }
            }
            append_script();
        }

        script.onreadystatechange = onload;
        script.onload = onload;
    }


    obj.prototype.self_import = function( dest, F ) {
        switch ( dest ) {
            case 'api':
                dest = obj.prototype.api;
                break;
            case 'utils':
                dest = obj.prototype.utils;
                break;
            case 'handlers':
                dest = obj.prototype.handlers;
                break;
        }
        for ( key in F ) {
            dest[ key ] = F[ key ];
        }
    }


    obj.prototype.log = function( msg ) {
        if ( console && console.log ) {
            return console.log( msg );
        }
        return undefined;
    }


    obj.prototype.list_modules = function() {
        return modules.slice(0);
    }

    return new obj();
})();


/* Import utils */
WOLFINGS.import('utils');
