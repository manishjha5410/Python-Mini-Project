
$(document).ready(function(){

    $('.fa-bars').click(function(){
      $(this).toggleClass('fa-times');
      $('.nav').toggleClass('nav-toggle');
    });
  
    if(window.screen.width<=992)
    {
      $('header').addClass('header-active');
    }
  
    $(window).on('load scroll',function(){
  
      $('.fa-bars').removeClass('fa-times');
      $('.nav').removeClass('nav-toggle');
  
      if(window.screen.width>992)
      {
        if($(window).scrollTop() > 10){
          $('header').addClass('header-active');
        }else{
          $('header').removeClass('header-active');
        }
      }
      else
      {
        if($(window).scrollTop() > 10){
          $('header').addClass('shadow--one');
        }else{
          $('header').removeClass('shadow--one');
        }
      }
  
    });
  
    $('.facility').magnificPopup({
      delegate:'a',
      type:'image',
      gallery:{
        enabled:true
      }
    });
  
    document.querySelectorAll('.depart_ment_tab li').forEach((item,index)=>{
        item.addEventListener('mouseover',(e)=>{
          document.querySelectorAll('.depart_ment_tab li').forEach((ele)=>{
            ele.children[0].classList.remove('active');
          })
          e.target.classList.add('active');
          e.target.parentNode.classList.add('active');
        })
    })
  
  });