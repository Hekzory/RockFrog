
var notificationSocket = new WebSocket(
    'ws://' + window.location.host +
    '/ws/notifications/');

notificationSocket.onmessage = function(e) {
    var data = JSON.parse(e.data);
    var message = data['message'];
    alert("New notification got - "+String(message));
};

notificationSocket.onclose = function(e) {
    console.error('Произошла ошибка. Пожалуйста, перезагрузите страницу для продолжения работы. Если ошибка повторяется - сообщите об этом администраторам');
};
