var Dropdown = function( menuNode ) {
    var submenuNode;

    function find_submenu() {
        var i;
        for ( i=0; i<menuNode.childNodes.length; i++ ) {
            if ( menuNode.childNodes[i].className == 'submenu' ) {
                return menuNode.childNodes[i];
            }
        }
    }

    function drop() {
    }

    submenuNode = find_submenu();
    submenuNode.style.width = menuNode.offsetWidth + "px";
    menuNode.addEventListener('hover', drop, false);
}

jQuery( document ).ready(function() {
    var i,
        dropdownNodes;

    dropdownNodes = jQuery('.dropdown');
    for ( i=0; i<dropdownNodes.length; i++ ) {
        new Dropdown( dropdownNodes[i] );
    }
})