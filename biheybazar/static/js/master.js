$(function () {
    $('textarea').ckeditor();
    $('#bton').on('click', function(e) {
        console.log("Hello")
      console.log('ckeditor content: ' + $('textarea[name="DSC"]').val());
    })
  });