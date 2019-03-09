$( function() {
    $( ".regular_slider" ).slider({
        orientation: "horizontal",
        range: "min",
        min: 100,
        max: 500,
        value: 100,
        slide: function( event, ui ) {
            $( ".regular_slider input" ).val(ui.value/100)
            //parent().parent().find("input").val( ui.value );
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

    // if (results.length == 0) {
    //     alert('No results for that search found');
    // }

    clearMarkers();
    $('#hairdressers_information_box').html('');
    if (results.length == 0) {
        $('#hairdressers_information_box').html(
            '<div class="hairdresser" id="no_results">\n' +
            '    <p>Unfortunately, no results were found for your search!</p>\n' +
            '</div>'
        );
    }
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
               'specialityTags': JSON.stringify(getTagFilters()),
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
            highlightMarkerInList(selectedMarker);
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

function getTagFilters() {
    var specitalityTags = [];
    $('.tag_filter .tag-row .tag-values div ul').children('.select2-search-choice').each(function () {
        specitalityTags.push($(this).children('div').text())
    })
    return specitalityTags;
}
