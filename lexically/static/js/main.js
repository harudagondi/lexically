$(function() {
  $("table").tablesorter();
  $(":file").filestyle();
  $(":submit").click(function() {
    var ipa, language, meaning, notes, parent, pos;
    parent = $("#parent").val();
    pos = $("#pos").val();
    meaning = $("#meaning").val();
    ipa = $("#ipa").val();
    notes = $("#notes").val();
    language = $("#language").val();
    $.ajax({
      url: '/',
      data: $('form').serialize(),
      type: 'POST',
      success: function(response) {
        return console.log(response);
      },
      error: function(error) {
        return console.log(error);
      }
    });
  });
});
