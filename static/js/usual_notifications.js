var notificationSocket = new WebSocket(
    'ws://' + window.location.host +
    '/ws/notifications/');

notificationSocket.onmessage = function(e) {
    var data = JSON.parse(e.data),
    	message = data['message'];
    var href = data['href'];
    var header = data['header'];

    send_notification(header, message, href);
};

function send_notification(title, text, href) {
	var notifications_block = document.getElementById("notifications");

    if (notifications_block.childElementCount == 3 & !document.getElementById("more_notifications_text")) {
    	var notification_block = document.createElement("div"),
    		notification_close = document.createElement("h6"),
	    	notification_close_text = document.createTextNode("×"),
    		notification_title = document.createElement("a"),
    		notification_title_2 = document.createElement("h6"),
	    	notification_title_text = document.createTextNode("Еще одно уведомление"),
	    	hidden_notifications_block = document.getElementById("hidden_notifications_block");

	    notification_block.setAttribute('class', 'notification');
	    notification_block.setAttribute('id', "hidden_notifications");
	    notification_block.style.height = "40px";

	    notification_close.setAttribute('class', 'notification_close');
	    notification_close.setAttribute('onclick', "delete_notification(0, 45, 'hidden_notifications')");
	    notification_close.append(notification_close_text);
	    notification_block.append(notification_close);

	    notification_title_2.setAttribute('id', 'more_notifications_text');
	    notification_title.setAttribute('class', 'notification_title');
	    notification_title.setAttribute('href', '/notifications');
	    notification_title_2.append(notification_title_text);
	    notification_title.append(notification_title_2);
	    notification_block.append(notification_title);

	    hidden_notifications_block.append(notification_block);

	    draw_notification(0, 40, notification_block);
    }
    else if (notifications_block.childElementCount == 3) {
    	var notification_block = document.getElementById("more_notifications_text"),
	    	hidden_notifications_block = document.getElementById("hidden_notifications_block");

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
    else {
    	var notification_block = document.createElement("div"),
	    	notification_title = document.createElement("a"),
	    	notification_title_2 = document.createElement("h6"),
	    	notification_title_text = document.createTextNode(title),
	    	notification_close = document.createElement("h6"),
	    	notification_close_text = document.createTextNode("×"),
	    	notification_hr = document.createElement("hr"),
	    	notification_content = document.createElement("p");

	    if(text.length > 50) {
	    	notification_content_text = document.createTextNode(text.slice(0, 51) + "...");
	    }
	    else {
	    	notification_content_text = document.createTextNode(text);
	    }

	    now = new Date()

	    notification_block.setAttribute('class', 'notification');
	    notification_block.setAttribute('id', now);

	    notification_close.setAttribute('class', 'notification_close');
	    notification_close.setAttribute('onclick', "delete_notification(0, 100, '" + now + "')");
	    notification_close.append(notification_close_text);
	    notification_block.append(notification_close);

	    notification_title.setAttribute('class', 'notification_title');
	    notification_title.setAttribute('href', href);
	    notification_title_2.append(notification_title_text);
	    notification_title.append(notification_title_2);
	    notification_block.append(notification_title);

	    notification_hr.style.margin = "2px 0px";
	    notification_block.append(notification_hr);

	    notification_content.append(notification_content_text);
	    notification_block.append(notification_content);

	    notifications_block.append(notification_block);

	    draw_notification(0, 100, notification_block);
	}
};

function draw_notification(i, height, element) {
	if (i >= height / 2 + 10 + 50) {
		return;
	}
	else if (i > height / 2 + 10) {
		element.style.opacity = (i - height / 2 + 10) / 50;
	}
	else {
		element.style.marginTop =  i * 2 - height + "px";
	}

	setTimeout(draw_notification, 1, i + 1, height, element);
};

function delete_notification(i, height, id) {
	deleted_notification = document.getElementById(id);

	if (i >= height / 2 + 10 + 50) {
		deleted_notification.remove();
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

function showwarning(text) {
	if( $('#warning').css('display') == "none" ) {
		$('#warning-text').text(text)
		$('#warning').show(300)
		$('#disabler').css({'z-index': '1021'})
		$('#warning-text').delay(200).animate({'opacity': '1'}, 300)
		$('#disabler').animate({'opacity': '0.7'}, 300)
        if ($(document).height() > $(window).height()) {
		    var scrollTop = ($('html').scrollTop()) ? $('html').scrollTop() : $('body').scrollTop()
		    $('html').addClass('noscroll').css('top',-scrollTop)
		}
	}
}

function showwarning2(text, clickfunction) {
	if( $('#warning').css('display') == "none" ) {
		$('#warning-text').html(text)
		$('#warning-apply').css('display', 'block')
		$('#warning-apply').attr('onclick', clickfunction)
		$('#disabler').css({'z-index': '1021'})
		$('#warning').show(300)
		$('#warning-text').delay(200).animate({'opacity': '1'}, 300)
		$('#disabler').animate({'opacity': '0.7'}, 300)
        if ($(document).height() > $(window).height()) {
		    var scrollTop = ($('html').scrollTop()) ? $('html').scrollTop() : $('body').scrollTop()
		    $('html').addClass('noscroll').css('top',-scrollTop)
		}
	}
}

function closewarning(text) {
	$('#warning-text').animate({'opacity': '0'}, 300)
	$('#warning').delay(200).hide(300)
	$('#disabler').animate({'opacity': '0'}, 300)
	$('#disabler').animate({'z-index': '0'}, 300)
    var scrollTop = parseInt($('html').css('top'))
		$('html').removeClass('noscroll')
		$('html,body').scrollTop(-scrollTop)
}