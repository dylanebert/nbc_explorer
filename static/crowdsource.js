let formLikert = `
<div class="form-group">
	<div class="form-check form-check-inline">
		<input class="form-check-input" type="radio" name="q0" id="radio1" value="1">
		<label class="form-check-label" for="radio1">Yes</label>
	</div>
	<div class="form-check form-check-inline">
		<input class="form-check-input" type="radio" name="q0" id="radio2" value="2">
		<label class="form-check-label" for="radio2">No</label>
	</div>
	<div class="form-check form-check-inline">
		<input class="form-check-input" type="radio" name="q0" id="radio3" value="3">
		<label class="form-check-label" for="radio2">Unsure</label>
	</div>
</div>
`

var origin = window.location.origin

function getQuestions(idx) {
	$('#likertQuestions').empty()
	$.getJSON(origin + '/get_questions?idx=' + idx, function(questions) {
		$.each(questions, function(i, question) {
			if(question != null) {
				let likert = formLikert.replace(/name="q0"/g, 'name="q' + (i+1) + '"')
				let html = `<h2 id="q` + (i+1) + `-text">` + question + `</h2>` + likert
				$('#likertQuestions').append(html)
				$('input[type=radio][name="q' + (i+1) + '"]').change(function() {
					checkReadySubmit()
				})
			}
		})
	})
}

function getQuery(idx) {
	let src = 'https://storage.googleapis.com/nbc_release/phrases/' + idx + '.mp4'
	$('#vid').attr('src', src)
}

function checkReadySubmit() {
	var names = {}
	$(':radio').each(function() {
		names[$(this).attr('name')] = true
	})
	var count = 0
	$.each(names, function() {
		count++
	})
	if($(':radio:checked').length == count) {
		$('#submit').prop('disabled', false)
	} else {
		$('#submit').prop('disabled', true)
	}
}

function configureSubmit(id) {
	$('#likert').submit(function(event) {
		event.preventDefault()
		var res = []
		for(i = 1; i <= 3; i++) {
			res.push(parseInt($('input[name=q' + i + ']:checked', '#likert').val()))
		}
		res = JSON.stringify(res)
		console.log(res)
		let params = '?id=' + id + '&res=' + res
		$.get(origin + '/save_response' + params, function(data) {
			if(data == 'done') {
				console.log('saved')
				next()
			} else {
				console.log(data)
			}
		})
	})
}

function next() {
	$.getJSON(origin + '/find_id', function(res) {
		window.location.href = origin + '/crowdsource?id=' + res
	})
}

$(document).ready(function() {
	var url_string = window.location.href
	var url = new URL(url_string)
	var id = url.searchParams.get('id')
	if(id == null) {
		next()
	} else {
		$.getJSON(origin + '/get_entity?id=' + id, function(res) {
			getQuestions(res['pid'])
			getQuery(res['qid'])
			configureSubmit(id)
		})
	}
})
