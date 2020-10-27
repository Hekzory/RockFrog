var id_of_user_messaging_with = $('#user_messaging').val();
var name_of_user_messaging_with = $('.dialog-name').val();

var PMSocket = new WebSocket(
    'ws://' + window.location.host +
    '/ws/personal_messages/'+id_of_user_messaging_with);

document.getElementById('msg-list').scrollTop = document.getElementById('msg-list').scrollHeight;

PMSocket.onclose = function(e) {
    console.error('Произошла ошибка. Пожалуйста, перезагрузите страницу для продолжения работы. Если ошибка повторяется - сообщите об этом администраторам');
};

PMSocket.onmessage = function(e) {
    var data = JSON.parse(e.data);
    var type = data['type'];
    if (type == "message") {
        var message = data['message'];
        var username = data['username'];
        var datetime = data['datetime'];
        var id = data['message_id'];
        var avatar_url = data['avatar_url'];
        if (username != name_of_user_messaging_with) {
            var res_html = '<div class="pm-dialog-message" id="'+id+'"> \
                                <div class="pm-dialog-message-avatar"> \
                                    <img class="pm-dialog-message-avatar-img" src="'+avatar_url+'"> \
                                </div> \
                                <div class="pm-dialog-message-info"> \
                                    <div class="pm-dialog-message-info-upper"> \
                                        <div class="info-username"> \
                                            '+username+' \
                                        </div> \
                                        <div class="info-settings"> \
                                            <ion-icon name="close-sharp" class="info-settings-icon" onclick="delete_message('+id+')"></ion-icon> \
                                        </div> \
                                    </div> \
                                    <div class="pm-dialog-message-info-text"> \
                                        '+message+' \
                                    </div> \
                                </div> \
                            </div>';
        }
        else {
            var res_html = '<div class="pm-dialog-message" id="'+id+'"> \
                                <div class="pm-dialog-message-avatar"> \
                                    <img class="pm-dialog-message-avatar-img" src="'+avatar_url+'"> \
                                </div> \
                                <div class="pm-dialog-message-info"> \
                                    <div class="pm-dialog-message-info-upper"> \
                                        <div class="info-username"> \
                                            '+username+' \
                                        </div> \
                                    </div> \
                                    <div class="pm-dialog-message-info-text"> \
                                        '+message+' \
                                    </div> \
                                </div> \
                            </div>';
        }
        $('#msg-list').append(res_html);
        var chatlist = document.getElementById('msg-list');
        chatlist.scrollTop = chatlist.scrollHeight;
    }
    if (type == "delete") {
        var id = parseInt(data['message_id'])
        $("#"+id).remove();
    }
    if (type == "edit") {
        var id = parseInt(data['message_id'])
        $("#"+id).children()[1].textContent = data['message'];
    }
};

function send_message(e) {
    var messageInputDom = document.querySelector('#id_text');
    var message = messageInputDom.value;
    PMSocket.send(JSON.stringify({
        'type' : 'message',
        'message': message,
        'user_messaging_with_id': id_of_user_messaging_with
    }));
    messageInputDom.value = '';
};


function delete_message(message_id) {
    var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url : "/conversations/delete_message",
        type : "POST",
        data : {
            'message_id' : message_id,
        	'csrfmiddlewaretoken': csrftoken,
        },

        success : function(data) {
			PMSocket.send(JSON.stringify({
                'type': 'delete',
                'id': message_id,
                'user_messaging_with_id': id_of_user_messaging_with,
            }));
        },
    });
}


document.querySelector('#id_text').focus();
document.querySelector('#id_text').onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter, return
        if ($("#send").is(":visible")) {
            document.querySelector('#send').click();
        }
        else {
            document.querySelector('#save_message').click();
        }
    }
};