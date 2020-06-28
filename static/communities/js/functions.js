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

function createpost(text) {
	if( $('#postarea').val().trim() == '') {
		showwarning('Текст поста не может быть пустым')
	} else {
		showwarning2('Создать пост? <br>' + text, 'document.getElementById("postform").submit()')
	}
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
        	console.log(data);
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
        	'type': 'sendsubrequest',
        	'csrfmiddlewaretoken': csrftoken
        },

        success : function(data) {
        	location.reload(true);
        	console.log(data);
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
		document.getElementById('requestarticles').style.display = 'none'

		$('#articles_button_1').addClass('button0-active')
		$('#articles_button_2').removeClass('button0-active')
		$('#articles_button_3').removeClass('button0-active')
	} else if( name == 2 ) {
		document.getElementById('articles').style.display = 'none'
		document.getElementById('author_request_articles').style.display = 'none'
		document.getElementById('requestarticles').style.display = 'block'

		$('#articles_button_1').removeClass('button0-active')
		$('#articles_button_2').addClass('button0-active')
		$('#articles_button_3').removeClass('button0-active')
	} else if( name == 3 ) {
		document.getElementById('articles').style.display = 'none'
		document.getElementById('requestarticles').style.display = 'none'
		document.getElementById('author_request_articles').style.display = 'block'

		$('#articles_button_1').removeClass('button0-active')
		$('#articles_button_2').removeClass('button0-active')
		$('#articles_button_3').addClass('button0-active')
	}
}

function auto_grow(element) {
    element.style.height = "5px";
    element.style.height = (element.scrollHeight)+"px";
    // console.log($(element).val())
}

function allowarticle(id) {	
	sendajax('allowarticle', id)
	document.getElementById('article' + id).style.display = 'none'
}

function deletearticle(id) {	
	sendajax('deletearticle', id)
	document.getElementById('article' + id).style.display = 'none'
}

function delete_request_article(id) {	
	sendajax('delete_request_article', id)
	document.getElementById('article' + id).style.display = 'none'
}

function showcreate() {
	if( $('#postoptions').css('display') == 'none' ) {
		$('#postplate').css('min-height', '110px');		
		$('#postadditions').css('display', 'block');
		$('#postoptions').css('display', 'block');
		$('#postplate').css('width', 'calc(75% - 5px)');
		$('#postarea').attr('onclick', 'auto_grow(this)');
	} else {
		$('#postplate').css('min-height', '41px');
		$('#postadditions').css('display', 'none');
		$('#postoptions').css('display', 'none');
		$('#postplate').css('width', '100%');
		$('#postarea').attr('onclick', 'showcreate()');
	}	
}

function readfile(input) {
  	if( input.files ) {
	    file = input.files[0]    
	    if( file.type != 'image/png' & file.type != 'image/jpeg' & file.type != 'application/pdf' & file.type != 'text/plain' & file.type != 'application/msword' ) {        
	        showwarning('Такой формат файла недоступен')
	       	files = document.getElementById('postfileinput2').files
			files = Object.values(files).splice(-1,1)	
			document.getElementById('postfileinput2').files = new FileListItem(files)        
	    } else 
	   	if( file.size > 5000000 ) {        
	        showwarning('Файл слишком большой')
	        files = document.getElementById('postfileinput2').files
			files = Object.values(files).splice(-1,1)
			document.getElementById('postfileinput2').files = new FileListItem(files)
	    } else 
	    {
	     	files = Object.values(document.getElementById('postfileinput').files)
	    	newfile = Object.values(document.getElementById('postfileinput2').files)
	    	files = files.concat(newfile)
	    	document.getElementById('postfileinput').files = new FileListItem(files)

	    	if( file.type == 'image/png' || file.type == 'image/jpeg' ) {
		        /*addition = document.getElementById('postaddition1')
		        img = document.createElement('img')
		        img.setAttribute('class', 'medium-img pointer')
		        img.setAttribute('name', file.name)
		        img.setAttribute('onclick', 'postremovefile(this)')
		        addition.append(img)
		        setimage(input, img)
		        */

              	newimg = $('<img>')
              	newdecorator = $('<div>')
              	newicon = $('<i>')

              	$(newimg).attr({'class': 'medium-img', 'name': file.name})
              	$(newdecorator).attr({'class': 'image-decorator'})
              	$(newicon).attr({'class': 'material-icons icon-image-decorator'})
              	$(newicon).text('delete_outline')

              	$(newdecorator).attr({'onclick': 'postremovefile($(this).parent())'})

              	newaddition = $('<div>')
              	$(newaddition).css({'position': 'relative'})

              	$(newdecorator).append(newicon)
              	newaddition.append(newdecorator, newimg)

              	$('#postaddition1').append(newaddition)
              	setimage(input, newimg)
              	
	    	} else {
	    		addition = document.getElementById('postaddition2')
	    		filetag = document.createElement('div')
	    		$(filetag).css({'text-align': 'center'})
	    		$(filetag).attr('class', 'button3 grey')
	    		$(filetag).attr('onclick', 'postremovefile(this)')
                $(filetag).text(cutstring(file.name))
	    		addition.append(filetag)
	    	}
	    }    
	}
}

