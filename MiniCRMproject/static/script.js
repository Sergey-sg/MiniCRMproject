// Open password
$('body').on('click', '.password-checkbox', function(){
          if ($(this).is(':checked')){
              $('#password-input').attr('type', 'text');
          } else {
              $('#password-input').attr('type', 'password');
          }
      });

$('body').on('click', '.register-password1-checkbox', function(){
          if ($(this).is(':checked')){
              $('#register-password1-input').attr('type', 'text');
          } else {
              $('#register-password1-input').attr('type', 'password');
          }
      });

$('body').on('click', '.register-password2-checkbox', function(){
          if ($(this).is(':checked')){
              $('#register-password2-input').attr('type', 'text');
          } else {
              $('#register-password2-input').attr('type', 'password');
          }
      });
