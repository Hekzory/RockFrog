function createpost(text) {
	if( $('#postarea').val().trim() == '') {
		showwarning('Текст поста не может быть пустым')
	} else {
		showwarning2('Создать пост? <br>' + text, 'document.getElementById("postform").submit()')
	}
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

function showedit(postid) {
    if( $('#editblock').css('display') == "none" ) {

    	$('#editremovedfiles').val("")

    	$("#editaddition1").empty()
    	$("#editaddition2").empty()
    	$("#edit_articleid").val(postid)
    	document.getElementById('editfileinput').files = new FileListItem([])

    	postid = parseInt(postid)
		var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();

		$.ajax({
	      	url : "/manage_articles/",
	        type : "POST",
	        data : {
	            'action': 'get_post',
	            'articleid': postid,
	            'csrfmiddlewaretoken': csrftoken
	        },

	        success : function(data) {
	        	data = JSON.parse(data)
	            $('#editarea').val(data['text'])
	            if (data['allow_comments'] == 'true')
	            {
	            	$("#edit_allow_comments").prop('checked', true)
	            }
	            else
	            {
	            	$("#edit_allow_comments").prop('checked', false); 
	            }
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
	$.ajax({
        url : "/manage_articles/",
        type : "POST",
        data : {
        	'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
        	'action': 'delete_article',
        	'articleid': id
        },

        success : function(json) {
        	location.reload(true);		
        },
    });
}