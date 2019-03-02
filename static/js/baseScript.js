
function home() {
    window.location = "http://localhost:8000/trimit/"
}

function hairdresserSignup(){
    window.location = "http://localhost:8000/trimit/"
}

function userSignup(){
    window.location = "http://localhost:8000/trimit/"
}

function login(){
    window.location = "http://localhost:8000/trimit/"
}

function contact(){
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