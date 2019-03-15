// $(document).ready(function(){
//     $("#txtSearch").autocomplete({
//         url: "/trimit/ajax_calls_search/",
//         minLength: 2,
//         open: function(){
//             setTimeout(function(){
//                 $('.ui-autocomplete').css('z-index',99);
//             }, 0);
//         }
//     });
// });

$(function(){
    $("#name").autocomplete({
        source: "/trimit/ajax_calls_search/",
        select: function(event,ui){
            AutoCompleteSelectHandler(event,ui)
        },
        minLength: 2,
    });
});

function AutoCompleteSelectHandler(event, ui){
    var selectedObj = ui.item;
}



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
