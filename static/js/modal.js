// Get the modal
var modal = document.getElementById('loginModal');

// Get the button that opens the modal
var btn = document.getElementById("myBtn");

// Get the <span> element that closes the modal
var cls = document.getElementsByClassName("close")[0];

// Get the modal tab elements
var loginTab = document.getElementById("login-tab-title");
var signupTab = document.getElementById("signup-tab-title");
var activeTab = loginTab;

// When the user clicks on the button, open the modal
if (btn) {
    btn.onclick = function () {
        modal.style.display = "block";
    }
}

// Functions to change the view shown in the modal to different tabs
$(".login-btn").on('click', function(){
    switch2login();
    modal.style.display = "block";
});

$(".user-signup-btn").on('click', function(){
    switch2signup();
    modal.style.display = "block";
})

// When the user clicks on <span> (x), close the modal
cls.onclick = function() {
    modal.style.display = "none";
}

// When the user picks a tab, do something
loginTab.onclick = function() {
    if (activeTab != loginTab) {
        switch2login();
    }
}

signupTab.onclick = function() {
    if (activeTab != signupTab) {
        switch2signup();
    }
}

// Methods which switch the tabs
function switch2login() {
    $('#login-tab-title').css("background-color", '#f4eaff');
    $('#login-tab-title').css("color", '#a81d73');
    $('#signup-tab-title').css("background-color", '#a81d73');
    $('#signup-tab-title').css("color", '#ffffff');
    activeTab = loginTab;
    $('#signup-form').css("display", "none");
    $('#login-form').css("display", "block");
}

function switch2signup() {
    $('#signup-tab-title').css("background-color", '#f4eaff');
    $('#signup-tab-title').css("color", '#a81d73');
    $('#login-tab-title').css("background-color", '#a81d73');
    $('#login-tab-title').css("color", '#ffffff');
    activeTab = signupTab
    $('#login-form').css("display", "none");
    $('#signup-form').css("display", "block");
}

// If the page has the optional context variable, opens the modal automatically
$(document).ready(function() {
    var popup = $("#loginModal").attr("data-popup");
    if (popup.toLowerCase() == 'login') {
        switch2login()
        modal.style.display = "block";
    } else if (popup.toLowerCase() == 'signup') {
        switch2signup()
        modal.style.display = "block";
    }

})

// Ajax method to log in without being taken to another page
$('#login_form').submit(function (e) {
    e.preventDefault(); // stops the form from changing the page
    var form = $(this).closest('form'); // get a reference to the form
    $('#login-notif-text').text('');
    $.ajax({
        type: $(this).attr('method'), //'POST',
        data: $(this).serialize(),
        url: form.attr("action"),
        success: function (response) {
            setTimeout(function(){
                $('#login-load').removeClass('loader') // hide the loader
                if (response['login']) {
                    $("input").prop('disabled', false); // enable inputs after the request is complete
                    location.reload();
                } else {
                    $('#login-notif-text').text(response['error']); // show error text
                    $("input").prop('disabled', false);
                }
            }, 700); // delay they success by a bit
        },
        error: function (response) {
            $('#login-load').removeClass('loader') // hide the loader
            $('#login-notif-text').text(response.status + ': ' + response.statusText);
            $("input").prop('disabled', false);

        }
    })
    // $('.loader').css("color", "#a81d73");
    $('#login-load').addClass('loader') // show the loader
    $("input").prop('disabled', true); // disable the inputs while the request is processing
})


