$(function() {
    $('button').click(function(e) {
        console.log(e.target.id);
        $.post('/buy', 
        {item_id: e.target.id},
        function(data, status){
            alert(data);
        }
        )
    });
});