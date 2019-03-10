$('document').ready(function(){
    setResults(resultset, picture_urls);
});

$('document').ready(function(){
    // debugger;
    searchGeocode(searchLocation);
});

function sliderSettings(handle) {
    return {
        orientation: "horizontal",
        range: "min",
        min: 10,
        max: 50,
        value: 10,
        create: function(  ) {
            sliderInit(handle);
        },
        slide: function( event, ui ) {
            sliderSlide(handle, event, ui);
        },
        stop: function () {
            searchFilter();
        }
    };
};

function sliderInit(handle) {
    handle.text( 'all' );
}

function sliderSlide(handle, event, ui) {
    if (ui.value == 10) {
        handle.text( 'all' );
    } else {
        handle.text(ui.value / 10 + '+');
    }
}

$( function() {
    var handle = $( "#vrating_handle" );
    $( "#vrating_slider" ).slider(sliderSettings(handle));
} );

$( function() {
    var handle = $( "#srating_handle" );

    $( "#srating_slider" ).slider(sliderSettings(handle));
} );

$( function() {
    var handle = $( "#arating_handle" );

    $( "#arating_slider" ).slider(sliderSettings(handle));
} );

$( function() {
    var handle = $( "#orating_handle" );

    $( "#orating_slider" ).slider(sliderSettings(handle));
} );

function setMapOnSearchLoc(searchLoc) {
    $('document').ready(function(){
        searchGeocode(searchLoc);
    });
}

$('div#tags_filters').on('select2-close', function(e) {
    var options = JSON.parse($('#id_specialities').attr('data-tag-list'));
    var input = $('li.select2-search-choice:last div').text();
    if (!options.includes(input)){
        $('li.select2-search-choice:last').remove();
    } else {
        searchFilter();
    }
});

$('div#tags_filters').on('select2-removed', function(e) {
    var options = JSON.parse($('#id_specialities').attr('data-tag-list'));
    var removed = e.val;
    if (options.includes(removed)){
        searchFilter();
    }
});


function setResults(results, image_urls) {
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
            '       <img src="'+ image_urls[results[i].fields['user']] +'" width="30%" height="30%">\n' +
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
            'value': $('#vrating_slider').slider("option", "value")/10,
            'overall': $('#orating_slider').slider("option", "value")/10,
            'service': $('#srating_slider').slider("option", "value")/10,
            'atmosphere': $('#arating_slider').slider("option", "value")/10,
            'latMin': latitudeBounds[0],
            'latMax': latitudeBounds[1],
            'lngMin': longitudeBounds[0],
            'lngMax': longitudeBounds[1],
            'specialityTags': JSON.stringify(getTagFilters()),
            // 'city': $('#searchTxt').val(),
            csrfmiddlewaretoken: CSRFtoken,
            'logged_in': LOGGED_IN,
        },

        url: AJAXlink,
        success: function (response) {
            // console.log("new lat bnds: " + latitudeBounds + "|lng bnds: " + longitudeBounds);
            results = JSON.parse(response['results']);
            image_urls = response['profile_picture_urls'];
            setResults(results, image_urls)
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