function readfile2(input) {
  	if( input.files ) {
	    file = input.files[0]    
	    if( file.type != 'image/png' & file.type != 'image/jpeg' & file.type != 'application/pdf' & file.type != 'text/plain' & file.type != 'application/msword' ) {        
	        // showwarning('Такой формат файла недоступен')
	    } else 
	   	if( file.size > 5000000 ) {        
	        // showwarning('Файл слишком большой')
	    } else 
	    {
	     	files = Object.values(document.getElementById('editfileinput').files)
	    	newfile = Object.values(document.getElementById('editfileinput2').files)
	    	files = files.concat(newfile)
	    	document.getElementById('editfileinput').files = new FileListItem(files)
	    	// console.log(document.getElementById('postfileinput').files)

	    	if( file.type == 'image/png' || file.type == 'image/jpeg' ) {
		        /*addition = document.getElementById('editaddition1')
		        img = document.createElement('img')
		        img.setAttribute('class', 'medium-img pointer')
		        img.setAttribute('name', file.name)
		        img.setAttribute('onclick', 'editremovefile(this)')
		        addition.append(img)
		        setimage(input, img)*/

		        newimg = $('<img>')
              	newdecorator = $('<div>')
              	newicon = $('<i>')

              	$(newimg).attr({'class': 'medium-img', 'name': file.name})
              	$(newdecorator).attr({'class': 'image-decorator'})
              	$(newicon).attr({'class': 'material-icons icon-image-decorator'})
              	$(newicon).text('delete_outline')

              	$(newdecorator).attr({'onclick': 'editremovefile($(this).parent())'})

              	newaddition = $('<div>')
              	$(newaddition).css({'position': 'relative'})

              	$(newdecorator).append(newicon)
              	newaddition.append(newdecorator, newimg)

              	$('#editaddition1').append(newaddition)
              	setimage(input, newimg)
	    	} else {
	    		addition = document.getElementById('editaddition2')
	    		filetag = document.createElement('div')
	    		$(filetag).css({'text-align': 'center'})
	    		$(filetag).attr('class', 'button3 grey')
	    		$(filetag).attr('name', file.name)
	    		$(filetag).attr('onclick', 'editremovefile(this)')
                $(filetag).text(cutstring(file.name))
	    		addition.append(filetag)
	    	}
	    }    
	}
}

function FileListItem(a) {
  a = [].slice.call(Array.isArray(a) ? a : arguments)
  for (var c, b = c = a.length, d = !0; b-- && d;) d = a[b] instanceof File
  if (!d) throw new TypeError("expected argument to FileList is File or array of File objects")
  for (b = (new ClipboardEvent("")).clipboardData || new DataTransfer; c--;) b.items.add(a[c])
  return b.files
}

function setimage(input, element) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();
    
    reader.onload = function(e) {
    	element.attr('src', e.target.result)
    }
    
    reader.readAsDataURL(input.files[0]);
  }
}

