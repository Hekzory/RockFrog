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
    $("#blacklist-table").html('<div class="content-box-text small">Ваш чёрный список пуст.</div>');
    }
}


function change_profile() {
    var birthday = document.getElementById('id_birthday').value;
    var email = document.getElementById('id_email').value;
    var city = document.getElementById('id_city').value;
    var phone = document.getElementById('id_phone').value;
    var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
    var avatar = $('#id_avatar').val();
    $.ajax({
        url : "/profile/edit_profile/",
        type : "POST",
        data : {
            'birthday': birthday,
            'email': email,
            'city': city,
            'phone': phone,
            'type' : 'edit_profile',
        	'csrfmiddlewaretoken': csrftoken,
        },
        success : function(data) {
			if (data["status"] == "ok") {
                $('#id_notification_profile_row').show();
                $('#id_notification_profile').text('Вы успешно изменили профиль.');
			}
			else if (data["status"] == "error") {
			    $('#id_notification_profile_row').show();
			    $('#id_notification_profile').text(data['error']);
			}
        },
    });
    if (avatar) {
        change_avatar();
    }
}

function change_avatar() {
    var avatar = $('#id_avatar').val();
    var avatar_data = new FormData();
    avatar_data.append('avatar', $('#id_avatar')[0].files[0], 'avatar.jpg');
    avatar_data.append('csrfmiddlewaretoken', $('input[name="csrfmiddlewaretoken"]').val());
    $.ajax({
        url : "/profile/change_avatar/",
        type : "POST",
        data : avatar_data,
        success : function(data) {
            $('.main-avatar').attr('src', data['path']);
            $('.menu-profile-img').attr('src', data['path']);
        },
        cache: false,
        processData: false,
        contentType: false,
    });
}