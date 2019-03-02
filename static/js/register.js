$(document).ready(function () {
    console.log($('#link').val())
    if ($('#link').val() != '' ){
        setTimeout(function(){
            window.location.href = $('#link').val();
        }, 5000);
    }
})