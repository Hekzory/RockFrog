var notificationSocket = new WebSocket(
    'ws://' + window.location.host +
    '/ws/notifications/');

notificationSocket.onmessage = function(e) {
    var data = JSON.parse(e.data),
    	message = data['message'],
    	notifications_block = document.getElementById("notifications");

    if (notifications_block.childElementCount > 4) {
    	var notification_block = document.getElementById("more_notifications_text");

    	count = notification_block.innerHTML.split(' ').slice(1, 2);

    	if (count == "одно") {
    		notification_block.innerHTML = "<h6>Еще 2 уведомления</h6>"
    	}
    	else {
    		count = +count + 1 
    		if (count % 100 > 20) {
    			if (count % 10 >= 5 || count % 10 == 0) {
    				notification_block.innerHTML = "Еще " + count + " уведомлений";   
    			} 		
    			else if (count % 10 >= 2) {
    				notification_block.innerHTML = "<h6>Еще " + count + " уведомления";
    			} else if (count % 10 == 1) {
    				notification_block.innerHTML = "<h6>Еще " + count + " уведомление";
    			}	
    		}
			else if (count % 100 >= 5 || count % 10 == 0) {
    			notification_block.innerHTML = "Еще " + count + " уведомлений";
    		} else if (count % 10 >= 2) {
    			notification_block.innerHTML = "Еще " + count + " уведомления";
    		} else if (count % 10 == 1) {
    			notification_block.innerHTML = "Еще " + count + " уведомление";
    		}	
    	}
    }
    else if (notifications_block.childElementCount == 4 & !document.getElementById("more_notifications_text")) {
    	var notification_block = document.createElement("div"),
    		notification_close = document.createElement("h6"),
	    	notification_close_text = document.createTextNode("×"),
    		notification_title = document.createElement("h6"),
	    	notification_title_text = document.createTextNode("Еще одно уведомление");

	    now = new Date()

	    notification_block.setAttribute('class', 'notification');
	    notification_block.setAttribute('id', now);
	    notification_block.style.height = "40px";

	    notification_close.setAttribute('class', 'notification_close');
	    notification_close.setAttribute('onclick', "delete_notification(0, 45, '" + now + "')");
	    notification_close.appendChild(notification_close_text);
	    notification_block.appendChild(notification_close);

	    notification_title.setAttribute('onclick', "to_notifications.click()");
	    notification_title.setAttribute('id', 'more_notifications_text');
	    notification_title.setAttribute('class', 'notification_title');
	    notification_title.appendChild(notification_title_text);
	    notification_block.appendChild(notification_title);

	    notifications_block.appendChild(notification_block);

	    draw_notification(0, 40);
    }
    else {
    	var notification_block = document.createElement("div"),
	    	notification_title = document.createElement("h6"),
	    	notification_title_text = document.createTextNode("Новое сообщение в чате"),
	    	notification_close = document.createElement("h6"),
	    	notification_close_text = document.createTextNode("×"),
	    	notification_hr = document.createElement("hr"),
	    	notification_content = document.createElement("p");

	    if(message.length > 50) {    	
	    	notification_content_text = document.createTextNode(message.slice(0, 51) + "...");
	    }
	    else {
	    	notification_content_text = document.createTextNode(message);
	    }

	    now = new Date()

	    notification_block.setAttribute('class', 'notification');
	    notification_block.setAttribute('id', now);	    

	    notification_close.setAttribute('class', 'notification_close');
	    notification_close.setAttribute('onclick', "delete_notification(0, 100, '" + now + "')");
	    notification_close.appendChild(notification_close_text);
	    notification_block.appendChild(notification_close);

	    notification_title.setAttribute('onclick', "to_notifications.click()");
	    notification_title.setAttribute('class', 'notification_title');
	    notification_title.appendChild(notification_title_text);
	    notification_block.appendChild(notification_title);

	    notification_hr.style.margin = "2px 0px";
	    notification_block.appendChild(notification_hr);

	    notification_content.appendChild(notification_content_text);
	    notification_block.appendChild(notification_content);

	    notifications_block.appendChild(notification_block);

	    draw_notification(0, 100);
	}

	function draw_notification(i, height) {
    	if (i >= height / 2 + 10 + 50) {
			return;
		}
		else if (i > height / 2 + 10) {			
			notification_block.style.opacity = (i - height / 2 + 10) / 50;
		}
		else {
			notification_block.style.marginTop =  i * 2 - height + "px"; 
		}	

		setTimeout(draw_notification, 1, i + 1, height);
    };

	/*alert("New notification got - "+message);*/
};

function delete_notification(i, height, id) {
	deleted_notification = document.getElementById(id);

	if (i >= height / 2 + 10 + 50) {	
		notifications_block = document.getElementById("notifications");	
		notifications_block.removeChild(deleted_notification);
		return;
	}
	else if (i > 50) {		
		deleted_notification.style.marginTop =  (60 - i) * 2 + "px"; 			
	}
	else {
		deleted_notification.style.opacity = (50 - i) / 50;
	}	

	setTimeout(delete_notification, 1, i + 1, height, id);
};

notificationSocket.onclose = function(e) {
    console.error('Произошла ошибка. Пожалуйста, перезагрузите страницу для продолжения работы. Если ошибка повторяется - сообщите об этом администраторам');
};