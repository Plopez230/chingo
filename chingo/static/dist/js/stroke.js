
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
  
  var chars = [];
  var timeout;
  var text;
  var last_call = 0;
  
  function create_chars(characters, speed){
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
          outlineColor: '#dddddd',
          strokeAnimationSpeed: speed,
          delayBetweenStrokes: 10,
          delayBetweenLoops: 3000,
          showCharacter: false
        }));
      }
  }

  function chainAnimations(index, call_number)
  {
    var delay = 1000;
    if (index >= chars.length)
    {
        return;
    }
    (chars[index]).animateCharacter({
      onComplete: function() {
            timeout = setTimeout(function() {
        if (call_number == last_call){
            chainAnimations(index+1, call_number);}
        }, delay)
        
      }
    })
  }
  
  function write_hanzi_strokes (){
    if (!text)
         ;
    last_call = last_call + 1;
    characters = text.split("");
    create_divs(characters.length);
    create_chars(characters, $('#range-speed')[0].value/100.0);
    chainAnimations(0, last_call);
  }

  function show_stroke_modal (txt){
    $('#stroke').modal('show'); 
    text = txt;
    write_hanzi_strokes ();
  }

