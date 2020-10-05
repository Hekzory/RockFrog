function toggle_personal_message_notifications() {
    var current_state = document.getElementById('id_personal_message_notifications').checked;
    var type = 'personal_message_notifications';
    var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url : "/profile/settings/edit_notifications/",
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
        url : "/profile/settings/edit_notifications/",
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
        url : "/profile/settings/edit_notifications/",
        type : "POST",
        data : {
            'current_state' : current_state,
            'type' : type,
        	'csrfmiddlewaretoken': csrftoken,
        },
    });
}