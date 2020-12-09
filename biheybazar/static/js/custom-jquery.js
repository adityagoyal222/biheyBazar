// $(document).ready(function(){
  
//     $(".dateinput").datepicker({changeYear: true,changeMonth: true});
   
   
//   });


  // initialize with defaults
// $("#input-id").rating();

// with plugin options (do not attach the CSS class "rating" to your input if using this approach)
// $("#input-id").rating({'size':'lg'});

// $(document).ready(function() {
//     $("#category-button-show").click(function() {
//         $("#category-form").toggle();
//     });
// });

console.log("hello")

$(document).ready(function(){
  $('li').mouseover(function(){
    var current = $(this)
    $('li').each(function(index){
        $(this).addClass("hovered-stars");
        if(index==current.index()){
          return false;
        }
    })
  })

});
