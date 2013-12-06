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
    menuNode.addEventListener( 'hover', drop, false );
}

jQuery( document ).ready(function() {
    var i,
        dropdownNodes,
        statusNode;

    dropdownNodes = jQuery('.dropdown');
    for ( i=0; i<dropdownNodes.length; i++ ) {
        new Dropdown( dropdownNodes[i] );
    }
    statusNode = document.getElementById('statusContainer');
    window.setTimeout(function() {
        slideUp( statusNode );
    }, 5000);
})