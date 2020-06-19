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

function edit_message(message_id) {
    var currentMessage = $("#"+message_id).children()[1].textContent;
    $("#id_text").val(currentMessage);
    $("#send").hide();
    $("#save_message").show();
    $("#cancel_edit").show();
    $("#current_edit").val(message_id);
    //document.querySelector('#username').text;
}

function cancel_edit() {
    $("#current_edit").val(-1);
    $("#id_text").val("");
    $("#send").show();
    $("#save_message").hide();
    $("#cancel_edit").hide();
    //document.querySelector('#username').text;
}

function save_edit() {
    var message_id = $('#current_edit').val();
    var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
    var currentMessage = $("#id_text").val();
    $.ajax({
        url : "/conversations/edit_message",
        type : "POST",
        data : {
            'message' : currentMessage,
            'message_id' : message_id,
        	'csrfmiddlewaretoken': csrftoken,
        },

        success : function(data) {
			send_edit_message(message_id);
        },
    });
    $("#id_text").val("");
    $("#send").show();
    $("#save_message").hide();
    $("#cancel_edit").hide();
}