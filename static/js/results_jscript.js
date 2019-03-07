$( function() {
    $( "#price_slider" ).slider({
        range: true,
        min: 0,
        max: 500,
        values: [ 75, 300 ],
        slide: function( event, ui ) {
            $( "#amount" ).val( "$" + ui.values[ 0 ] + " - $" + ui.values[ 1 ] );
        }
    });
    $( "#amount" ).val( "$" + $( "#slider-range" ).slider( "values", 0 ) +
        " - $" + $( "#slider-range" ).slider( "values", 1 ) );
} );

$( function() {
    $( "#distance_slider" ).slider({
        orientation: "horizontal",
        range: "min",
        min: 0,
        max: 100,
        value: 60,
        slide: function( event, ui ) {
            $( "#amount" ).val( ui.value );
        }
    });
    $( "#amount" ).val( $( "#slider-horizontal" ).slider( "value" ) );
} );

$('document').ready(function(){
    setResults(resultset);
});

$('document').ready(function(){
    // debugger;
    searchGeocode(searchLocation);
});

function setMapOnSearchLoc(searchLoc) {
    $('document').ready(function(){
        searchGeocode(searchLoc);
    });
}

function setResults(results) {
    // debugger;
    var i;
    if (results.length == 0) {
        alert('No results for that search found');
    } else {
        $('#hairdressers_information_box').html('');
        for (i = 0; i < results.length; i++) {
            $('#hairdressers_information_box').append(
                '<div class="hairdresser">\n' +
                '   <div id="image_box">\n' +
                '       <img src="//:0" width="30%" height="30%">\n' +
                '   </div>\n' +
                '   <div id="hairdresser_data">\n' +
                '       <div id="name_and_distance">\n' +
                '           <p3>' + results[i].fields['name'] + '</p3>' +
                '       </div>\n' +
                '   </div>\n' +
                '   <div id="rating">\n' +
                '       <p5>' + results[i].fields['city'] + '</p5>\n' +
                '   </div>\n' +
                '<hr>\n' +
                '</div>\n'
            );
        }
        ;
    }
}

// function csrfSafeMethod(method) {
//     // these HTTP methods do not require CSRF protection
//     return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
// }
//
// $.ajaxSetup({
//     beforeSend: function(xhr, settings) {
//         if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
//             xhr.setRequestHeader("X-CSRFToken", $('#searchTxt').attr('data-token'));
//         }
//     }
// });

function searchFilter(search) {
    $.ajax({
        type: 'POST',
        data: {'city': search},
               // 'csrfmiddlewaretoken': $('#searchTxt').attr('data-token')},
        url: $('#searchTxt').attr('data-link'),
        success: function (response) {
            results = JSON.parse(response['results'])
            setResults(results)
            searchGeocode(search)
        }
    })
}
