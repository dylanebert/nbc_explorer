var origin = window.location.origin

function getPhrase(idx) {
	$.getJSON(origin + '/get_phrase?idx=' + idx, function(phrase) {
		$('#phrase').text(phrase.phrase)
	})
}

function getQuery(idx) {
	let src = 'https://storage.cloud.google.com/nbc_release/phrases/' + idx + '.mp4'
	$('#vid').attr('src', src).trigger('play')
}

$(document).ready(function() {
	var url_string = window.location.href
	var url = new URL(url_string)
	var id = url.searchParams.get('id')
	var phraseIdx = parseInt(url.searchParams.get('phrase'))
	var queryIdx = parseInt(url.searchParams.get('query'))
	getPhrase(phraseIdx)
	getQuery(queryIdx)
	$('#likert').submit(function(event) {
		event.preventDefault()
		let input = parseInt($('input[name=inlineRadioOptions]:checked', '#likert').val())
		console.log(id, input)
	})
})
