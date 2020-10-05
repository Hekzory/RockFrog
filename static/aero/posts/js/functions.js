function plus_minus(articleid, action) {
    new_rating = parseInt($('#rating' + articleid).text())
    if( action == 'plus' || action == 'remove_minus' ) {
        new_rating += 1
    } 
    else if( action == 'minus' ||  action == 'remove_plus') {
        new_rating -= 1
    }
    else if( action == 'plusplus' ) {
        new_rating += 2
    }
    else if( action == 'minusminus' ) {
        new_rating -= 2
    }
    if( new_rating > 0 ) {
        new_rating = String('+' + new_rating)
    }
    $('#rating' + articleid).text(new_rating)

    if (action == 'plus')
    {    
        $('#plusicon' + articleid).addClass('blue-icon')

        $('#plusicon' + articleid).attr('onclick', "plus_minus('" + articleid + "', 'remove_plus')")
        $('#minusicon' + articleid).attr('onclick', "plus_minus('" + articleid + "', 'minusminus')")
    }
    else if (action == 'minus')
    {
        $('#minusicon' + articleid).addClass('blue-icon')

        $('#plusicon' + articleid).attr('onclick', "plus_minus('" + articleid + "', 'plusplus')")
        $('#minusicon' + articleid).attr('onclick', "plus_minus('" + articleid + "', 'remove_minus')")
    }
    else if (action == 'plusplus')
    {
        $('#plusicon' + articleid).addClass('blue-icon')
        $('#minusicon' + articleid).removeClass('blue-icon')

        $('#plusicon' + articleid).attr('onclick', "plus_minus('" + articleid + "', 'remove_plus')")
        $('#minusicon' + articleid).attr('onclick', "plus_minus('" + articleid + "', 'minusminus')")
    }
    else if (action == 'minusminus')
    {
        $('#plusicon' + articleid).removeClass('blue-icon')
        $('#minusicon' + articleid).addClass('blue-icon')

        $('#plusicon' + articleid).attr('onclick', "plus_minus('" + articleid + "', 'plusplus')")
        $('#minusicon' + articleid).attr('onclick', "plus_minus('" + articleid + "', 'remove_minus')")
    }
    else if (action == 'remove_plus')
    {
        $('#plusicon' + articleid).removeClass('blue-icon')

        $('#plusicon' + articleid).attr('onclick', "plus_minus('" + articleid + "', 'plus')")
        $('#minusicon' + articleid).attr('onclick', "plus_minus('" + articleid + "', 'minus')")
    }
    else if (action == 'remove_minus')
    {
        $('#minusicon' + articleid).removeClass('blue-icon')

        $('#plusicon' + articleid).attr('onclick', "plus_minus('" + articleid + "', 'plus')")
        $('#minusicon' + articleid).attr('onclick', "plus_minus('" + articleid + "', 'minus')")
    }


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
            //console.log('Ok')
        },
    });
}