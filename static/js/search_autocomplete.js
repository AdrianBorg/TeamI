$(document).ready(function() {
    $('#searchAC').autocomplete({
        source: ajax_search_link,
        select: function (event, ui) {
            AutoCompleteSelectHandler(event, ui)
        },
        minLength: 1,
    })
        .autocomplete( "instance" )._renderItem = function( ul, item ) {
        return $("<li><div><img src='" + item.img + "'><div>" + item.value + "</div></div></li>").appendTo(ul);
    };
});

// resize width of suggestions to width of the input box
$(document).ready(function() {
    jQuery.ui.autocomplete.prototype._resizeMenu = function () {
      var ul = this.menu.element;
      ul.outerWidth(this.element.outerWidth());
    }
});

function AutoCompleteSelectHandler(event, ui) {
    var selectedObj = ui.item;
    $('#searchAC').val(selectedObj.value)
    $('#searchType').val(selectedObj.type)
    if (selectedObj.slug) {
        $('#searchSlug').val(selectedObj.slug)
    } else {
        $('#searchSlug').val('')
    }
    selectionMade();
};

$(document).ready(function() {
    $('#searchAC').on('keypress', function(e) {
        if (e.which == 13) {
            selectionMade();
        }
    })
});

function selectionMade() {
    if ($('#searchType').val() == 'city') {
        window.location.href = search_url + '?q=' + $('#searchAC').val();
    } else if ($('#searchType').val() == 'page') {
        window.location.href = page_url + $('#searchSlug').val() + '/';
    } else {
        window.location.href = search_url + '?q=' + $('#searchAC').val();
    }
}

$(document).ready(function() {
    $('input#search').autocomplete({
        source: ajax_search_link,
        select: function (event, ui) {
            AutoCompleteSelectHandler2(event, ui)
        },
        minLength: 1,
    });
    if ( $('input#search').length) {
     $('input#search')
         .autocomplete("instance")._renderItem = function (ul, item) {
            return $("<li><div><img src='" + item.img + "'><div>" + item.value + "</div></div></li>").appendTo(ul);
        };
    };
});

function AutoCompleteSelectHandler2(event, ui) {
    var selectedObj = ui.item;
    $('#search').val(selectedObj.value)
    $('#searchType2').val(selectedObj.type)
    if (selectedObj.slug) {
        $('#searchSlug2').val(selectedObj.slug)
    } else {
        $('#searchSlug2').val('')
    }
    selectionMade2();
};

$(document).ready(function() {
    $('#search').on('keypress', function(e) {
        if (e.which == 13) {
            selectionMade2();
        }
    })
});

function selectionMade2() {
    if ($('#searchType2').val() == 'city') {
        window.location.href = search_url + '?q=' + $('#search').val();
    } else if ($('#searchType2').val() == 'page') {
        window.location.href = page_url + $('#searchSlug2').val() + '/';
    } else {
        window.location.href = search_url + '?q=' + $('#search').val();
    }
}