var DLSocket = new WebSocket(
    'ws://' + window.location.host +
    '/ws/dialog_list');

DLSocket.onmessage = function(e) {
    var data = JSON.parse(e.data);
    $.get('/conversations/base_list', function(messages){
            $('#messages').html(messages);
        });
};

DLSocket.onclose = function(e) {
    console.error('Произошла ошибка. Пожалуйста, перезагрузите страницу для продолжения работы. Если ошибка повторяется - сообщите об этом администраторам');
};