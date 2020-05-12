    
    $(document).ready(function() {

        $("#search-bar-form").on("submit",function(event) {
            event.preventDefault();
            var search_query = $("#search-bar-query").val();
            var search_href = search_query ? home_url + "?query=" + search_query : home_url;
            window.location.replace(search_href);

        })

        $(".comment-reply-btn").click(function(event){
            event.preventDefault();
            $(this).parent().next(".comment-reply").fadeToggle();
        })
 
        $(".content-markdown").each(function(){
            var content = $(this).text();
            var markedContent = marked(content);
            $(this).html(markedContent)
        })

        $(".post-detail-item img").each(function() {
            $(this).addClass("img-responsive");
        })

        var titleInput = $("#id_title");

        function setTitle(value) {        
            $("#preview-title").text(value);
        }

        setTitle(titleInput.val())

        titleInput.keyup(function() {
            var newTitle = $(this).val();
            setTitle(newTitle);
        })

        var contentInput = $("#wmd-input-id_content");

        function setContent(value){
            var markedContent = marked(value);
            $("#preview-content").html(markedContent);
            $("#preview-content img").each(function() {
                $(this).addClass("img-responsive");
            })
        }

        setContent(contentInput.val())

        contentInput.keyup(function() {
            var newContent = $(this).val();
                setContent(newContent);
        })
        


    })
