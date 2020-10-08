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
            //console.log(data);
            data = JSON.parse(data);

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

function create_micropost(data) {
    posts_content = $("#posts_content");
    post = $("<div>");
    post.addClass("post");

    post_header = $("<div>");
    post_header.addClass("post-header");

    title = $("<a>");
    title.addClass("title");
    title.attr("href", data["post_link"]);
    title.text(data['title']);
    post_header.append(title);

    author = $("<div>");
    author.addClass("author");

    name0 = $("<div>");
    name0.addClass("name");
    name0.text(data["author"]);

    avatar = $("<div>");
    avatar.addClass("avatar");
    avatar_32 = $("<img>");
    avatar_32.addClass("avatar-32");
    avatar_32.attr("src", data["avatar"]);
    avatar.append(avatar_32);

    author.append(name0);
    author.append(avatar);
    post_header.append(author);

    post_content = $("<div>");
    post_content.addClass("post-content");
    post_content.text(data["text"]);

    post_footer = $("<div>");
    post_footer.addClass("post-footer");

    rating_comments = $("<div>");
    rating_comments.addClass("rating-comments");

    rating = $("<div>");
    rating.addClass("rating");

    plus_icon = $("<ion-icon>");
    plus_icon.attr("name", "arrow-up-circle-sharp"); 
    plus_icon.addClass("rating-btn");
    plus_icon.attr("id", "plusicon" + data["id"]);  

    minus_icon = $("<ion-icon>");
    minus_icon.attr("name", "arrow-down-circle-sharp"); 
    minus_icon.addClass("rating-btn");
    minus_icon.attr("id", "minusicon" + data["id"]);  

    if( data["react_status"] == "plus" ) {        
        plus_icon.addClass("grey-icon blue-icon pointer");        
        plus_icon.attr("onclick", "plus_minus('" + data["id"] + "', 'remove_plus')");
        
        minus_icon.addClass("grey-icon pointer");        
        minus_icon.attr("onclick", "plus_minus('" + data["id"] + "', 'minusminus')");   
    } else if( data["react_status"] == "minus" ) {        
        plus_icon.addClass("grey-icon pointer");        
        plus_icon.attr("onclick", "plus_minus('" + data["id"] + "', 'plusplus')");
        
        minus_icon.addClass("grey-icon pointer blue-icon");        
        minus_icon.attr("onclick", "plus_minus('" + data["id"] + "', 'remove_minus')");   
    } else if( data["react_status"] == "no_react" ) {        
        plus_icon.addClass("grey-icon pointer");        
        plus_icon.attr("onclick", "plus_minus('" + data["id"] + "', 'plus')");
        
        minus_icon.addClass("grey-icon pointer");        
        minus_icon.attr("onclick", "plus_minus('" + data["id"] + "', 'minus')");   
    } 

    rating_value = $("<div>");
    rating_value.addClass("rating-count");
    rating_value.attr("id", "rating" + data["id"]);
    rating_value.text(data["rating"]);

    rating.append(plus_icon);
    rating.append(rating_value);
    rating.append(minus_icon);

    comments = $("<a>");
    comments.addClass("comments");
    comments.attr("href", data["post_link"]);

    comment_icon = $("<ion-icon>");
    comment_icon.addClass("comment-icon grey-icon");
    comment_icon.attr("name", "chatbox-sharp");

    comment_count = $("<div>");
    comment_count.addClass("comment-count");
    comment_count.text(data["comment_count"]);    

    comments.append(comment_icon);
    comments.append(comment_count);

    rating_comments.append(rating);
    rating_comments.append(comments);

    secondary_info = $("<div>");
    secondary_info.addClass("secondary-info");
    secondary_info.text(data["pubdate"]);

    read_more = $("<div>");
    read_more.addClass("read-more");
    read_more_btn = $("<a>");
    read_more_btn.addClass("read-more-btn");
    read_more_btn.attr("href", data["post_link"]);
    read_more_btn.text("Читать далее");

    read_more.append(read_more_btn);

    post_footer.append(rating_comments);
    post_footer.append(secondary_info);
    post_footer.append(read_more);

    post.append(post_header);
    post.append(post_content);
    post.append(post_footer);

    posts_content.append(post);
}