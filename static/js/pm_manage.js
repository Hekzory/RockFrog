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
			send_delete_message(message_id);
        },
    });
}