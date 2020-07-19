function showitem(item_id, type) {
    var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url : "/inventory/get_item/",
        type : "POST",
        data : {
            'item_id' : item_id,
        	'csrfmiddlewaretoken': csrftoken,
        	'type': type,
        },

        success : function(data) {
			console.log("Got info about item");
			if (data["response"] == "ok") {
			    console.log("Response is ok");
			    var header_html = "<h5 class='card-title'>"+data["item_name"]+"</h5>";
			    var description_html = "<p class='card-text'>"+data["item_description"]+"</p>";
			    var content = header_html+description_html;
			    $("#item-body").html(content);
			    var main_section = '<div class="card-body" id="item-body">'+$("#item-body").html()+'</div>';
			    var add_info_start = '<ul class="list-group list-group-flush">';
                var add_info_end = "</ul>";
                var add_info_rarity = '<li class="list-group-item">Редкость: '+data['item_rarity']+'</li>'
                var content = main_section+add_info_start+add_info_rarity+add_info_end;
                $("#item-card").html(content);
			}
        },
    });
}