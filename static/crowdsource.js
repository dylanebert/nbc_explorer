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

function configureSubmit(id) {
	$('#likert').submit(function(event) {
		event.preventDefault()
		let res = parseInt($('input[name=inlineRadioOptions]:checked', '#likert').val())
		let params = '?id=' + id + '&res=' + res
		$.get(origin + '/save_response' + params, function(data) {
			if(data == 'done') {
				console.log('saved')
			} else {
				console.log(data)
			}
		})
	})
}

$(document).ready(function() {
	var url_string = window.location.href
	var url = new URL(url_string)
	var id = url.searchParams.get('id')
	if(id == null) {
		$.getJSON(origin + '/find_id', function(res) {
			window.location.href = window.location.href + '?id=' + res
		})
	} else {
		$.getJSON(origin + '/get_res?id=' + id, function(res) {
			getPhrase(res['pid'])
			getQuery(res['qid'])
			configureSubmit(id)
		})
	}
})
