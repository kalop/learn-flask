$(document).ready(function(){


//POST method with ajax
    $("form").on('submit', function(event){

        console.log("Value: " + $("#id1").text())
        $.ajax({
            data : {
                permission : $('#id1').text()
            },
            type : 'POST',
            url : '/changePermission'
        })
        .done(function(data){
            $('#id1').text(data).show();
        });

        event.preventDefault();
    });



});
