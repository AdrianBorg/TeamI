// Map Js
var map;
var geocoder;
var markers = [];
var markerIcons = {
    default: null,
    red: { url: "../static/images/red-dot-icon.png" }, //"http://maps.google.com/mapfiles/ms/icons/red-dot.png" },
    blue: { url: "../static/images/blue-dot-icon.png" }, //"http://maps.google.com/mapfiles/ms/icons/blue-dot.png" }
    yellow: { url: "../static/images/yellow-dot-icon.png" },
    orange: { url: "../static/images/orange-dot-icon.png" },
    purple: { url: "../static/images/purple-dot-icon.png" },
}
var favouriteIds = [3, 5, 7]; // CHANGE BACK TO EMPTY ##########################################

function initMap() {
    var noPoiLabels = [
        {
            featureType: "poi",
            elementType: "labels",
            stylers: [
                { visibility: "off" }
            ],
        }]

    var options = {
        zoom: 12,
        center: { lat: 55.8642, lng: -4.2518 },
        disableDefaultUI: true, // hide all controls
        scaleControl: true, // make scale visible
        zoomControl: true, // make zoom controls visible
        clickableIcons: false,
        mapTypeId: google.maps.MapTypeId.ROADMAP,
        styles: noPoiLabels,
    };

    map = new google.maps.Map(document.getElementById('map'), options);
    geocoder = new google.maps.Geocoder;

    //searchGeocode(''); // search location NEED TO ENTER
}

// searches for the location passed (as a string)
function searchGeocode(location) {
    geocoder.geocode({ 'address': location }, function (results, status) {
        if (status == 'OK') {
            map.setCenter(results[0].geometry.location);
            map.set
        } else {
             console.log('Geocode was not successful for the following reason: ' + status);
        }
    })
}

// makes markers visible
function showMarkers() {
    for (var i=0;i<markers.length;i++) {
        markers[i].setVisible(true);
    }
}

// makes markers invisible
function hideMarkers() {
    for (var i=0;i<markers.length;i++) {
        markers[i].setVisible(false);
    }
}

// loads an array of markers into the array
function loadMarkers(markersArr) {
    for (var i=0;i<markersArr.length;i++) {
        addMarker(markersArr[i]);
    }
}

// adds a marker to the markers array
function addMarker(marker) {
    var newMarker = new google.maps.Marker({
        position: marker.LatLng,
        map: map,
        id: marker.id,
        icon: markerIcons.red,
    });
    newMarker.addListener('click', function() {
        markerClicked(newMarker.id)
    });
    markers.push(newMarker);
    setFavouriteMarkers();
}

// clears the marker array
function clearMarkers() {
    for (var i=0;i<markers.length;i++) {
        markers[i].setMap(null);
    }
    markers = [];
}

// do this when a marker is clicked
function markerClicked(id) {
    var index;
    for (var i=0;i<markers.length;i++) {
        if (markers[i].id == id) {
            index = i;
        } else {
            markers[i].setIcon(markerIcons.red); // set to null to go to default one
        }
    }
    setFavouriteMarkers();
    markers[index].setIcon(markerIcons.blue);
    alert(id); // ######################### change this to what is necessary
}

// set favourite markers to yellow
function setFavouriteMarkers() {
    for (var i=0;i<markers.length;i++) {
        if (favouriteIds.includes(markers[i].id)) {
            markers[i].setIcon(markerIcons.yellow);
        }
    }
}

// populate favourite array
function addFavouriteIds(favArr) {
    for (var i=0;i<favArr.length;i++) {
        favouriteIds.push(faveArr[i].id);
    }
}

// format search results -> ensure search results have an id (name) and lat & long in latlng format
function prepSearchResults() {
    // if (!(markersArr[0].LatLng)) {
    //     for (var i=0;i<markersArr.length;i++) {
    //         markersArr[i] = {
    //             LatLng: { lat: markersArr[i].lat, lng: markersArr[i].lng },
    //             id: markersArr[i].id
    //         };
    //     }
    // }
}

function getMinMaxBounds() {
    var bounds = map.getBounds();
    var left = bounds.getSouthWest().lng();
    var right = bounds.getNorthEast().lng();
    var top = bounds.getNorthEast().lat();
    var bottom = bounds.getSouthWest().lat();
    var output = {
        lat: { min: bottom, max: top },
        lng: { min: left, max: right },
    };
    return output;
}

//testing functions #############################################
var mrkrid = 0;
var markerobjects = [
    {
        LatLng: { lat: 55.865, lng: -4.2518 }
    },
    {
        LatLng: { lat: 55.8635, lng: -4.2518 }
    }
];

// Function to load test markers
function addMarkers() {
    loadMarkers(markerobjects);
    markerobjects.push({
        LatLng: { lat: 55.866, lng: -4.2518 }
    })
}

// add a random marker
function addRandomMarker() {
    var bounds = map.getBounds();
    var left = bounds.getSouthWest().lng();
    var right = bounds.getNorthEast().lng();
    var top = bounds.getNorthEast().lat();
    var bottom = bounds.getSouthWest().lat();
    var lng = random(left, right);
    var lat = random(bottom, top);
    loadMarkers([{
        LatLng: { lat: lat, lng: lng },
        id: mrkrid,
    }]);
    mrkrid++;
}

// Function to create a random number between 2 numbers
function random(min, max) {
    var random = Math.random() * (+max - +min) + +min;
    return random;
}

