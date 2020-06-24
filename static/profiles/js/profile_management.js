function block_user(id) {
    var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url : "/profile/block/",
        type : "POST",
        data : {
            'user_id' : id,
        	'csrfmiddlewaretoken': csrftoken,
        },

        success : function(data) {
			change_to_unblock(id);
        },
    });
}

function change_to_unblock(id) {
    $("#blacklist_button").text("Удалить из черного списка");
    $("#blacklist_button").attr('onclick', "unblock_user("+id+")");
}

function unblock_user(id) {
    console.log("Successfully switched to other button");
}