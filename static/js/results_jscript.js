$( function() {
    var handle = $( "#vrating_handle" );
    $( "#vrating_slider" ).slider({
        orientation: "horizontal",
        range: "min",
        min: 10,
        max: 50,
        value: 10,
        create: function() {
        handle.text( $( this ).slider( "value" ) );
      },
      create: function(  ) {
        handle.text( 10/10 + '+' );
      },
      slide: function( event, ui ) {
        handle.text( ui.value/10 + '+' );
      }
    });
    $( "#amount" ).val( $( "#slider-horizontal" ).slider( "value" ) );
} );

$( function() {
    var handle = $( "#srating_handle" );

    $( "#srating_slider" ).slider({
        orientation: "horizontal",
        range: "min",
        min: 10,
        max: 50,
        value: 10,
        create: function() {
        handle.text( $( this ).slider( "value" ) );
      },
      create: function(  ) {
        handle.text( 10/10 + '+' );
      },
      slide: function( event, ui ) {
        handle.text( ui.value/10 + '+' );
      }
    });
    $( "#amount" ).val( $( "#slider-horizontal" ).slider( "value" ) );
} );

$( function() {
    var handle = $( "#arating_handle" );

    $( "#arating_slider" ).slider({
        orientation: "horizontal",
        range: "min",
        min: 10,
        max: 50,
        value: 10,
        create: function() {
        handle.text( $( this ).slider( "value" ) );
      },
      create: function(  ) {
        handle.text( 10/10 + '+' );
      },
      slide: function( event, ui ) {
        handle.text( ui.value/10 + '+' );
      }
    });
    $( "#amount" ).val( $( "#slider-horizontal" ).slider( "value" ) );
} );

$( function() {
    var handle = $( "#orating_handle" );

    $( "#orating_slider" ).slider({
        orientation: "horizontal",
        range: "min",
        min: 10,
        max: 50,
        value: 10,
        create: function() {
        handle.text( $( this ).slider( "value" ) );
      },
      create: function(  ) {
        handle.text( 10/10 + '+' );
      },
      slide: function( event, ui ) {
        handle.text( ui.value/10 + '+' );
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
               // 'city': $('#searchTxt').val(),
               csrfmiddlewaretoken: CSRFtoken,
               'logged_in': LOGGED_IN,
            },

        url: AJAXlink,
        success: function (response) {
            console.log("new lat bnds: " + latitudeBounds + "|lng bnds: " + longitudeBounds);
            results = JSON.parse(response['results']);
            setResults(results)
            if (response['favourites']) {
                favouriteHairdressers = JSON.parse(response['favourites']);
            }
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

$(document).on('click', '.hairdresser', function() {
    var user = $(this).attr('id').replace('hairdresser', '');
    for (var i=0;i<markers.length;i++) {
        if (markers[i].user == user) {
            markerClicked(markers[i].id);
            break;
        }
    }

})

function highlightMarkerOnMap(user) {
    debugger; //// ##########impement what happens when you clock on a menu item
}
