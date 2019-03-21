
window.onload = function () {
   if (has_user_page) {
      console.log('dadaf');
   $.ajax({
      url: window.location.href + "checkfavourite",

      
      success: function (json) {
         if (json.is_favourite) {
            $('favText').text("Click to remove from favourites")
            $('.favourites').css('color', '#a81d73')
         } else {
            $('favText').html("Click to remove from favourites")
            $('.favourites').css('color', '#f2f2f2')
         }

      }
   });
};
}

function treatment() {

   $(".changing-content").load("loadtest .treatment-content")
}

function review() {
   $(" .changing-content").load(location.href + " .review-content")
}
function makeReview() {

   window.location.href = window.location.href + "review";
}

function addFavourite() {
   $.ajax({
      url: window.location.href + "addfavourite",

      success: function (json) {

         if (json.exists) {
            $('.favourites').css('color', '#a81d73')
         } else {
            $('.favourites').css('color', '#f2f2f2')
         }

      }
   });

}