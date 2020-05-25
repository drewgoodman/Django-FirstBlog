
$(document).ready(function () {


    $(".search-bar-form").on("submit", function (event) {
        event.preventDefault();
        var search_query = $(this).find(".search-bar-query").val();
        var search_href = search_query ? home_url + "?query=" + search_query : home_url;
        window.location.replace(search_href);

    })

    $(window).scroll(function(){
        if($(this).scrollTop() > $(window).height()) {
            $('#scroll-to-top').fadeIn();
        } else {
            $('#scroll-to-top').fadeOut();
        }
    })  

    $('#scroll-to-top').click(function() {
        $('html, body').animate({scrollTop: 0}, 700);
        return false;
    })

});