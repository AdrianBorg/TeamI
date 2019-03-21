
// set the results of the search on the map when loaded
$('document').ready(function(){
    setResults(resultset, picture_urls, ratings);
});

// search the location of the query when loaded
$('document').ready(function(){
    // debugger;
    searchGeocode(searchLocation);
});

// helper functions to return slider settings for the sliders
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
        handle.text('all');
    } else if (ui.value == 50) {
        handle.text('5');
    } else {
        handle.text(ui.value / 10 + '+');
    }
}

// setting up the sliders
$( function() {
    var handle = $( "#vrating_handle" );
    $( "#vrating_slider" ).slider(sliderSettings(handle));
} );
// service rating slider
$( function() {
    var handle = $( "#srating_handle" );
    $( "#srating_slider" ).slider(sliderSettings(handle));
} );
// atmosphere rating slider
$( function() {
    var handle = $( "#arating_handle" );
    $( "#arating_slider" ).slider(sliderSettings(handle));
} );
// // overall rating slider
$( function() {
    var handle = $( "#orating_handle" );
    $( "#orating_slider" ).slider(sliderSettings(handle));
} );

// action listener on selecting a specialities
$('div#tags_filters').on('select2-close', function(e) { // when the suggestion window is closed
    var options = JSON.parse($('#id_specialities').attr('data-tag-list')); // get all the specialities options
    var input = $('li.select2-search-choice:last div').text(); // get the value input by the user
    if (!options.includes(input)){ // if the input is not an option
        $('li.select2-search-choice:last').remove(); // remove the tag created
    } else {
        searchFilter(); // otherwise update the search results with the new options
    }
});

// action listener on removing a speciality
$('div#tags_filters').on('select2-removed', function(e) {
    var options = JSON.parse($('#id_specialities').attr('data-tag-list')); // get all the speciality options
    var removed = e.val; // get the removed tag value
    if (options.includes(removed)){ // if the removed tag was one of the options
        searchFilter(); // update the search results with new options
    }
});

// create the menu items for the search results
function setResults(results, image_urls, ratings) {
    var i;
    var searchResults = [];


    clearMarkers();
    $('#hairdressers_information_box').html(''); // reset all menu items
    if (results.length == 0) { // if no search results show the appropriate message
        $('#hairdressers_information_box').html(
            '<div class="hairdresser" id="no_results">\n' +
            '    <err>Unfortunately, no results were found for your search!</err>\n' +
            '</div>'
        );
    }
    for (i = 0; i < results.length; i++) { // for each search result add a menu item with the appropriate information
        $('#hairdressers_information_box').append(
            '<div class="hairdresser" id="hairdresser'+ results[i].fields['user'] +'">' +
            '   <div class="image_box">' +
            '       <img src="'+ image_urls[results[i].fields['user']] +'" width="30%" height="30%">' +
            '   </div>' +
            '   <div class="data_box">' +
            '       <div class="hairdresser_content">' +
            '           <div class="hairdresser_data">' +
            '               <div class="name_and_distance">' +
            '                   <p3>' + results[i].fields['name'] + '</p3>' +
            '               </div>' +
            '           </div>' +
            '           <div class="hairdresser_rating_box">' +
            '               <p4>Overall: <p5>' + ratings[results[i].fields['user']] + '</p5></p4>' +
            '           </div>' +
            '       </div>' +
            '       <a href="hairdresser/' + results[i].fields['slug'] + '/"><img src="' + page_link_image_url + '"></a>' +
            '   </div>' +
            // '<hr>' +
            '</div>'
        );
        searchResults[i] = { // save a reference of info required for markers
            id: results[i]['pk'],
            user: results[i].fields['user'],
            LatLng: {
                lat: Number(results[i].fields['latitude']),
                lng: Number(results[i].fields['longitude'])
            },
            name: results[i].fields['name'],
        }
    };
    loadMarkers(searchResults); // load markers
}

// ajax method to request results of the searching parameters
function searchFilter() {
    $.ajax({
        type: 'POST',
        data: { // get the filtering terms
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
        success: function (response) { // once the request is returned, update the map and info box as necessary
            results = JSON.parse(response['results']);
            image_urls = response['profile_picture_urls'];
            ratings = response['ratings'];
            setResults(results, image_urls, ratings)
            if (response['favourites']) {
                favouriteHairdressers = JSON.parse(response['favourites']);
            }
            highlightMarkerInList(selectedMarker);
        }
    })
}

// highlight the menu item relevant to the marker passed into the function
function highlightMarkerInList(selectedMarker) {
    for (var i =0;i<markers.length;i++) {
        $('#hairdresser'+markers[i]["user"]).removeClass('selected-marker')
    }
    $('#hairdresser'+selectedMarker["user"]).addClass('selected-marker')
}

// highlight the relevant marker to the menu item that is clicked
$(document).on('click', '.hairdresser', function() {
    var user = $(this).attr('id').replace('hairdresser', '');
    for (var i=0;i<markers.length;i++) {
        if (markers[i].user == user) {
            markerClicked(markers[i].id);
            break;
        }
    }
})

// retrieve all the tags in the specialities filter box
function getTagFilters() {
    var specitalityTags = [];
    $('.tag_filter .tag-row .tag-values div ul').children('.select2-search-choice').each(function () {
        specitalityTags.push($(this).children('div').text())
    })
    return specitalityTags;
}

// testing function
function setMapOnSearchLoc(searchLoc) {
    $('document').ready(function(){
        searchGeocode(searchLoc);
    });
}
