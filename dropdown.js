$(document).ready(function(){
    $(".teacher").click(function () {
       //this is change select value 1
        $('#dynamicChange').val('1').trigger('change');
    });
     $(".student").click(function () {
         //
         //this is change select value 1
         $('#dynamicChange').val('2').trigger('change');
    });

});