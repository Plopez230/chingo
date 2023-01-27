function populate_fields(word) {
    $("#edit-word").modal('show');
    document.getElementById("edit_simplified").value = word.getAttribute("simplified");
    document.getElementById("edit_traditional").value = word.getAttribute("traditional");
    document.getElementById("edit_pinyin").value = word.getAttribute("pinyin");
    document.getElementById("edit_part_of_speech").value = word.getAttribute("part_of_speech");
    document.getElementById("edit_translation").value = word.getAttribute("translation");
    document.getElementById("edit_classifiers").value = word.getAttribute("classifiers");
    document.getElementById("edit_id").value = word.getAttribute("word_id");
  }

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