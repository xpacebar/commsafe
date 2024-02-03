$(document).ready(function(){
    $('#consent').click(function(){
        var consent = $(this).prop('checked');
        if(consent == true){
            $('#btn_signup').removeAttr('disabled');
        }else{
            $('#btn_signup').attr('disabled','disabled')
        }
    })

    $('#btn_show').click(function(){
        $('#password').attr('type','text')
    })
    $('#btn_show').mouseleave(function(){
        $('#password').attr('type','password')
    })

    $('#btn_show1').click(function(){
        $('#new_password1').attr('type','text')    
    })
    $('#btn_show1').mouseleave(function(){
        $('#new_password1').attr('type','password')
    })



    $('#send_button').click(function(){
        var message = $('.message_area').val();
        var receiver_id = $('#receiver_id').val();
        var csrf = $('#csrf').val();
        var data2send = {"message":message, "receiver_id":receiver_id, "csrf_token":csrf};
        $.ajax({
            type: 'POST',
            url: '/send',
            data: data2send,
            success: function(res){
                    $('#display').text(res.content);
                    $('#new_msg').val(res.id);
                    $('#floatingTextarea2').val("");
            }
        });
    });

    $('#comment_btn').click(function(){
        var comment = $(this).closest('.comment_section').find('#comment').val();
        var report_id = $(this).closest('.comment_section').find('#reporr_id').val();
        var csrf_token = $(this).closest('.comment_section').find('#csrf_token').val();
        var data2send = {"comment":comment, "report_id":report_id, "csrf_token":csrf_token};
        var self = $(this);
        $.ajax({
            type: 'POST',
            url: '/comment/',
            data: data2send,
            success: function(res){
                 var back = self.closest('.comment_section').find('.cnt').text(res.comment);
                self.closest('.comment_section').find('#comment').val('');
            }
        })
    });

    $('.btnlike').click(function(){
        var self = $(this);
        var isLiked = self.hasClass('liked');
        var post_id = $(this).data('post-id');
        var csrf_token = $(this).data('csrf');
        data = {"report_id": post_id, "csrf_token":csrf_token}
        // alert(isLiked)
        if(isLiked == true){
            $.ajax({
                url: '/unlike/',
                type: 'POST',
                data: data,
                success: function(res){
                self.text('Like');
                self.removeClass('liked');
                self.addClass('like');
                self.siblings('.like_counter').text(res.count);
                }
            })
        }else{
            $.ajax({
                url: '/like/',
                type: 'POST',
                data: data,
                success: function(res){
                    self.text('Liked');
                    self.removeClass('like');
                    self.addClass('liked');
                    self.siblings('.like_counter').text(res.count)
                }
            })   
        }
    })




})