var id_of_user_messaging_with = document.querySelector('#user_messaging').value;
var PMSocket = new WebSocket(
    'ws://' + window.location.host +
    '/ws/personal_messages/'+id_of_user_messaging_with);

PMSocket.onmessage = function(e) {
    var data = JSON.parse(e.data);
    var type = data['type']
    if (type == "message") {
        var message = data['message'];
        var username = data['username'];
        var datetime = data['datetime'];
        var id = data['message_id'];
        if (username == document.querySelector('#username').text) {
        var res_html = '  <div class="list-group-item list-group-item-action flex-column align-items-start" id="'+id+'"> \
        <div class="d-flex w-100 justify-content-between"> \
          <h5 class="mb-1">'+username+'</h5> \
          <div> \
          </div> \
          <small>'+datetime+'</small> \
        </div> \
        <p class="mb-1">'+message+'</p> \
        </div>';
        } else {
        var res_html = '  <div class="list-group-item list-group-item-action flex-column align-items-start" id="'+id+'"> \
        <div class="d-flex w-100 justify-content-between"> \
          <h5 class="mb-1">'+username+'</h5> \
          <div> \
          <small><button class="btn btn-link" onclick="delete_message('+id+')">Удалить</button></small> \
          </div> \
          <small>'+datetime+'</small> \
        </div> \
        <p class="mb-1">'+message+'</p> \
        </div>';
        }
        $('#msg-list').append(res_html);
        var chatlist = document.getElementById('msg-list-div');
        chatlist.scrollTop = chatlist.scrollHeight;
    }
    if (type == "delete") {
        var id = parseInt(data['message_id'])
        $("#"+id).remove();
    }
};

PMSocket.onclose = function(e) {
    console.error('Произошла ошибка. Пожалуйста, перезагрузите страницу для продолжения работы. Если ошибка повторяется - сообщите об этом администраторам');
};

var chatlist = document.getElementById('msg-list-div');
chatlist.scrollTop = chatlist.scrollHeight;
document.querySelector('#id_text').focus();
document.querySelector('#id_text').onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#send').click();
    }
};

document.querySelector('#send').onclick = function(e) {
    var messageInputDom = document.querySelector('#id_text');
    var message = messageInputDom.value;
    PMSocket.send(JSON.stringify({
        'type' : 'message',
        'message': message,
        'user_messaging_with_id': id_of_user_messaging_with
    }));
    messageInputDom.value = '';
};

function send_delete_message(id) {
    PMSocket.send(JSON.stringify({
        'type': 'delete',
        'id': id,
        'user_messaging_with': document.querySelector('#username').text,
    }));
}