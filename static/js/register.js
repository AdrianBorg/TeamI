$(document).ready(function () {
    console.log($('#link').val())
    if ($('#link').val() != '' ){
        setTimeout(function(){
            window.location.href = $('#link').val();
        }, 3000);
    }
})

$('#country-field').on('change', function () {
    var url = $('#head').attr('data-static-images') + 'flags/' + $('#country-field').val().toLowerCase() + '.gif';
    $('.country-select-flag').attr('src', url);
})