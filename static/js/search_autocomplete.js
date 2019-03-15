$(document).ready(function() {
    $('#search').autocomplete({
        source: ajax_search_link,
        select: function (event, ui) {
            AutoCompleteSelectHandler(event, ui)
        },
        minLength: 1,
    })
    .autocomplete( "instance" )._renderItem = function( ul, item ) {
        return $( "<li><div><img src='"+item.img+"'><div>"+item.value+"</div></div></li>" ).appendTo( ul );
      };
});

function AutoCompleteSelectHandler(event, ui) {
    var selectedObj = ui.item;
    $('#searchType').val(selectedObj.type)
    if (selectedObj.slug) {
        $('#searchSlug').val(selectedObj.slug)
    } else {
        $('#searchSlug').val('')
    }
    selectionMade();
};

$(document).ready(function() {
    $('#search').on('keypress', function(e) {
        if (e.which == 13) {
            selectionMade();
        }
    })
});

function selectionMade() {
    if ($('#searchType').val() == 'city') {
        window.location.href = search_url + '?q=' + $('#search').val();
    } else if ($('#searchType').val() == 'page') {
        window.location.href = page_url + $('#searchSlug').val() + '/';
    } else {
        window.location.href = search_url + '?q=' + $('#search').val();
    }
}