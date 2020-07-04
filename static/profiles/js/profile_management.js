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
    $("#blacklist_button").text("Удалить из чёрного списка");
    $("#blacklist_button").attr('onclick', "unblock_user("+id+")");
}

function unblock_user(id) {
    var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url : '/profile/unblock/',
        type : 'POST',
        data : {
            'user_id' : id,
            'csrfmiddlewaretoken' : csrftoken,
        },

        success : function(data) {
			change_to_block(id);
        },
    });
}


function change_to_block(id) {
    $("#blacklist_button").text("Добавить в чёрный список");
    $("#blacklist_button").attr('onclick', "block_user("+id+")");
}

function delete_from_blacklist(id) {
    var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url : "/profile/unblock/",
        type : "POST",
        data : {
            'user_id' : id,
        	'csrfmiddlewaretoken': csrftoken,
        },

        success : function(data) {
			delete_unblock_button(id);
        },
    });
}

function delete_unblock_button(id) {
    $("#blacklist-user-"+id).remove();
    if ($("#blacklist-table").children().length == 0) {
    $("#blacklist-table").html('<tr><td>Чёрный список пуст.</td></tr>');
    }
}

function toggle_personal_message_notifications() {
    var current_state = document.getElementById('id_personal_message_notifications').checked;
    var type = 'personal_message_notifications';
    var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url : "/profile/edit_notifications/",
        type : "POST",
        data : {
            'current_state' : current_state,
            'type' : type,
        	'csrfmiddlewaretoken': csrftoken,
        },
    });
}

function toggle_accepted_to_group_notifications() {
    var current_state = document.getElementById('id_accepted_to_group_notifications').checked;
    var type = 'accepted_to_group_notifications';
    var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url : "/profile/edit_notifications/",
        type : "POST",
        data : {
            'current_state' : current_state,
            'type' : type,
        	'csrfmiddlewaretoken': csrftoken,
        },
    });
}

function toggle_post_published_notifications() {
    var current_state = document.getElementById('id_post_published_notifications').checked;
    var type = 'post_published_notifications';
    var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url : "/profile/edit_notifications/",
        type : "POST",
        data : {
            'current_state' : current_state,
            'type' : type,
        	'csrfmiddlewaretoken': csrftoken,
        },
    });
}

$(function() {
    $('#id_personal_message_notifications').change(toggle_personal_message_notifications)
    })

$(function() {
    $('#id_accepted_to_group_notifications').change(toggle_accepted_to_group_notifications)
    })

$(function() {
    $('#id_post_published_notifications').change(toggle_post_published_notifications)
    })