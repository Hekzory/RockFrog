
var chatSocket = new WebSocket(
    'ws://' + window.location.host +
    '/ws/chat/');

chatSocket.onmessage = function(e) {
    var data = JSON.parse(e.data);
    var message = data['message'];
    document.querySelector('#msg-list').value += (message + '\n');
    $('#msg-list').append('<li class="text-left list-group-item">'+message+' </li>');
    console.log("GOT", message);
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

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
