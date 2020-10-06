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

function toggle_view_for_unreg() {
    var current_state = document.getElementById('id_view_for_unreg').checked;
    var type = 'view_for_unreg';
    var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url : "/profile/settings/edit_privacy/",
        type : "POST",
        data : {
            'current_state' : current_state,
            'type' : type,
        	'csrfmiddlewaretoken': csrftoken,
        },
    });
}

function change_password() {
    var current_password = document.getElementById('id_old_password').value;
    var new_password = document.getElementById('id_new_password').value;
    var confirm_password = document.getElementById('id_confirm_password').value;
    var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url : "/profile/settings/edit_security/",
        type : "POST",
        data : {
            'old_password': current_password,
            'new_password': new_password,
            'confirm_password': confirm_password,
            'type' : 'change_password',
        	'csrfmiddlewaretoken': csrftoken,
        },
        success : function(data) {
			if (data["status"] == "ok") {
			    document.getElementById('id_old_password').value = "";
                document.getElementById('id_new_password').value = "";
                document.getElementById('id_confirm_password').value = "";
                $('#id_notification_password_row').show();
                $('#id_notification_password').text('Пароль был успешно изменён. Авторизуйтесь повторно.');
			}
			else if (data["status"] == "error") {
			    $('#id_notification_password_row').show();
			    $('#id_notification_password').text(data['error']);
			}

        },
    });
}