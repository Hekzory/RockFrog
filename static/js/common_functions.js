manage_articles_url = "/manage_articles/"

function plus_minus(articleid, action) {
    var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
    articleid = parseInt(articleid)

    $.ajax({
        url : "/manage_articles/",
        type : "POST",
        data : {
            'action': 'plus_minus',
            'type': action,
            'articleid': articleid,
            'csrfmiddlewaretoken': csrftoken
        },

        success : function(data) {
            // console.log('Ok')

            $('#plusicon' + articleid).removeClass('grey-color')
            $('#minusicon' + articleid).removeClass('grey-color')

            if (action == 'plus')
            {
                $('#plus' + articleid).text(parseInt($('#plus' + articleid).text()) + 1)                
                $('#plusicon' + articleid).addClass('green-color')

                $('#plusicon' + articleid).attr('onclick', "plus_minus('" + articleid + "', 'remove_plus')")
                $('#minusicon' + articleid).attr('onclick', "plus_minus('" + articleid + "', 'minusminus')")
            }
            else if (action == 'minus')
            {
                $('#minus' + articleid).text(parseInt($('#minus' + articleid).text()) + 1)
                $('#minusicon' + articleid).addClass('red-color')

                $('#plusicon' + articleid).attr('onclick', "plus_minus('" + articleid + "', 'plusplus')")
                $('#minusicon' + articleid).attr('onclick', "plus_minus('" + articleid + "', 'remove_minus')")
            }
            else if (action == 'plusplus')
            {
                $('#plus' + articleid).text(parseInt($('#plus' + articleid).text()) + 1)
                $('#minus' + articleid).text(parseInt($('#minus' + articleid).text()) - 1)

                $('#plusicon' + articleid).addClass('green-color')
                $('#minusicon' + articleid).removeClass('red-color')
                $('#minusicon' + articleid).addClass('grey-color')

                $('#plusicon' + articleid).attr('onclick', "plus_minus('" + articleid + "', 'remove_plus')")
                $('#minusicon' + articleid).attr('onclick', "plus_minus('" + articleid + "', 'minusminus')")
            }
            else if (action == 'minusminus')
            {
                $('#minus' + articleid).text(parseInt($('#minus' + articleid).text()) + 1)
                $('#plus' + articleid).text(parseInt($('#plus' + articleid).text()) - 1)

                $('#plusicon' + articleid).removeClass('green-color')
                $('#plusicon' + articleid).addClass('grey-color')
                $('#minusicon' + articleid).addClass('red-color')

                $('#plusicon' + articleid).attr('onclick', "plus_minus('" + articleid + "', 'plusplus')")
                $('#minusicon' + articleid).attr('onclick', "plus_minus('" + articleid + "', 'remove_minus')")
            }
            else if (action == 'remove_plus')
            {
                $('#plus' + articleid).text(parseInt($('#plus' + articleid).text()) - 1)
                $('#plusicon' + articleid).removeClass('green-color')
                $('#plusicon' + articleid).addClass('grey-color')

                $('#plusicon' + articleid).attr('onclick', "plus_minus('" + articleid + "', 'plus')")
                $('#minusicon' + articleid).attr('onclick', "plus_minus('" + articleid + "', 'minus')")
            }
            else if (action == 'remove_minus')
            {
                $('#minus' + articleid).text(parseInt($('#minus' + articleid).text()) - 1)
                $('#minusicon' + articleid).removeClass('red-color')
                $('#minusicon' + articleid).addClass('grey-color')

                $('#plusicon' + articleid).attr('onclick', "plus_minus('" + articleid + "', 'plus')")
                $('#minusicon' + articleid).attr('onclick', "plus_minus('" + articleid + "', 'minus')")
            }
        },
    });
}

function mark_viewed(articleid, value) {
    var csrftoken = $('input[name="csrfmiddlewaretoken"]').val()

    $.ajax({
        url : manage_articles_url,
        type : "POST",
        data : {
            'action': 'mark_viewed',
            'articleid': articleid,
            'value': value,
            'csrfmiddlewaretoken': csrftoken
        },

        success : function(data) {
            if( data == 'Ok' )
            {     
                if( value )
                {   
                    $('#viewscount' + articleid).text(parseInt($('#viewscount' + articleid).text()) + 1)
                    $('#visibility' + articleid).text('visibility')
                    $('#visibility' + articleid).attr('onclick', 'mark_viewed(' + articleid + ', ' + false + ')')
                    $('#visibility' + articleid).attr('title', 'Просмотрено')
                }
                else
                {   
                    $('#viewscount' + articleid).text(parseInt($('#viewscount' + articleid).text()) - 1)
                    $('#visibility' + articleid).text('visibility_off')
                    $('#visibility' + articleid).attr('onclick', 'mark_viewed(' + articleid + ', ' + true + ')')
                    $('#visibility' + articleid).attr('title', 'Не просмотрено')
                }
            }
        },
    })
    
}
function update_symbols(id_symbols, id_input, count) {
    $('#' + id_symbols).text('Еще символов: ' + (count - $('#' + id_input).val().length))
}

function auto_grow(element) {
    element.style.height = "5px";
    element.style.height = (element.scrollHeight)+"px";
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