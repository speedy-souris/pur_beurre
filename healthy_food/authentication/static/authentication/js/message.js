/* Pop-up message for html
for login, logout, incorrect authentication, etc.
*/

document.addEventListener('DOMContentLoaded', function() {
    // We check if the variable ‘djangoMessages’ exists.
    if (typeof djangoMessages !== 'undefined' && djangoMessages.length > 0) {

        djangoMessages.forEach(function(msg) {
            // Mapping Django tags to SweetAlert icons
            // Django: debug, info, success, warning, error
            // SweetAlert: info, success, warning, error, question
            let iconType = msg.tag;
            if (iconType === 'debug') iconType = 'info';

            Swal.fire({
                title: 'Information',
                text: msg.text,
                icon: iconType,
                confirmButtonText: 'OK',
                confirmButtonColor: '#3085d6',
                timer: 4000,
                timerProgressBar: true
            });
        });
    }
});