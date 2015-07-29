jQuery(document).ready(function() {
   jQuery('.toggle-nav').click(function(e) {
       jQuery(this).toggleClass('active');
       jQuery('.menu ul').toggleClass('active');

       e.preventDefault();
   });
});

/* Anything that gets to the document
   will hide the dropdown */
$(document).click(function(){
  $(".menu ul").addClass('active');
});

/* Clicks within the dropdown won't make
   it past the dropdown itself */
$(".menu").click(function(e){
  e.stopPropagation();
});

// One page scrolling!!!! :O

$(".main").onepage_scroll();
