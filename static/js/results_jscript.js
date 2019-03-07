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
    var searchResults = [];
    if (results.length == 0) {
        alert('No results for that search found');
    } else {
        clearMarkers();
        $('#hairdressers_information_box').html('');
        for (i = 0; i < results.length; i++) {
            $('#hairdressers_information_box').append(
                '<div class="hairdresser" id="hairdresser'+ results[i].fields['user'] +'">\n' +
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
            searchResults[i] = {
                id: results[i]['pk'],
                user: results[i].fields['user'],
                LatLng: {
                    lat: Number(results[i].fields['latitude']),
                    lng: Number(results[i].fields['longitude'])
                },
                name: results[i].fields['name'],
            }
        };
        loadMarkers(searchResults);
    }
}

function searchFilter() {
    $.ajax({
        type: 'POST',
        data: {
            // 'types': $('#hair_types'),
            //    'value': $('#vrating'),
            //    'rating': $('#orating'),
            //    'service': $('#srating'),
            //    'atmosphere': $('#arating'),
               'latMin': latitudeBounds[0],
               'latMax': latitudeBounds[1],
               'lngMin': longitudeBounds[0],
               'lngMax': longitudeBounds[1],
               'city': $('#searchTxt').val(),
            },
               // 'csrfmiddlewaretoken': $('#searchTxt').attr('data-token')},
        url: $('#searchTxt').attr('data-link'),
        success: function (response) {
            console.log("new lat bnds: " + latitudeBounds + "|lng bnds: " + longitudeBounds);
            results = JSON.parse(response['results'])
            setResults(results)
            //searchGeocode($('#searchTxt').val())
        }
    })
}

function highlightMarkerInList(selectedMarker) {
    for (var i =0;i<markers.length;i++) {
        $('#hairdresser'+markers[i]["user"]).removeClass('selected-marker')
    }
    $('#hairdresser'+selectedMarker["user"]).addClass('selected-marker')
}

function highlightMarkerOnMap(user) {
    debugger; //// ##########impement what happens when you clock on a menu item
}
