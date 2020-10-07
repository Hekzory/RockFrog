function get_posts(userid, feed) {
    var csrftoken = $('input[name="csrfmiddlewaretoken"]').val()

    $.ajax({
        url : 'get_posts/',
        type : "POST",
        data : {
        	'userid': userid,
            'feed': feed,
            'csrfmiddlewaretoken': csrftoken
        },

        success : function(data) {
            data = JSON.parse(data);
        	//console.log(data);

            $("#posts_content").html("");
            if(feed == 'own') {
                $("#feed_own").addClass('active');
                $("#feed_reacted").removeClass('active');
            } else {
                $("#feed_own").removeClass('active');
                $("#feed_reacted").addClass('active');                
            }

            data.forEach(post => create_micropost(post));
        },
    })  
}

function switch_feed(userid, feed) {
    get_posts(userid, feed);    
}

function create_micropost(post) {
    posts_content = $("#posts_content");
    post = $("<div>");
    post.addClass("post");

    post_header = $("<div>");

    post_content = $("<div>");

    post_footer = $("<div>");
}