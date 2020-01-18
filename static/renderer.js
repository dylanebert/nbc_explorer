var origin = window.location.origin
var phrases;

function loadVideo(idx) {
    $.getJSON(origin + '/get_images?idx=' + idx, function(res) {
        $('#main').append(`<div id="player" class="imageplayer"></div>`)
        $.each(res, function(i, url) {
            let line = `<img src="` + url + `"/>`
            $('#player').append(line)
        })
        $('#player').imgplay({rate: 30}).data('imgplay').play()
    })
}

function select(id) {
    let idx = parseInt(id.replace('phrase-', ''))
    let phrase = phrases[idx]
    $.getJSON(origin + '/get_phrase?idx=' + idx, function(res) {
        $('#main').empty()
        if (phrase['object'] == null) {
            $('#main').append('<h1>' + idx + ': ' + phrase['verb'] + '</h1>')
        } else {
            $('#main').append('<h1>' + idx + ': ' + phrase['verb'] + ' (' + phrase['object'] + ')</h1>')
        }
        $('#main').append('<h3><b>Phrase:</b> ' + res['phrase'] + '</h3>')
        $('#main').append('<p><b>Caption:</b> ' + res['caption'] + '</p>')
        $('#main').append('<p>' + res['start_step'] + ' - '+ res['end_step'] + '</p>')
        loadVideo(idx)
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
