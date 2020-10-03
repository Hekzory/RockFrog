var commentsurl = '/manage_comments/'

function createcomment(postid) {
    var csrftoken = $('input[name="csrfmiddlewaretoken"]').val()
    
    $.ajax({
        url : commentsurl,
        type : "POST",
        data : {
        	'action': 'create_comment',
        	'articleid': postid,
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
            else if( data != 'long' )
            {	
            	data = JSON.parse(data)
	            $('#comment' + postid + 'input').val('')
	            $('#post' + postid + 'commenticon').text(parseInt($('#post' + postid + 'commenticon').text()) + 1)
	            $('#post' + postid + 'commentcount').text(parseInt($('#post' + postid + 'commentcount').text()) + 1)
	            auto_grow(document.getElementById('comment' + postid + 'input'))
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
        url : commentsurl,
        type : "POST",
        data : {
        	'action': 'edit_comment',
        	'commentid': commentid,
            'text': $('#comment' + postid + 'input').val(),
            'csrfmiddlewaretoken': csrftoken
        },

        success : function(data) {
        	// console.log(data)
			if( data == 'empty' )
            {
                showwarning('Пустое поле')
            }
            else if( data == 'Ok' )
            {	
            	$('#comment' + commentid + 'text').text($('#comment' + postid + 'input').val())
	            $('#comment' + postid + 'input').val('')      
	            closecomment(postid)  	
            }
        },
    })
    
}

function deletecomment(commentid, postid) {
    var csrftoken = $('input[name="csrfmiddlewaretoken"]').val()
    
    $.ajax({
        url : commentsurl,
        type : "POST",
        data : {
        	'action': 'delete_comment',
            'commentid': commentid,
            'csrfmiddlewaretoken': csrftoken
        },

        success : function(data) {
        	// console.log(data)
			if( data == 'Ok' )
            {	            	
        	    $('#post' + postid + 'commenticon').text(parseInt($('#post' + postid + 'commenticon').text()) - 1 - $('#comment' + commentid + 'children').children().length / 2)
	            $('#post' + postid + 'commentcount').text(parseInt($('#post' + postid + 'commentcount').text()) - 1 - $('#comment' + commentid + 'children').children().length / 2)
				closecomment(postid)

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
            else if( data == 'is_deleted' )
            {
				closecomment(postid)

	            $('#comment' + commentid).html('<div class="text2 solid">Комментарий удален</div><hr>')          	
            }
        },
    })
    
}

function answercomment(commentid, postid, name) {
	closecomment(postid)
	$('#comment' + postid + 'input').attr('answering', commentid) 

	$('#comment' + postid + 'answertext').text('Ответить ' + name)
	$('#comment' + postid + 'answertext').removeClass('hidden')
	$('#post' + postid + 'inputgroupappend').removeClass('hidden')
	$('#post' + postid + 'inputgroup').addClass('input-group')

	$('#comment' + postid + 'answer').removeClass('hidden')
	$('#comment' + postid + 'input').focus()
}

function closecomment(postid) {
	$('#comment' + postid + 'input').attr('answering', '') 
	$('#comment' + postid + 'input').attr('editing', '') 

	$('#comment' + postid + 'answertext').addClass('hidden')
	$('#post' + postid + 'inputgroupappend').addClass('hidden')
	$('#post' + postid + 'inputgroup').removeClass('input-group')

	$('#comment' + postid + 'buttonsend').removeClass('hidden')
	$('#comment' + postid + 'buttonedit').addClass('hidden')
	$('#comment' + postid + 'input').val('')

	update_symbols('post' + postid + 'commentssymbols', 'comment' + postid + 'input', 750)
	auto_grow(document.getElementById('comment' + postid + 'input'))
}

function closeanswercomment(postid) {
	$('#comment' + postid + 'input').attr('answering', '')   
	$('#comment' + postid + 'answer').addClass('hidden')
}

function showeditcomment(commentid, postid) {
	$('#comment' + postid + 'input').attr('editing', commentid) 

	$('#comment' + postid + 'answertext').text('Редактирование') 
	$('#comment' + postid + 'answertext').removeClass('hidden')
	$('#post' + postid + 'inputgroupappend').removeClass('hidden')
	$('#post' + postid + 'inputgroup').addClass('input-group')


	$('#comment' + postid + 'input').val($('#comment' + commentid + 'text').text())	

	$('#comment' + postid + 'buttonsend').addClass('hidden')
	$('#comment' + postid + 'buttonedit').removeClass('hidden')

	$('#comment' + postid + 'input').focus()
	update_symbols('post' + postid + 'commentssymbols', 'comment' + postid + 'input', 750)
	auto_grow(document.getElementById('comment' + postid + 'input'))
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
	third_wrapper.css('width', 'calc(100% - 50px)')
	second_wrapper.append(third_wrapper)

	fourth_wrapper = $('<div>')
	fourth_wrapper.addClass('inline-wrapper')
	fourth_wrapper.css('margin-bottom', '-15px')
	third_wrapper.append(fourth_wrapper)	

	author_wrapper = $('<div>')
	author_wrapper.addClass('inline-wrapper')	

	author_text = $('<div>')
	author_text.addClass('text3')
	author_text.css({'overflow': 'auto', 'white-space': 'nowrap'})
	author_wrapper.append(author_text)

	author_link = $('<a>')
	author_link.addClass('link1')
	author_link.attr({'href': '/profile/' + author + '/'})
	author_link.css({'display': 'inline'})
	author_link.text(author)
	author_text.append(author_link)

	reply_icon = $('<i>')
	reply_icon.addClass('material-icons mirrorX icon3 pointer grey-color')
	reply_icon.attr('onclick', 'answercomment(' + commentid + ',' + postid + ', "себе")')
	reply_icon.attr('title', 'ответить')
	reply_icon.text('reply')
	author_wrapper.append(reply_icon)

	fourth_wrapper.append(author_wrapper)
	
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

	pubdate_wrapper = $('<div>')
	pubdate_wrapper.addClass('inline-wrapper')	

	edit_icon = $('<i>')
	edit_icon.addClass('material-icons icon3 pointer grey-color')
	edit_icon.attr('onclick', 'showeditcomment(' + commentid + ',' + postid + ')')
	edit_icon.text('edit')
	pubdate_wrapper.append(edit_icon)

	delete_icon = $('<i>')
	delete_icon.addClass('material-icons icon3 pointer grey-color')
	delete_icon.attr('onclick', 'deletecomment(' + commentid + ',' + postid + ')')	
	delete_icon.text('delete')
	pubdate_wrapper.append(delete_icon)	

	pubdate_text = $('<div>')
	pubdate_text.addClass('text3')
	pubdate_text.text('только что')
	pubdate_wrapper.append(pubdate_text)

	fourth_wrapper.append(pubdate_wrapper)	

	fifth_wrapper = $('<div>')
	fifth_wrapper.addClass('inline-wrapper')
	third_wrapper.append(fifth_wrapper)

	comment_text = $('<div>')
	comment_text.css({'width': 'calc(100% - 100px)', 'word-wrap': 'break-word'})
	comment_text.addClass('text2')
	comment_text.attr('id', 'comment' + commentid + 'text')
	comment_text.text(text)
	fifth_wrapper.append(comment_text)

	plus_minus_wrapper = $('<div>')
	plus_minus_wrapper.css({'display': 'flex', 'margin-top': '10px', 'text-align': 'center', 'margin-bottom': '-10px'})

	plus_minus_wrapper_2 = $('<div>')
	plus_minus_wrapper_2.css({'display': 'flex', 'margin': 'auto'})

	pluses_count = $('<div>')
	pluses_count.attr('id', 'plus_c' + commentid)
	pluses_count.addClass('text3')
	pluses_count.text('0')
	plus_minus_wrapper_2.append(pluses_count)

	plus_icon = $('<i>')
	plus_icon.attr('id', 'plusicon_c' + commentid)
	plus_icon.addClass('material-icons icon3 pointer grey-color-1')
	plus_icon.attr('title', 'Вы не можете оценивать собственный комментарий')	
	plus_icon.text('thumb_up')
	plus_minus_wrapper_2.append(plus_icon)	

	minus_icon = $('<i>')
	minus_icon.attr('id', 'minusicon_c' + commentid)
	minus_icon.addClass('material-icons icon3 pointer grey-color-1')
	plus_icon.attr('title', 'Вы не можете оценивать собственный комментарий')	
	minus_icon.text('thumb_down')
	plus_minus_wrapper_2.append(minus_icon)	

	minuses_count = $('<div>')
	minuses_count.attr('id', 'minuses_c' + commentid)
	minuses_count.addClass('text3')
	minuses_count.text('0')
	plus_minus_wrapper_2.append(minuses_count)

	plus_minus_wrapper.append(plus_minus_wrapper_2)
	fifth_wrapper.append(plus_minus_wrapper)

	wrapper.append($('<hr>'))	

	$('#' + locationid).append(wrapper)

	children_wrapper = $('<div>')
	children_wrapper.attr('id', 'comment' + commentid + 'children')
	children_wrapper.css('margin-left', '40px')
	$('#' + locationid).append(children_wrapper)

	wrapper.show(200)
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

function plus_minus_c(commentid, action) {
    var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
    commentid = parseInt(commentid)

    $.ajax({
        url : "/manage_comments/",
        type : "POST",
        data : {
            'action': 'plus_minus',
            'type': action,
            'commentid': commentid,
            'csrfmiddlewaretoken': csrftoken
        },

        success : function(data) {
            // console.log('Ok')

            $('#plusicon_c' + commentid).removeClass('grey-color')
            $('#minusicon_c' + commentid).removeClass('grey-color')

            if (action == 'plus')
            {
                $('#plus_c' + commentid).text(parseInt($('#plus_c' + commentid).text()) + 1)                
                $('#plusicon_c' + commentid).addClass('green-color')

                $('#plusicon_c' + commentid).attr('onclick', "plus_minus_c('" + commentid + "', 'remove_plus')")
                $('#minusicon_c' + commentid).attr('onclick', "plus_minus_c('" + commentid + "', 'minusminus')")
            }
            else if (action == 'minus')
            {
                $('#minus_c' + commentid).text(parseInt($('#minus_c' + commentid).text()) + 1)
                $('#minusicon_c' + commentid).addClass('red-color')

                $('#plusicon_c' + commentid).attr('onclick', "plus_minus_c('" + commentid + "', 'plusplus')")
                $('#minusicon_c' + commentid).attr('onclick', "plus_minus_c('" + commentid + "', 'remove_minus')")
            }
            else if (action == 'plusplus')
            {
                $('#plus_c' + commentid).text(parseInt($('#plus_c' + commentid).text()) + 1)
                $('#minus_c' + commentid).text(parseInt($('#minus_c' + commentid).text()) - 1)

                $('#plusicon_c' + commentid).addClass('green-color')
                $('#minusicon_c' + commentid).removeClass('red-color')
                $('#minusicon_c' + commentid).addClass('grey-color')

                $('#plusicon_c' + commentid).attr('onclick', "plus_minus_c('" + commentid + "', 'remove_plus')")
                $('#minusicon_c' + commentid).attr('onclick', "plus_minus_c('" + commentid + "', 'minusminus')")
            }
            else if (action == 'minusminus')
            {
                $('#minus_c' + commentid).text(parseInt($('#minus_c' + commentid).text()) + 1)
                $('#plus_c' + commentid).text(parseInt($('#plus_c' + commentid).text()) - 1)

                $('#plusicon_c' + commentid).removeClass('green-color')
                $('#plusicon_c' + commentid).addClass('grey-color')
                $('#minusicon_c' + commentid).addClass('red-color')

                $('#plusicon_c' + commentid).attr('onclick', "plus_minus_c('" + commentid + "', 'plusplus')")
                $('#minusicon_c' + commentid).attr('onclick', "plus_minus_c('" + commentid + "', 'remove_minus')")
            }
            else if (action == 'remove_plus')
            {
                $('#plus_c' + commentid).text(parseInt($('#plus_c' + commentid).text()) - 1)
                $('#plusicon_c' + commentid).removeClass('green-color')
                $('#plusicon_c' + commentid).addClass('grey-color')

                $('#plusicon_c' + commentid).attr('onclick', "plus_minus_c('" + commentid + "', 'plus')")
                $('#minusicon_c' + commentid).attr('onclick', "plus_minus_c('" + commentid + "', 'minus')")
            }
            else if (action == 'remove_minus')
            {
                $('#minus_c' + commentid).text(parseInt($('#minus_c' + commentid).text()) - 1)
                $('#minusicon_c' + commentid).removeClass('red-color')
                $('#minusicon_c' + commentid).addClass('grey-color')

                $('#plusicon_c' + commentid).attr('onclick', "plus_minus_c('" + commentid + "', 'plus')")
                $('#minusicon_c' + commentid).attr('onclick', "plus_minus_c('" + commentid + "', 'minus')")
            }
        },
    });
}