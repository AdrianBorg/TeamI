$(document).ready(function(){
    $("#txtSearch").autocomplete({
        source: "/trimit/search_input/",
        minLength: 2,
        open: function(){
            setTimeout(function(){
                $('.ui-autocomplete').css('z-index',99);
            }, 0);
        }
    });
});

// $ (function(){

//     $('#search').keyup(function(){

//         $.ajax({
//             type: 'POST',
//             url: "/search_input/",
//             data: { 'search_text' : $('#search').val()},

//             success = searchSuccess,
//             datatype = 'html'

//         })

//     })
// })

// function searchSuccess(data,textStatus,jqXHR) {
//     $('#search-results').html(data);
// }
