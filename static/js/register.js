
// once the registration is finished successfully, redirect the user to the page they were at before starting registration
$(document).ready(function () {
    console.log($('#link').val())
    if ($('#link').val() != '' ){
        setTimeout(function(){
            window.location.href = $('#link').val();
        }, 3000);
    }
})

// set the countries flag to the one relevent to the chosen country in the countries field
$('#country-field').on('change', function () {
    var url = $('#head').attr('data-static-images') + 'flags/' + $('#country-field').val().toLowerCase() + '.gif';
    $('.country-select-flag').attr('src', url);
})