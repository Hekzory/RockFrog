var notificationSocket = new WebSocket(
    'ws://' + window.location.host +
    '/ws/notifications/');

notificationSocket.onmessage = function(e) {
    var data = JSON.parse(e.data);
    var message = data['message'];

    var notification_block = document.createElement("div"),
    	notifications_block = document.getElementById("notifications"),
    	notification_title = document.createElement("h6"),
    	notification_title_text = document.createTextNode("Новое сообщение в чате"),
    	notification_hr = document.createElement("hr"),
    	notification_content = document.createElement("p");

    if(message.length > 50) {    	
    	notification_content_text = document.createTextNode(message.slice(0, 51) + "...");
    }
    else {
    	notification_content_text = document.createTextNode(message);
    }

    notification_block.setAttribute('class', 'notification');

    notification_title.appendChild(notification_title_text);
    notification_block.appendChild(notification_title);

    notification_hr.style.margin = "2px 0px";
    notification_block.appendChild(notification_hr);

    notification_content.appendChild(notification_content_text);
    notification_block.appendChild(notification_content);

    notifications_block.appendChild(notification_block);

    draw_notification(0);

    function draw_notification(i) {
    	if (i == 110) {
			return;
		}
		else if (i > 60) {			
			notification_block.style.opacity = (i - 60) / 50;
		}
		else {
			notification_block.style.marginTop =  (i - 50) * 2 + "px"; 
		}	

		setTimeout(draw_notification, 1, i + 1);
    };

	/*alert("New notification got - "+message);*/
};

notificationSocket.onclose = function(e) {
    console.error('Произошла ошибка. Пожалуйста, перезагрузите страницу для продолжения работы. Если ошибка повторяется - сообщите об этом администраторам');
};