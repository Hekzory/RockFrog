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
			show_item(data, item_id);
        },
    });
}

function show_item(data, item_id) {
        if (data["response"] == "ok") {
                window.currentItem = {
                  name: data['item_name'],
                  level: data['item_level'],
                  maxlevel: data['item_maxlevel'],
                  collected_cards: data["item_collected_cards"],
                  points_per_level: data['points_per_level'],
                  next_level_desc: data['next_level_description'],
                  upgradable_stats: data['improvable_stats_list']
                };
			    var header_html = "<h5 class='card-title'>"+data["item_name"]+"</h5>";
			    var description_html = "<p class='card-text'>"+data["item_description"]+"</p>";
			    var content = header_html+description_html;
			    $("#item-body").html(content);
			    var main_section = '<div class="card-body" id="item-body">'+$("#item-body").html()+'</div>';
			    var add_info_start = '<ul class="list-group list-group-flush">';
                var add_info_end = "</ul>";
                var add_info_rarity = '<li class="list-group-item text-center">'+data['item_rarity']+'</li>';
                var add_info_level = data["item_level"];
                var add_info_maxlevel = data["item_maxlevel"];
                var collected_cards = data["item_collected_cards"];
                var points_per_level = data['points_per_level'];
                var add_info_upgrades_info = '<li class="list-group-item text-center"><div onclick="levels_info_item('+item_id+');" class="btn btn-success">Характеристики</div></li>';
                if (add_info_level != add_info_maxlevel) {
                    var add_info_progress = `<li class="list-group-item text-center"><div class="text-center mb-3"><b>Прогресс:</b> `+collected_cards+`/`+((add_info_level+1)*points_per_level)+`</div>
                        <div class="row">
                        <span class="col-sm-3 h5 font-weight-bold">`+add_info_level+`</span>
                        <div class="col-sm-6">
                    <div class="progress my-1"><div class="progress-bar" role="progressbar" aria-valuenow="`+collected_cards+`" aria-valuemin="0" aria-valuemax="25" style="width:`+(collected_cards/((add_info_level+1)*points_per_level)*100)+`%;"></div>
                    </div>
                        </div>
                        <span class="col-sm-3 h5 font-weight-bold">`+(add_info_level+1)+`</span>
                      </div>
                    </li>`;
                } else {
                    var add_info_progress = `<li class="list-group-item text-center"><div class="text-center mb-3"><b>Свободных карточек: `+collected_cards+`</b></div>
                        <div class="row">
                        <span class="col-sm-3 h5 font-weight-bold">`+add_info_level+`</span>
                        <div class="col-sm-6">
                    <div class="progress my-1"><div class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar" aria-valuenow="`+collected_cards+`" aria-valuemin="0" aria-valuemax="25" style="width:100%;"></div>
                    </div>
                        </div>
                        <span class="col-sm-3 font-weight-bold"><b>MAX</b></span>
                      </div>
                    </li>`;
                }
                if ((collected_cards >= (add_info_level+1)*points_per_level) && add_info_level < add_info_maxlevel) {
                    var add_info_upgrade_level_button = '<li class="list-group-item text-center"><div onclick="upgrade_item('+item_id+');" class="btn btn-primary">Повысить уровень</div></li>';
                    var content = main_section+add_info_start+add_info_rarity+add_info_progress+add_info_upgrade_level_button+add_info_upgrades_info+add_info_end;
                } else {
                    var content = main_section+add_info_start+add_info_rarity+add_info_progress+add_info_upgrades_info+add_info_end;
                }
                $("#item-card").html(content);
		}
}

function upgrade_item(item_id) {
    var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url : "/inventory/increase_item_level/",
        type : "POST",
        data : {
            'item_id' : item_id,
        	'csrfmiddlewaretoken': csrftoken,
        },

        success : function(data) {
			show_item(data, item_id);
        },
    });
}

function levels_info_item(item_id) {
    console.log(item_id);
    $('#level-info-modal-title').text(window.currentItem.name+" - Характеристики");
    $('#level-info-modal-progress').width((window.currentItem.collected_cards/((window.currentItem.level+1)*window.currentItem.points_per_level)*100)+"%");
    $('#level-info-modal-level').text(window.currentItem.level);
    if (window.currentItem.level == window.currentItem.maxlevel) {
        $('#level-info-modal-nextlevel').text('MAX');
    } else {
        $('#level-info-modal-nextlevel').text(window.currentItem.level+1);
    }
    $('#level-info-modal-next-upgrade').text(window.currentItem.next_level_desc);
    var upgradable_stats_html = '';
    for (var i = 0; i < window.currentItem.upgradable_stats.length; i++) {
        upgradable_stats_html += '<div class="col-6">'+window.currentItem.upgradable_stats[i][0] + '</div> <div class="col-6">' + window.currentItem.upgradable_stats[i][1] + '</div>';
    }
    $('#level-info-modal-stats').html(upgradable_stats_html);
    $('#level-info-modal').modal();
}