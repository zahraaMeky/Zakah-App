/*
   $(document).ready(function(){

   //this function send url request every 800 sec
   //to refresh data
      setInterval(function(){
       $.ajax({
         method:'GET',
         url: "get_money/",
         success: function(response){
           var m = response.money
           console.log(m);
           $("#amount").val(m.toString());
           console.log(response);
       }});
    },500);

  });
  */

  if ($('.typed').length) {
    var typed_strings = $(".typed").data('typed-items');
    typed_strings = typed_strings.split(',')
    new Typed('.typed', {
      strings: typed_strings,
      loop: true,
      typeSpeed: 100,
      backSpeed: 50,
      backDelay: 2000
    });
  }
  if ($('.typed-e').length) {
    var typed_strings = $(".typed-e").data('typed-items-e');
    typed_strings = typed_strings.split(',')
    new Typed('.typed-e', {
      strings: typed_strings,
      loop: true,
      typeSpeed: 100,
      backSpeed: 50,
      backDelay: 2000
    });
  }

  var ml4 = {};
  ml4.opacityIn = [0,1];
  ml4.scaleIn = [0.2, .8];
  ml4.scaleOut = 1;
  ml4.durationIn = 800;
  ml4.durationOut = 600;
  ml4.delay = 500;


  anime.timeline({loop: true})
    .add({
      targets: '.ml4 .letters-1',
      opacity: ml4.opacityIn,
      scale: ml4.scaleIn,
      duration: ml4.durationIn
    }).add({
      targets: '.ml4 .letters-1',
      opacity: 0,
      scale: ml4.scaleOut,
      duration: ml4.durationOut,
      easing: "easeInExpo",
      delay: ml4.delay
    }).add({
      targets: '.ml4 .letters-2',
      opacity: ml4.opacityIn,
      scale: ml4.scaleIn,
      duration: ml4.durationIn
    }).add({
      targets: '.ml4 .letters-2',
      opacity: 0,
      scale: ml4.scaleOut,
      duration: ml4.durationOut,
      easing: "easeInExpo",
      delay: ml4.delay
    }).add({
      targets: '.ml4 .letters-3',
      opacity: ml4.opacityIn,
      scale: ml4.scaleIn,
      duration: ml4.durationIn
    }).add({
      targets: '.ml4 .letters-3',
      opacity: 0,
      scale: ml4.scaleOut,
      duration: ml4.durationOut,
      easing: "easeInExpo",
      delay: ml4.delay
    }).add({
      targets: '.ml4',
      opacity: 0,
      duration: ml4.delay,
      delay: ml4.delay
    });
