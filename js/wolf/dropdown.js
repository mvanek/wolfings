goog.provide('wolf.ui.dropdown');

wolf.ui.Dropdown = function( menuNode ) {
    this.menuNode = menuNode;
    this.submenuNode = find_submenu();
    this.submenuNode.style.width = this.menuNode.offsetWidth + "px";
    this.menuNode.addEventListener( 'hover', drop, false );
}

wolf.ui.dropdown.prototype.find_submenu = function() {
    var i;
    for ( i=0; i<this.menuNode.childNodes.length; i++ ) {
        if ( this.menuNode.childNodes[i].className == 'submenu' ) {
            return this.menuNode.childNodes[i];
        }
    }
}
