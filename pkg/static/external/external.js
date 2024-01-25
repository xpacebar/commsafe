$(document).ready(function(){
    $('#consent').click(function(){
        var consent = $(this).prop('checked');
        if(consent == true){
            $('#btn_signup').removeAttr('disabled');
        }else{
            $('#btn_signup').attr('disabled','disabled')
        }
    })

    // $('#btn_login').click(function(event){
    //     var username = $('#username').val();
    //     var password = $('#password').val();
    //     if(username != 'admin' && password != 'admin'){
    //         alert('Login Failed')
    //         event.preventDefault();
    //     }
    // })
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
})