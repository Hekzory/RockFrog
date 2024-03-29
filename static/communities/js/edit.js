function sendajax(type, data) {
    var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();

    $.ajax({
        url :  $("#cururl").attr("cururl") + "edit/moreedit/",
        type : "POST",
        data : {
            'type': type,
            'data': data,
            'csrfmiddlewaretoken': csrftoken
        },

        success : function(returned) {
            // console.log(returned);
            return returned
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

function auto_grow(element) {
    element.style.height = "5px";
    element.style.height = (element.scrollHeight)+"px";
}

function deletegroup() {
	var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();

	$.ajax({
        url : $("#cururl").attr("cururl") + "edit/moreedit/",
        type : "POST",
        data : {
        	'type': 'delete',
        	'csrfmiddlewaretoken': csrftoken
        },

        success : function(data) {
        	// console.log(data)
			document.location.href = '/groups/'
        },
    });
}

function allowarticles() {
    var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
    // console.log($('#allow_articles_selector').val())


    ans = sendajax('allowarticles', $('#allow_articles_selector').val())
    // console.log(ans)
    /*
    if( number == 1 ){
        document.getElementById('allowarticles1').style.display = 'none'
        document.getElementById('allowarticles2').style.display = 'block'
        document.getElementById('allowarticles3').style.display = 'block'
    } else if( number == 2 ){
        document.getElementById('allowarticles2').style.display = 'none'
        document.getElementById('allowarticles1').style.display = 'block'
        document.getElementById('allowarticles3').style.display = 'block'
    } else {
        document.getElementById('allowarticles3').style.display = 'none'
        document.getElementById('allowarticles1').style.display = 'block'
        document.getElementById('allowarticles2').style.display = 'block'
    }
    */
}

function showdelete() {
	document.getElementById('closedelete').style.display = "block"
	document.getElementById('canceldelete').style.display = "block"
	document.getElementById('delete').style.display = "none"
}

function hidedelete() {
	document.getElementById('closedelete').style.display = "none"
	document.getElementById('canceldelete').style.display = "none"
	document.getElementById('delete').style.display = "block"
}

function opengroup() {
	var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();

	$.ajax({
        url :  $("#cururl").attr("cururl") + "edit/moreedit/",
        type : "POST",
        data : {
        	'type': 'public',
        	'csrfmiddlewaretoken': csrftoken
        },

        success : function(data) {
        	// console.log(data);
        	document.getElementById("publicstatus").innerHTML = 'Закрыть';
        	document.getElementById("publicstatus").setAttribute('onclick', "closegroup()");
        },
    });
}

function closegroup() {
	var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();

	$.ajax({
        url :  $("#cururl").attr("cururl") + "edit/moreedit/",
        type : "POST",
        data : {
        	'type': 'public',
        	'csrfmiddlewaretoken': csrftoken
        },

        success : function(data) {
        	// console.log(data);
        	document.getElementById("publicstatus").innerHTML = 'Открыть';
        	document.getElementById("publicstatus").setAttribute('onclick', "opengroup()");
        },
    });
}

function banuser(userid) {
    var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
    userid = parseInt(userid)

    $.ajax({
        url : $("#cururl").attr("cururl") + "edit/moreedit/",
        type : "POST",
        data : {
            'type': 'banuser',
            'userid': userid,
            'csrfmiddlewaretoken': csrftoken
        },

        success : function(data) {
            // console.log(data);
            try {
               document.getElementById('user' + userid).style.display = 'none'
            }
            catch {
               document.getElementById('editor' + userid).style.display = 'none'
            }
            
            // plate = document.createElement('<div id=' + userid + '><hr><div class="inline-wrapper"><div class="text2">' + data + '</div><div class="inline-wrapper"><div class="button2" onclick="cancelban(' + userid + ')">Восстановить</div></div></div></div>')
            // document.getElementById('hid2.2').append(plate)
        },
    });
}

function toeditor(userid) {
    userid = parseInt(userid)
    ans = sendajax('toeditor', userid)
    document.getElementById('user' + userid).style.display = 'none'
}

function toadmin(userid) {
    userid = parseInt(userid)
    var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();

    $.ajax({
        url :  $("#cururl").attr("cururl") + "edit/moreedit/",
        type : "POST",
        data : {
            'type': 'toadmin',
            'data': userid,
            'csrfmiddlewaretoken': csrftoken
        },

        success : function(returned) {
            document.location.href = '/groups/' + $('#groupslug').attr('groupslug') + '/'
        },
    });

}

function touser(userid) {
    userid = parseInt(userid)
    ans = sendajax('touser', userid)
    document.getElementById('editor' + userid).style.display = 'none'
}

function deletegroupimage() {
    var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();

    $.ajax({
        url : $("#cururl").attr("cururl") + "edit/moreedit/",
        type : "POST",
        data : {
            'type': 'deletegroupimage',
            'csrfmiddlewaretoken': csrftoken
        },

        success : function(data) {
            location.reload(true);
        },
    });
}

function cancelban(userid) {
    var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
    userid = parseInt(userid)

    $.ajax({
        url : $("#cururl").attr("cururl") + "edit/moreedit/",
        type : "POST",
        data : {
            'type': 'cancelban',
            'userid': userid,
            'csrfmiddlewaretoken': csrftoken
        },

        success : function(data) {
            // console.log(data);
            document.getElementById('banned' + userid).style.display = 'none'
        },
    });
}

function checkslug(slug) {
    var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();

    $.ajax({
        url : $("#cururl").attr("cururl") + "edit/moreedit/",
        type : "POST",
        data : {
            'type': 'checkslug',
            'slug': slug,
            'csrfmiddlewaretoken': csrftoken
        },

        success : function(data) {
            // console.log(data)
            if( data == 'hasAlready' ) {
                showwarning('Такой идентификатор уже занят')
            }
            else if( data == 'wrong' )
            {
                showwarning('Используйте только латинские буквы')
            }
            else if( data == 'empty' )
            {
                showwarning('Пустое поле')
            }
            else if( data == 'spaces' )
            {
                showwarning('Без пробелов')
            }
            else if( data != 'error' ) {
                document.location.href = data
            }
        },
    });
}

function savevalue(type) {
    var csrftoken = $('input[name="csrfmiddlewaretoken"]').val(),
        ajaxtype = false;

    if( type == 'name') {
        if (document.getElementById('nameinput').value.replace(/\s+/g, '') != '')
        {
            ajaxtype = 'editname'
            data = document.getElementById('nameinput').value
        }
        else
        {
            showwarning('Название не должно быть пустым')
        }

    }
    else if( type == 'description') {
        ajaxtype = 'editdescription'
        data = document.getElementById('descriptioninput').value
    }
    else if( type == 'slug') {
        data = document.getElementById('sluginput').value
        checkslug(data)
    }

    if( ajaxtype ) {
        $.ajax({
            url : $("#cururl").attr("cururl") + "edit/moreedit/",
            type : "POST",
            data : {
                'type': ajaxtype,
                'data': data,
                'csrfmiddlewaretoken': csrftoken
            },

            success : function(data) {
                console.log(data)
                if( data != 'error') {
                    document.location.href = data
                }
            },
        });
    }
}

function readURL(input) {
  if( input.files ) {
    file = input.files[0]
    if( file.type != 'image/png' & file.type != 'image/jpeg' ) {
        showwarning('Загрузите изображение в формате jpeg или png')
    } else
    if( file.size > 5000000 ) {
        showwarning('Файл слишком большой')
    } else
    {
        setimage(input, 'testimg')
        img = document.getElementById('testimg')
        img.onload = function() {
            console.log(img.naturalWidth)
            width = img.naturalWidth
            height = img.naturalHeight
            if( width / height >= 2 || height / width >= 1.2 ) {
                showwarning('Слишком вытянутая картинка')
            } else {
                setimage(input, 'groupimage')
                $('#stage1').hide()
                $('#stage2').show()
                // document.getElementById('uploadimage').style.display = "none"
                // document.getElementById('cancelupload').style.display = "block"
                // document.getElementById('saveimage').style.display = "block"
            }
        }
    }
  }
}

function readURL2(input) {
  if( input.files ) {
    file = input.files[0]
    if( file.type != 'image/png' & file.type != 'image/jpeg' ) {
        showwarning('Загрузите изображение в формате jpeg или png')
    } else
    if( file.size > 5000000 ) {
        showwarning('Файл слишком большой')
    } else
    {
        setimage(input, 'testimg')
        img = document.getElementById('testimg')
        img.onload = function() {
            console.log(img.naturalWidth)
            width = img.naturalWidth
            height = img.naturalHeight
            if( width / height >= 2 || height / width >= 1.2 ) {
                showwarning('Слишком вытянутая картинка')
            } else {
                input.form.submit()
                // document.getElementById('uploadimage').style.display = "none"
                // document.getElementById('cancelupload').style.display = "block"
                // document.getElementById('saveimage').style.display = "block"
            }
        }
    }
  }
}

function uploadfile() {
    var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();

    input = document.getElementById('fileinput')
    file = input.files[0]

    $.ajax({
        url : $("#cururl").attr("cururl") + "edit/moreedit/?csrfmiddlewaretoken=" + csrftoken,
        type : "GET",
        contentType: false,
        processData: false,
        data : {
            'type': 'uploadimage',
            'image': file,
            'csrfmiddlewaretoken': csrftoken
        },

        success : function(data) {
            // location.reload(true)
        },
    });
}

function setimage(input, imgid) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();

    reader.onload = function(e) {
      $('#' + imgid).attr('src', e.target.result);
    }

    reader.readAsDataURL(input.files[0]);
  }
}

function cancelupload(url) {
    $('#groupimage').attr('src', url);
    $('#stage2').hide()
    $('#stage1').show()
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

function showeditors() {
    if( $('#toadminlist').css('display') == "none" ) {
        $('#toadminlist').show(300)
        $('#disabler').css({'z-index': '1021'}) 
        $('#disabler').animate({'opacity': '0.7'}, 300)  

        if ($(document).height() > $(window).height()) {
            var scrollTop = ($('html').scrollTop()) ? $('html').scrollTop() : $('body').scrollTop()
            $('html').addClass('noscroll').css('top',-scrollTop)       
        }

    } else {
        $('#toadminlist').hide(300)
        $('#disabler').animate({'opacity': '0'}, 300)
        $('#disabler').animate({'z-index': '0'}, 300) 

        var scrollTop = parseInt($('html').css('top'))
        $('html').removeClass('noscroll')
        $('html,body').scrollTop(-scrollTop)   
    }
}

function copyLink(text) {
    navigator.clipboard.writeText(window.location.hostname + text)
}

function update_symbols(id_symbols, id_input, count) {
    $('#' + id_symbols).text('Еще символов: ' + (count - $('#' + id_input).val().length))
}

/*

function removeElement(element) {
     element.remove();
}

*/
