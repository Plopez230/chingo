
function create_divs(n) {
    var i = 0;
    document.getElementById('multiple-character-target-div').innerHTML = "";
    while (i < n)
    {
      var element = document.createElement("div");
      element.setAttribute("id", "character-target-"+i.toString())
      document.getElementById('multiple-character-target-div').appendChild(element); 
      i++;
    }
  }
  
  var chars;
  var timeout;
  
  function create_chars(characters){
    chars = [];
    for (var i = 0; i < characters.length; i++){
      chars.push (HanziWriter.create(
        'character-target-'+i.toString(), 
        characters[i], 
        {
          width: 130,
          height: 130,
          padding: 0,
          strokeColor: '#17a2b8',
          outlineColor: '#cccccc',
          strokeAnimationSpeed: 1,
          delayBetweenStrokes: 10,
          delayBetweenLoops: 3000,
          showCharacter: false
        }));
      }
  }

  function chainAnimations(index)
  {
    var delay = 1000;
    if (index >= chars.length)
    {
        return;
    }
    (chars[index]).animateCharacter({
      onComplete: function() {
        timeout = setTimeout(function() {
        chainAnimations(index+1);
      }, delay)
      }
    })
  }
  
  function write_hanzi_strokes (text){
    if (!text)
        return;
    $('#stroke').modal('show'); 
    characters = text.split("");
    create_divs(characters.length);
    create_chars(characters);
    chainAnimations(0);
  }