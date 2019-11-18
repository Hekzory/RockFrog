
var chatSocket = new WebSocket(
    'ws://' + window.location.host +
    '/ws/chat/');

chatSocket.onmessage = function(e) {
    var data = JSON.parse(e.data);
    var message = data['message'];
    var username = data['username'];
    document.querySelector('#msg-list').value += (username+': '+message + '\n');
    $('#msg-list').append('<li class="text-left list-group-item">'+username+': '+message+' </li>');
    var chatlist = document.getElementById('msg-list-div');
    chatlist.scrollTop = chatlist.scrollHeight;
};

chatSocket.onclose = function(e) {
    console.error('Произошла ошибка. Пожалуйста, перезагрузите страницу для продолжения работы. Если ошибка повторяется - сообщите об этом администраторам');
};

var chatlist = document.getElementById('msg-list-div');
chatlist.scrollTop = chatlist.scrollHeight;
document.querySelector('#chat-msg').focus();
document.querySelector('#chat-msg').onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#send').click();
    }
};

document.querySelector('#send').onclick = function(e) {
    var messageInputDom = document.querySelector('#chat-msg');
    var message = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'message': message
    }));
    messageInputDom.value = '';
};