function postremovefile(element) {
	$(element).hide(300, function(){ $(element).remove(); });
	files = document.getElementById('postfileinput').files
	files = Object.values(files).filter(file => file.name != element.find('img').attr('name'))
	document.getElementById('postfileinput').files = new FileListItem(files)
}

function editremovefile(element) {
	$(element).hide(300, function(){ $(element).remove(); });
	files = document.getElementById('editfileinput').files
	if( $(element).find('img').attr('name') )
	{	
		files = Object.values(files).filter(file => file.name != $(element).find('img').attr('name'))
		document.getElementById('editfileinput').files = new FileListItem(files)		
	}
	else 
	{
		files = Object.values(files).filter(file => file.name != $(element).attr('name'))
		document.getElementById('editfileinput').files = new FileListItem(files)	
	}

}

function editremovefile2(element) {
	$('#editremovedfiles').val($('#editremovedfiles').val() + ' ' + $(element).attr('fileid'))
	$(element).hide(300, function(){ $(element).remove(); });
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

function showfile(url, name='file', current_number=1, source_id='mainimage') {
    if( $('#fileviewer').css('display') == "none" ) {
    	$('#fileviewerimage').attr('src', url)
    	$('#fileviewerlink').attr('href', url)

    	if( current_number > 1 ) {
			$('#fileviewer_left').attr({'onclick': 'swipefile("left", ' + (current_number - 1) + ', "' + source_id + '")'})
			$('#fileviewer_left').css({'visibility': 'visible'})
    	} else {
    		$('#fileviewer_left').css({'visibility': 'hidden'})
    	}

    	if( current_number < $('#' + source_id).children().length ) {
			$('#fileviewer_right').attr({'onclick': 'swipefile("right", ' + (current_number + 1) + ', "' + source_id + '")'})
			$('#fileviewer_right').css({'visibility': 'visible'})
    	} else {
    		$('#fileviewer_right').css({'visibility': 'hidden'})
    	}
    	
    	$('#fileviewerlink').attr('download', name)
    	if( (window.innerWidth - 320 - 80) / (window.innerHeight * 0.8 - 47) > document.getElementById("fileviewerimage").width / document.getElementById("fileviewerimage").height ) {
    		$('#fileviewerimage').attr('class', 'vert-img')
    	} else {
    		$('#fileviewerimage').attr('class', 'hor-img')
    	}
    	$('#fileviewer').show(300)
        $('#disabler').css({'z-index': '1021'}) 
        $('#disabler').animate({'opacity': '0.7'}, 300)   
        if ($(document).height() > $(window).height()) {
		    var scrollTop = ($('html').scrollTop()) ? $('html').scrollTop() : $('body').scrollTop()
		    $('html').addClass('noscroll').css('top',-scrollTop)       
		}        
    } else {
        $('#fileviewer').hide(300)
        $('#disabler').animate({'opacity': '0'}, 100)
        $('#disabler').animate({'z-index': '0'}, 100) 
        var scrollTop = parseInt($('html').css('top'))
			$('html').removeClass('noscroll')
			$('html,body').scrollTop(-scrollTop)
	}
}

function showedit(postid) {
    if( $('#editblock').css('display') == "none" ) {

    	$('#editremovedfiles').val("")

    	$("#editaddition1").empty()
    	$("#editaddition2").empty()
    	$("#editform").attr('action', $("#cururl").attr("cururl") + 'editarticle/' + postid + '/')
    	document.getElementById('editfileinput').files = new FileListItem([])

    	postid = parseInt(postid)
		var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();

		$.ajax({
	      	url : $("#cururl").attr("cururl") + "moreedit/",
	        type : "POST",
	        data : {
	            'type': 'getpost',
	            'data': postid,
	            'csrfmiddlewaretoken': csrftoken
	        },

	        success : function(returned) {
	            result = returned
	            $('#editarea').val(returned)
	            // document.getElementById("editarea").reload(true);
	            // document.getElementById('editarea').innerHTML = returned
	            // console.log(result)
	        },
	    });

		$('#post' + postid + 'addition1').children().each(function(index, elem) {
	        $("#editaddition1").append($(elem).clone())
	    })
	    // $("#editaddition1 img").attr('onclick', 'editremovefile2(this)')
	    $("#editaddition1 .image-decorator").attr('onclick', 'editremovefile2(this.parentElement)')
	    $("#editaddition1 i").text('delete_outline')

		$('#post' + postid + 'addition2').children().each(function(index, elem) {
	        $("#editaddition2").append($(elem).clone())
	    })
	    $("#editaddition2 a").attr({'onclick': 'editremovefile2(this)', 'src': $("#editaddition2 a").attr('href')})
	    $("#editaddition2 a").removeAttr('href')
	    $("#editaddition2 a").removeAttr('download')

        $('#editblock').show(300)
        $('#disabler').css({'z-index': '1021'}) 
        $('#disabler').animate({'opacity': '0.7'}, 300)  
        if ($(document).height() > $(window).height()) {
		    var scrollTop = ($('html').scrollTop()) ? $('html').scrollTop() : $('body').scrollTop()
		    $('html').addClass('noscroll').css('top',-scrollTop)       
		}
	} else {
        $('#editblock').hide(300)
        $('#disabler').animate({'opacity': '0'}, 300)
        $('#disabler').animate({'z-index': '0'}, 300)  
        var scrollTop = parseInt($('html').css('top'))
		$('html').removeClass('noscroll')
		$('html,body').scrollTop(-scrollTop) 
    }
}

function editpost() {
	if( $('#editarea').val().trim() == '') {
		showwarning('Текст поста не может быть пустым')
	} else {
		document.getElementById("editform").submit()
	}
}

function deletepost(id) {
	document.getElementById('delete' + id).click()
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

function swipefile(direction, current_number=1, source_id) {
	f = false
	if( direction == 'left' && $('#' + source_id + ' div:nth-child(' + (current_number) + ')').length) {
		newimage = $('#' + source_id + ' div:nth-child(' + (current_number) + ') img')

		f = true
		url = newimage.attr('src')
		name = newimage.attr('name')

	}
	else if( direction == 'right' && $('#' + source_id + ' div:nth-child(' + (current_number) + ')').length){
		newimage = $('#' + source_id + ' div:nth-child(' + (current_number) + ') img')

		f = true
		url = newimage.attr('src')
		name = newimage.attr('name')
	}

	if( f ) {
		$('#fileviewerimage').attr('src', url)
    	$('#fileviewerlink').attr('href', url)
    	$('#fileviewerlink').attr('download', name)

    	if( current_number > 1 ) {
			$('#fileviewer_left').attr({'onclick': 'swipefile("left", ' + (current_number - 1) + ', "' + source_id + '")'})
			$('#fileviewer_left').css({'visibility': 'visible'})
    	} else {
    		$('#fileviewer_left').css({'visibility': 'hidden'})
    	}

    	if( current_number < $('#' + source_id).children().length ) {
			$('#fileviewer_right').attr({'onclick': 'swipefile("left", ' + (current_number + 1) + ', "' + source_id + '")'})
			$('#fileviewer_right').css({'visibility': 'visible'})
    	} else {
    		$('#fileviewer_right').css({'visibility': 'hidden'})
    	}

    	if( (window.innerWidth - 320 - 80) / (window.innerHeight * 0.8 - 47) > document.getElementById("fileviewerimage").width / document.getElementById("fileviewerimage").height ) {
    		$('#fileviewerimage').attr('class', 'vert-img')
    	} else {
    		$('#fileviewerimage').attr('class', 'hor-img')
    	}
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

function createcomment(postid) {
    var csrftoken = $('input[name="csrfmiddlewaretoken"]').val()
    
    $.ajax({
        url : $("#cururl").attr("cururl") + "createcomment/" + postid + '/',
        type : "POST",
        data : {
            'text': $('#comment' + postid + 'input').val(),
            'reply': $('#comment' + postid + 'input').attr('answering'),
            'csrfmiddlewaretoken': csrftoken
        },

        success : function(data) {
        	// console.log(data)
			if( data == 'empty' )
            {
                showwarning('Пустое поле')
            }
            else
            {	
            	data = JSON.parse(data)
	            $('#comment' + postid + 'input').val('')
	            $('#post' + postid + 'commenticon').text(parseInt($('#post' + postid + 'commenticon').text()) + 1)
	            $('#post' + postid + 'commentcount').text(parseInt($('#post' + postid + 'commentcount').text()) + 1)
	        	showcomments(postid)
	        	closecomment(postid)
	    		insertcomment(data['locationid'], data['avatar'], data['text'], data['author'], data['pubdate'], data['postid'], data['commentid'], data['parentname'])
            }
        },
    })
    
}

function editcomment(postid) {
    var csrftoken = $('input[name="csrfmiddlewaretoken"]').val()

    commentid = $('#comment' + postid + 'input').attr('editing')
    
    $.ajax({
        url : "/groups/editcomment/" + commentid + '/',
        type : "POST",
        data : {
            'text': $('#comment' + postid + 'input').val(),
            'csrfmiddlewaretoken': csrftoken
        },

        success : function(data) {
        	// console.log(data)
			if( data == 'empty' )
            {
                showwarning('Пустое поле')
            }
            else
            {	
            	$('#comment' + commentid + 'text').text($('#comment' + postid + 'input').val())
	            $('#comment' + postid + 'input').val('')      
	            closecomment(postid)  	
            }
        },
    })
    
}

function answercomment(commentid, postid, name) {
	$('#comment' + postid + 'input').attr('answering', commentid) 
	$('#comment' + postid + 'answer').text('Ответ ' + name) 

	$('#comment' + postid + 'answer').removeClass('hidden')
	$('#comment' + postid + 'input').focus()
}

function closecomment(postid) {
	$('#comment' + postid + 'input').attr('answering', '') 
	$('#comment' + postid + 'input').attr('editing', '') 
	$('#comment' + postid + 'answer').addClass('hidden')

	$('#comment' + postid + 'buttonsend').removeClass('hidden')
	$('#comment' + postid + 'buttonedit').addClass('hidden')
	$('#comment' + postid + 'input').val('')
}

function closeanswercomment(postid) {
	$('#comment' + postid + 'input').attr('answering', '')   
	$('#comment' + postid + 'answer').addClass('hidden')


}

function showeditcomment(commentid, postid) {
	$('#comment' + postid + 'input').attr('editing', commentid) 
	$('#comment' + postid + 'answer').text('Редактировать') 
	$('#comment' + postid + 'answer').removeClass('hidden')

	$('#comment' + postid + 'input').val($('#comment' + commentid + 'text').text())

	$('#comment' + postid + 'buttonsend').addClass('hidden')
	$('#comment' + postid + 'buttonedit').removeClass('hidden')

	$('#comment' + postid + 'input').focus()
}

function insertcomment(locationid, avatar_link, text, author, pubdate, postid, commentid, parentname) {

	wrapper = $('<div>')
	wrapper.attr('id', 'comment' + commentid)
	wrapper.hide()

	second_wrapper = $('<div>')
	wrapper.append(second_wrapper)
	second_wrapper.css('display', 'flex')

	avatar = $('<img>')
	avatar.addClass('comment-img')
	avatar.attr({'src': avatar_link, 'alt': ''})
	second_wrapper.append(avatar)

	third_wrapper = $('<div>')
	third_wrapper.css('width', '100%')
	second_wrapper.append(third_wrapper)

	fourth_wrapper = $('<div>')
	fourth_wrapper.addClass('inline-wrapper')
	fourth_wrapper.css('margin-bottom', '-10px')
	third_wrapper.append(fourth_wrapper)	

	author_text = $('<div>')
	author_text.addClass('text3')
	author_text.css({'overflow': 'auto', 'white-space': 'nowrap'})
	fourth_wrapper.append(author_text)

	author_link = $('<a>')
	author_link.addClass('link1')
	author_link.attr({'href': '/profile/' + author + '/'})
	author_link.css({'display': 'inline'})
	author_link.text(author)
	author_text.append(author_link)
	
	if( parentname != '' )
	{	
		answered = $('<div>')
		answered.addClass('text3')
		answered.text('ответил')
		answered.css({'display': 'inline'})
		author_text.append(answered)

		parent_link = $('<a>')
		parent_link.addClass('link1')
		parent_link.attr({'href': '/profile/' + parentname + '/'})
		parent_link.css({'display': 'inline'})
		parent_link.text(parentname)
		author_text.append(parent_link)
	}	

	pubdate_text = $('<div>')
	pubdate_text.addClass('text3')
	pubdate_text.text('только что')
	fourth_wrapper.append(pubdate_text)	

	fifth_wrapper = $('<div>')
	fifth_wrapper.addClass('inline-wrapper')
	third_wrapper.append(fifth_wrapper)

	comment_text = $('<div>')
	comment_text.css('width', 'calc(100% - 50px)')
	comment_text.addClass('text2')
	comment_text.attr('id', 'comment' + commentid + 'text')
	comment_text.text(text)
	fifth_wrapper.append(comment_text)

	edit_icon = $('<i>')
	edit_icon.addClass('material-icons icon-comment pointer')
	edit_icon.attr('onclick', 'showeditcomment(' + commentid + ',' + postid + ')')
	edit_icon.text('edit')
	fifth_wrapper.append(edit_icon)

	delete_icon = $('<i>')
	delete_icon.addClass('material-icons icon-comment pointer')
	delete_icon.attr('onclick', 'deletecomment(' + commentid + ',' + postid + ')')	
	delete_icon.text('delete')
	fifth_wrapper.append(delete_icon)

	reply_icon = $('<i>')
	reply_icon.addClass('material-icons mirrorX icon-comment pointer')
	reply_icon.attr('onclick', 'answercomment(' + commentid + ',' + postid + ', "себе")')
	reply_icon.attr('title', 'ответить')
	reply_icon.text('reply')
	fifth_wrapper.append(reply_icon)

	wrapper.append($('<hr>'))	

	$('#' + locationid).append(wrapper)

	children_wrapper = $('<div>')
	children_wrapper.attr('id', 'comment' + commentid + 'children')
	children_wrapper.css('margin-left', '40px')
	$('#' + locationid).append(children_wrapper)

	wrapper.show(200)
}

function deletecomment(commentid, postid) {
    var csrftoken = $('input[name="csrfmiddlewaretoken"]').val()
    
    $.ajax({
        url : "/groups/deletecomment/" + commentid + '/',
        type : "POST",
        data : {
            'id': commentid,
            'csrfmiddlewaretoken': csrftoken
        },

        success : function(data) {
        	// console.log(data)
			if( data == 'Ok' )
            {	            	
        	    $('#post' + postid + 'commenticon').text(parseInt($('#post' + postid + 'commenticon').text()) - 1 - $('#comment' + commentid + 'children').children().length / 2)
	            $('#post' + postid + 'commentcount').text(parseInt($('#post' + postid + 'commentcount').text()) - 1 - $('#comment' + commentid + 'children').children().length / 2)

	            $('#comment' + commentid + 'children').hide(200)
	            $('#comment' + commentid).hide(200, function() { 
	            	$('#comment' + commentid).remove()
	            	$('#comment' + commentid + 'children').remove() 
		      		if( $('#post' + postid + 'icon-helper').html() == 'keyboard_arrow_down' )
		            {			            	
		            	$('#post' + postid + 'comments').children().slice(0, 2).show(200)		            	
		            }
	        	})
            }
        },
    })
    
}

function showcomments(postid) {
	$('#post' + postid + 'comments').children().show(200)
	$('#post' + postid + 'helper').attr('onclick', 'hidecomments(' + postid + ')')
	$('#post' + postid + 'icon-helper').html('keyboard_arrow_up')
}

function hidecomments(postid) {
	$('#post' + postid + 'comments').children().slice(2).hide(200)
	$('#post' + postid + 'helper').attr('onclick', 'showcomments(' + postid + ')')
	$('#post' + postid + 'icon-helper').html('keyboard_arrow_down')
}
/*

function removeElement(element) {
     element.remove();
}

*/
