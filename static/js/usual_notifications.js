var notificationSocket = new WebSocket(
    'ws://' + window.location.host +
    '/ws/notifications/');

notificationSocket.onmessage = function(e) {
    var data = JSON.parse(e.data);
    var message = data['message'];

    var notification_block = document.createElement("div"),
    	notifications_block = document.getElementById("notifications"),
    	notification_title = document.createElement("h6"),
    	notification_title_text = document.createTextNode("Новое сообщение"),
    	notification_hr = document.createElement("hr"),
    	notification_content = document.createElement("div"),
    	notification_content_text = document.createTextNode("В чате написали: " + message);

    notification_block.setAttribute('class', 'notification');

    notification_title.appendChild(notification_title_text);
    notification_block.appendChild(notification_title);

    notification_block.appendChild(notification_hr);

    notification_content.appendChild(notification_content_text);
    notification_block.appendChild(notification_content);

    notifications_block.appendChild(notification_block);

	let start = Date.now();

	let timer = setInterval(function() {
	  	let timePassed = Date.now() - start;

	 	if (timePassed > 3500) {
	    	clearInterval(timer);
	   		return;
	  	}

	 	draw_notification(timePassed);
	}, 1);

	function draw_notification(timePassed) {
		if (timePassed >= 3497) {
			notifications_block.removeChild(notification_block);
		}
		if (timePassed >= 3250) {
			notification_block.style.opacity = (3500 - timePassed) / 250;
		}
		else {
			notification_block.style.opacity = timePassed / 250;
		}	  	
	}

	/*alert("New notification got - "+message);*/
};

notificationSocket.onclose = function(e) {
    console.error('Произошла ошибка. Пожалуйста, перезагрузите страницу для продолжения работы. Если ошибка повторяется - сообщите об этом администраторам');
};