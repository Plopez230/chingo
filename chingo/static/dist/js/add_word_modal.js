
function suggest_words(){
    var data = $('#new-word-form').serialize();
    $.ajax({
        type: 'post',
        url: '/suggest/',
        data: data,
        success: function (data) {
            $('#suggestions tr').not(':first').remove();
            var rows = '';
            for(var i = 0; i < data.length; i++)
            rows += '<tr><td>'+ data[i].label +'</td><td><button type="submit" formaction="add/' + data[i].id + '/" class="close"><span aria-hidden="true">➕</span></button></td></tr>'
            $('#suggestions tr').first().after(rows);
        },
        error: function (data) {
            console.log('An error occurred.');
        },
    });
}