function sendajax(type, data) {
    var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url : $("#cururl").attr("cururl") + "moreedit/",
        type : "POST",
        data : {
            'type': type,
            'data': data,
            'csrfmiddlewaretoken': csrftoken
        },

        success : function(returned) {
            result = returned
            // console.log(result)
        },
    });
}

function subscribe() {
	var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();

	$.ajax({
        url : $("#cururl").attr("cururl") + "subscribe/",
        type : "POST",
        data : {'csrfmiddlewaretoken': csrftoken},

        success : function(json) {
        	location.reload(true);
        	document.getElementById("sub_button").innerHTML = "Отписаться";
			document.getElementById("sub_button").setAttribute("onclick","unsubscribe()");			
        },
    });
}

function unsubscribe() {
	var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();

	$.ajax({
        url : $("#cururl").attr("cururl") + "unsubscribe/",
        type : "POST",
        data : {'csrfmiddlewaretoken': csrftoken},

        success : function(json) {
        	location.reload(true);
        	document.getElementById("sub_button").innerHTML = "Подписаться";
			document.getElementById("sub_button").setAttribute("onclick","subscribe()");			
        },
    });
}

function setlike(articleid) {
	var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
	articleid = parseInt(articleid)

	$.ajax({
        url : $("#cururl").attr("cururl") + "like/" + articleid + "/",
        type : "POST",
        data : {
        	'articleid': articleid,
        	'csrfmiddlewaretoken': csrftoken
        },

        success : function(json) {
        	document.getElementById("like" + articleid).innerHTML = "favorite";
			document.getElementById("like" + articleid).setAttribute("onclick","removelike(" + articleid + ")");
			$('#like' + articleid).parent().find('div').text(parseInt($('#like' + articleid).parent().find('div').text()) + 1)
        },
    });
}

function removelike(articleid) {
	var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
	articleid = parseInt(articleid)

	$.ajax({
        url : $("#cururl").attr("cururl") + "removelike/" + articleid + "/",
        type : "POST",
        data : {
        	'articleid': articleid,
        	'csrfmiddlewaretoken': csrftoken
        },

        success : function(json) {
        	document.getElementById("like" + articleid).innerHTML = "favorite_border";
			document.getElementById("like" + articleid).setAttribute("onclick","setlike(" + articleid + ")");
			$('#like' + articleid).parent().find('div').text(parseInt($('#like' + articleid).parent().find('div').text()) - 1)
        },
    });
}

function show(id, button) {
	el = document.getElementById(id);
	el.style.display = "block";
	button.setAttribute("onclick", "hide('" + id + "', this)");
	button.innerHTML = "Скрыть";
}

function hide(id, button) {
	el = document.getElementById(id);
	el.style.display = "none";
	button.setAttribute("onclick", "show('" + id + "', this)");
	button.innerHTML = "Открыть";
}

function allowsub(userid) {
	var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
	userid = parseInt(userid)

	$.ajax({
        url : $("#cururl").attr("cururl") + "edit/moreedit/",
        type : "POST",
        data : {
        	'type': 'allowsub',
        	'userid': userid,
        	'csrfmiddlewaretoken': csrftoken
        },

        success : function(data) {
        	console.log(data);
        	document.getElementById('sub' + userid).style.display = 'none';
        },
    });
}

function rejectsub(userid) {
	var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
	userid = parseInt(userid)

	$.ajax({
        url : $("#cururl").attr("cururl") + "edit/moreedit/",
        type : "POST",
        data : {
        	'type': 'rejectsub',
        	'userid': userid,
        	'csrfmiddlewaretoken': csrftoken
        },

        success : function(data) {
        	console.log(data);
        	document.getElementById('sub' + userid).style.display = 'none';
        },
    });
}

function sendsubrequest() {
	var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();

	$.ajax({
        url : $("#cururl").attr("cururl") + "edit/moreedit/",
        type : "POST",
        data : {
        	'type': 'sendsubrequest',
        	'csrfmiddlewaretoken': csrftoken
        },

        success : function(data) {
        	location.reload(true);
        	// console.log(data);
        	document.getElementById('sub_button').innerHTML = 'Отозвать заявку';
        	document.getElementById('sub_button').setAttribute('onclick', 'cancelsubrequest()');        	
        },
    });
}

