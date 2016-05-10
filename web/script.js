`use strict`

function scrollTo(id) {
  $('html, body').animate({
    scrollTop: $(id).offset().top
  }, 1000);
}

function championSprite(cName) {
  name = cName.replace(/['\.\s]/g, '');
  return 'http://ddragon.leagueoflegends.com/cdn/6.9.1/img/champion/' + name + '.png'
}

function createListItem(cName, cMastery) {
  var $li = $('<li>').attr('class', 'compatibility row top-buffer').append(
    $('<div>').attr('class', 'cSprite col-xs-2').append(
      $('<img>').attr('src', championSprite(cName)).attr('class', 'small-img'))
    ).append(
    $('<div>').attr('class', 'cName col-xs-4').text(cName)).append(
    $('<div>').attr('class', 'cMastery col-xs-6').text(cMastery)
  );
  return $li;
}

function displayContent(data) {
  scores = []
  for(var key in data) {
    scores.push([key, data[key]])
  }
  scores.sort(function(a,b) {
    return b[1] - a[1];
  });
  console.log(scores);

  $ol = $('ol.compatibility').empty();
  for(var i = 0; i < scores.length; i++) {
    var cName = scores[i][0];
    var cMastery = scores[i][1];
    var $li = createListItem(cName, cMastery);
    $ol.append($li);
  }

  $('#content').removeClass('hidden');    
  scrollTo('#content');
}

function displayError(jqXHR, textStatus, errorThrown) {
  console.log(textStatus);
  $('ol.compatibility').prepend(
    $('<li>').attr('class', 'compatibility row top-buffer').text(textStatus)
  );
}

$(document).ready(function() {
  $('button.submit').click(function() {
    var summoner_name = $('.input.summoner_name').val();
    var region = $('.input.region').val();
    var url = 'predict?summoner_name=' + summoner_name + '&region=' + region
    console.log(url);
    $.ajax({
      url: url,
      contentType: 'application/json'
,      success: displayContent,
      err: displayError
    });
  });

  $('.scrolltoarrow').click(function() {
    scrollTo('html');
  });
});