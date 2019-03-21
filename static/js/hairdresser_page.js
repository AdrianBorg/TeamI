
function treatment() {
 
   $(".changing-content").load("loadtest .treatment-content")
}

function review() {
   $(" .changing-content").load(location.href + " .review-content")
}
function makeReview() {
  
 window.location.href = window.location.href +"review"; 
}

function addFavourite() {
   
   $.ajax({
      url: window.location.href + "addfavourite",
     
      success: function (json) {
         
          if(json.exists) {
            $('.favourites').css('color', 'red')
          } else {
             $('.favourites').css('color', 'yellow')
          }
      
      }
    });
   
}