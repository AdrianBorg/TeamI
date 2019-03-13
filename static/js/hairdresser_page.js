
function treatment() {
 
   $(".changing-content").load("loadtest .treatment-content")
}

function review() {
   $(" .changing-content").load(location.href + " .review-content")
}
function makeReview() {
  
 window.location.href = window.location.href +"review"; 
}