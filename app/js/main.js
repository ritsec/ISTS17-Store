$(document).ready(function(){
    $("#login-modal").modal('show');
});

$(function() {
    $('button').click(function(e) {
        console.log(e.target.id);
        $.post(
            '/shop', 
            {
                item_id: e.target.id
            },
            function(data, status){
                $("#result").html(data);
            }
        )
    });
});


   
