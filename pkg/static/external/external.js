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

    $('#email_submit').click(function(){
        var email = $('#email').val()
        var csrf = $('#csrf').val()
        $.ajax({
            url: '/pass/reset/',
            type: 'POST',
            data: {"email":email, "csrf_token":csrf},
            success: function(resp){
                if (resp === "success") {
                    $('.email').addClass('d-none')
                    $('.otp').removeClass('d-none')
                }else {
                    window.location.href = "/forgot-password/";
                }
            }
          })
    })


    $('#pass_reset').click(function(){
        var otp = $('#otp').val()
        var csrf = $('#csrf').val()
        var email = $('#email').val()
        $.ajax({
            url: '/password/reset/',
            type: 'POST',
            data: {"otp":otp,"email":email,"csrf_token":csrf},
            success: function(resp){
                if (resp === "success") {
                    $('.otp').addClass('d-none')
                    $('.pass_reset').removeClass('d-none')
                }else {
                    $('#incorrect').removeClass('d-none')
                }
            }
          })
    })

    $('#otp').keydown(function(){
        $('#incorrect').addClass('d-none') 
    })



    $('#reset_submit').click(function(){
        var pwd = $('#pwd').val()
        var pwd1 = $('#pwd1').val()
        var csrf = $('#csrf').val()
        var email = $('#email').val()
        $.ajax({
            url: '/reset/user/password/',
            type: 'POST',
            data: {"pwd":pwd, "pwd1":pwd1, "email":email, "csrf_token":csrf},
            success: function(resp){
                if (resp === "success") {
                    window.location.href = "/login/";
                }else {
                    $('#pass_inc').removeClass('d-none')
                }
            }
          })
    })

    $('#pwd').keydown(function(){
        $('#pass_inc').addClass('d-none') 
    })
    $('#pwd1').keydown(function(){
        $('#pass_inc').addClass('d-none') 
    })
    

    $('#reset_submit').click(function(){
        var pwd = $('#pwd').val()
        var pwd1 = $('pwd1').val()
        var csrf = $('#csrf').val()
        $.ajax({
            url: '/pass/reset/',
            type: 'POST',
            data: {"otp":otp, "csrf_token":csrf},
            success: function(resp){
                if (resp === "success") {
                    $('.email').hide()
                    $('.otp').removeClass('d-none')
                }else {
                    $('#incorrect').removeClass('d-none')
                }
            }
          })
    })





    $('#state').change(function(){
        var stateId = $(this).val()
        var csrf = $('#csrf_token').val()
        $.ajax({
          url: '/state/lgas/',
          type: 'POST',
          data: {"state":stateId, "csrf_token":csrf},
          beforeSend: function(){
            $('#lga').html("")
          },
          success: function(resp){
            $('#lga').append("<option class='bg-transparent text-light' value='' disabled>Select LGA</option>")
            for (let index = 0; index < resp.length; index++){
              $('#lga').append(`<option class="bg-transparent text-light" value="${resp[index].lga_id}">${resp[index].lga_name}</option>`)
            }
          }
        })
      })
    
      $('#search').click(function(){
            var search_input = $(this).val();
            var csrf_token = $('#csrf_token').val();
            $.ajax({
                type: 'POST',
                url: '/user-search-page/',
                data: {"search_input":search_input,"csrf_token":csrf_token},
                success: function(data) {
                    $('#searchResults').empty();
                    $.each(data.users, function(index, user) {
                        $('#searchResults').append(`<li class="text-light">${user.name} - ${user.type}</li>`);
                    });
                    $.each(data.reports, function(index, report) {
                        $('#searchResults').append(`<li class="text-light">${report.name} - ${report.type}</li>`);
                    });
                    $.each(data.categories, function(index, category) {
                        $('#searchResults').append(`<li class="text-light">${category.name} - ${category.type}</li>`);
                    });
                }
            });
        });
    


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

    $('.comment_btn').click(function(){
        var commentSection = $(this).closest('.comment_section');
        var comment = commentSection.find('#comment').val();
        var report_id = commentSection.find('#report_id').val();
        var csrf_token = commentSection.find('#csrf_token').val();
        var data2send = {"comment":comment, "report_id":report_id, "csrf_token":csrf_token};
        $.ajax({
            type: 'POST',
            url: '/comment/',
            data: data2send,
            success: function(res){
                commentSection.find('.cnt').text(res.comment);
                commentSection.find('#comment').val('');
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