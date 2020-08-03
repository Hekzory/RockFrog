function switch_show_viewed_settings() {
	var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();

	$.ajax({
        url : "/manage_settings/",
        type : "POST",
        data : {            
            'action': 'switch_show_viewed_settings',
            'csrfmiddlewaretoken': csrftoken,
        },

        success : function(json) {
        	location.reload(true);	
        },
    });
}

function set_default_section(section) {
    var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();

    $.ajax({
        url : "/manage_settings/",
        type : "POST",
        data : {
            'action': 'set_default_section',
            'section': section,
            'csrfmiddlewaretoken': csrftoken,
        },

        success : function(json) {
        },
    });
}