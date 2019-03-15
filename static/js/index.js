$(document).ready(function() {
    $('input#search').autocomplete({
        source: ajax_search_link,
        select: function (event, ui) {
            AutoCompleteSelectHandler2(event, ui)
        },
        minLength: 1,
    })
        .autocomplete( "instance" )._renderItem = function( ul, item ) {
        return $("<li><div><img src='" + item.img + "'><div>" + item.value + "</div></div></li>").appendTo(ul);
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