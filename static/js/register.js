(function() {
    var phoneInput,
        phoneLabel, labels,
        i;

    function isValidPhone( val ) {
        val = val.replace(/[^0-9]/g, '');
        if (val.length != 10) {
            return false;
        }
        return true;
    }

    function validateForm() {
        if ( phoneInput.value.length == 0 ) {
            phoneLabel.className = '';
            return;
        }
        if ( !isValidPhone( phoneInput.value ) ) {
            phoneLabel.className = 'invalid';
        } else {
            phoneLabel.className = 'valid';
        }
    }

    phoneInput = document.forms[0]['phone'];
    labels = document.getElementsByTagName('label');
    for ( i=0; i<labels.length; i++ ) {
        if ( labels[i].htmlFor == 'phone' ) {
            phoneLabel = labels[i];
            break;
        }
    }
    phoneInput.addEventListener('change', validateForm, false);
    validateForm();
;})();
