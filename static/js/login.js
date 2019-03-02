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
btn.onclick = function() {
    modal.style.display = "block";
}

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

// $('#user_form').submit(function (e) {
//     e.preventDefault();
//     var form = $(this).closest('form');
//     $.ajax({
//         type: $(this).attr('method'), //'POST',
//         data: $(this).serialize(),
//         url: form.attr("form-registration"),
//         success: function (result) {
//             debugger;
//
//         },
//         error: function (data) {
//             debugger;
//         }
//     })
// })
