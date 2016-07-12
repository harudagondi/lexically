$ ->
  $( "table" ).tablesorter()
  $( ":file" ).filestyle()

  $( ":submit" ).click ->
    parent = $( "#parent" ).val()
    pos = $( "#pos" ).val()
    meaning = $( "#meaning" ).val()
    ipa = $( "#ipa" ).val()
    notes = $( "#notes" ).val()
    language = $( "#language" ).val()

    $.ajax({
      url: '/',
      data: $('form').serialize(),
      type: 'POST',
      success: (response) ->
        console.log(response)
      error: (error) ->
        console.log(error)
      })

    return

  return
