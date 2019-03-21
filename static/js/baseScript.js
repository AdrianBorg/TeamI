// Button click listeners

function login(){
    window.location = "http://localhost:8000/trimit/"
}

function about(){
    window.location = "http://localhost:8000/trimit/"
}

$(".home-btn").on('click', function(){
    var url = $("li.home-btn").attr("data-link");
     window.location = url;
});

$(".contact-us-btn").on('click', function(){
    var url = $("li.contact-us-btn").attr("data-link");
     window.location = url;
});

$(".about-btn").on('click', function(){
    var url = $("li.about-btn").attr("data-link");
     window.location = url;
});

$(".hairdresser-signup-btn").on('click', function(){
    var url = $("li.hairdresser-signup-btn").attr("data-link");
     window.location = url;
});

$(".logout-btn").on('click', function(){
    var url = $("li.logout-btn").attr("data-link");
     window.location = url;
});

$(".profile-btn").on('click', function(){
    var url = $("a.profile-btn").attr("data-link");
    debugger;
    window.location = url;
});
$(".account-btn").on('click', function(){
    var url = $("a.account-btn").attr("data-link");
    window.location = url;
});
