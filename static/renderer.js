var origin = window.location.origin
var phrases;
var currentID = 0;

/*function loadVideo(urls) {
    $('#main').append(`<div id="player" class="imageplayer"></div>`)
    $.each(urls, function(i, url) {
        let line = `<img src="` + url + `"/>`
        $('#player').append(line)
    })
    $('#player').imgplay({rate: 30}).data('imgplay').play()
}*/

function loadVideo(url) {
    $('#main').append('<video src="' + url + '" controls></video>')
}

function select(id) {
    currentID = id
    let idx = parseInt(id.replace('phrase-', ''))
    let phrase = phrases[idx]
    let method = $('#changepointSelect').children('option:selected').val()
    $.getJSON(origin + '/get_phrase?idx=' + idx + '&method=' + method, function(phraseData) {
        $('#main').empty()
        if (phrase['object'] == null) {
            $('#main').append('<h1>' + idx + ': ' + phrase['verb'] + '</h1>')
        } else {
            $('#main').append('<h1>' + idx + ': ' + phrase['verb'] + ' (' + phrase['object'] + ')</h1>')
        }
        if('error' in phraseData) {
            $('#main').append('<p>Error: ' + phraseData['error'] + '</p>')
        }
        else {
            $('#main').append('<h3><b>Phrase:</b> ' + phraseData['phrase'] + '</h3>')
            $('#main').append('<p><b>Caption:</b> ' + phraseData['caption'] + '</p>')
            $('#main').append('<p>' + phraseData['start_step'] + ' - '+ phraseData['end_step'] + '</p>')
            loadVideo(phraseData['video'])
        }
    })
}

function initialize() {
    $('#phrasesTable').DataTable({
        initComplete: function() {
            this.api().columns([1, 2]).every(function() {
                var column = this
                var select = $('<select><option value=""></option></select>')
                    .appendTo($(column.footer()).empty())
                    .on('change', function() {
                        var val = $.fn.dataTable.util.escapeRegex($(this).val())
                        column.search(val ? '^' + val + '$' : '', true, false).draw()
                    })
                column.data().unique().sort().each(function(d, j) {
                    select.append('<option value="' + d + '">' + d + '</option>')
                })
            })
            this.api().columns([3, 4]).every(function() {
                var column = this
                var input = $('<input type="text">')
                    .appendTo($(column.footer()).empty())
                    .on('keyup change clear', function() {
                        if(column.search() !== this.value) {
                            column.search(this.value).draw()
                        }
                    })
            })
        },
        'paging': false,
        'scrollY': '300px',
        'scrollCollapse': true
    })
    $('tbody tr').click(function(e) {
        e.preventDefault()
        select($(this).attr('id'))
    })
    $('tbody tr').hover(function() {
        $(this).css('background-color', '#eeeeee')
    }, function() {
        $(this).css('background-color', 'white')
    })
    $('#changepointSelect').change(function() {
        select(currentID)
    })
    select($('.datarow').first().attr('id'))
}

function populate() {
    $.each(phrases, function(idx, phrase) {
        let html = `
            <tr class="datarow" id="phrase-` + idx + `">
                <td>` + idx + `</td>
                <td>` + phrase['participant'] + `</td>
                <td>` + phrase['task'] + `</td>
                <td>` + phrase['verb'] + `</td>
                <td>` + phrase['object'] + `</td>
            </tr>
        `
        $('#phrasesBody').append(html)
    })
    initialize()
}

$(document).ready(function() {
    $.getJSON(origin + '/get_phrases', function(res) {
        phrases = res;
        populate()
    })
})