function cancelsubrequest() {
	var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();

	$.ajax({
        url : $("#cururl").attr("cururl") + "edit/moreedit/",
        type : "POST",
        data : {
        	'type': 'cancelsubrequest',
        	'csrfmiddlewaretoken': csrftoken
        },

        success : function(data) {
        	location.reload(true);
        	// console.log(data);
        	document.getElementById('sub_button').innerHTML = 'Подать заявку';
        	document.getElementById('sub_button').setAttribute('onclick', 'sendsubrequest()');        	
        },
    });
}

function showarticles(name) {
	if( name == 1 ) {
		location.reload(true)
		document.getElementById('articles').style.display = 'block'
		document.getElementById('author_request_articles').style.display = 'none'
		document.getElementById('request_articles').style.display = 'none'

		$('#articles_button_1').addClass('button0-active')
		$('#articles_button_2').removeClass('button0-active')
		$('#articles_button_3').removeClass('button0-active')
	} else if( name == 2 ) {
		document.getElementById('articles').style.display = 'none'
		document.getElementById('author_request_articles').style.display = 'none'
		document.getElementById('request_articles').style.display = 'block'

		$('#articles_button_1').removeClass('button0-active')
		$('#articles_button_2').addClass('button0-active')
		$('#articles_button_3').removeClass('button0-active')
	} else if( name == 3 ) {
		document.getElementById('articles').style.display = 'none'
		document.getElementById('request_articles').style.display = 'none'
		document.getElementById('author_request_articles').style.display = 'block'

		$('#articles_button_1').removeClass('button0-active')
		$('#articles_button_2').removeClass('button0-active')
		$('#articles_button_3').addClass('button0-active')
	}
}

function allowarticle(id) {	
	sendajax('allowarticle', id)
	document.getElementById('request_article' + id).style.display = 'none'
    document.getElementById('author_request_article' + id).style.display = 'none'
}

function deletearticle(id) {	
	sendajax('deletearticle', id)
    document.getElementById('request_article' + id).style.display = 'none'
    document.getElementById('author_request_article' + id).style.display = 'none'
}

function delete_request_article(id) {	
	sendajax('delete_request_article', id)
    document.getElementById('request_article' + id).style.display = 'none'
    document.getElementById('author_request_article' + id).style.display = 'none'
}

function searchlist(id, s) {
	$('#' + id).children().each(function(index, elem) {
		if( !$(elem).attr('name').toLowerCase().includes(s.toLowerCase()) ) {
			$(elem).hide()
		} else {
			$(elem).show()
		}
    })
}

function showgroups(id, button) {
	$('.main_groups_list').hide()
	$('#table_buttons').children().removeClass('button0-active')

	$('#' + id).show()
	$(button).addClass('button0-active')

	$('#main_groups_search').attr('onkeyup', "searchlist('" + id + "', this.value)")
}

function showliked(id) {
	id = parseInt(id)
    if( $('#see_likes').css('display') == "none" ) {
        $('#see_likes').show(300)
        $('#disabler').css({'z-index': '1021'}) 
        $('#disabler').animate({'opacity': '0.7'}, 300)             
    } else {
        $('#see_likes').hide(300)
        $('#disabler').animate({'opacity': '0'}, 300)
        $('#disabler').animate({'z-index': '0'}, 300)   
    }
}

function add_to_collection() {
	file = $('#collectioninput').prop('files')[0]

	if( file.size > 5000000 ) {        
        showwarning('Файл слишком большой')
    } else if( file.type != 'image/png' & file.type != 'image/jpeg' & file.type != 'application/pdf' & file.type != 'text/plain' & file.type != 'application/msword' ) {        
        showwarning('Такой формат файла недоступен')
    } else {
    	$('#collectionform').submit()
    }
}

function delete_from_collection(id) {
	var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
	id = parseInt(id)

	$.ajax({
        url : $("#cururl").attr("cururl") + "moreedit/",
        type : "POST",
        data : {
        	'csrfmiddlewaretoken': csrftoken,
        	'type': 'delete_from_collection',
        	'file': id
        },

        success : function(json) {
        	location.reload(true);		
        },
    });
}

function cutstring(text, val=7) {
    if( text.length > val )
    {
      text = text.slice(0, val) + '...'
    }
    return text
}

function copyLink(text) {
    navigator.clipboard.writeText(window.location.hostname + text)
}

function deleteErrorImage(element) {
	delete_from_collection($(element).parent().attr('fileid'))
}
/*

function removeElement(element) {
     element.remove();
}

*/
