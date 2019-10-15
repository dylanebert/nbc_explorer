var origin = window.location.origin

function showDependencyTable(idx) {
    $.getJSON(origin + '/get_svo?idx=' + idx, function(svo) {
        $.each(svo, function(index, elems) {
            let html = `<tr>
                <td>` + index + `</td>
                <td>` + elems.token + `</td>
                <td>` + elems.lemma + `</td>
                <td>` + elems.dep + `</td>
                <td>` + elems.coref + `</td>
            </tr>`
            $('#dependencyTable').append(html)
        })
    })
}

function select(id) {
    var elems = id.split('%'); var participant = elems[0]; var task = elems[1];
    var caption = elems[2]; var idx = parseInt(elems[3]); var phrase = elems[4]
    let vidsrc = 'https://storage.cloud.google.com/nbc_release/phrases/' + idx + '.mp4'
    $('#main').empty()
    $('#main').append('<h1>' + phrase + '</h1>')
    $('#main').append('<h5>' + caption + '</h5>')
    $('#main').append('<video src="' + vidsrc + '" type="video/mp4" controls></video>')
    $('#main').append(`<table class="table"><thead><tr>
        <th>index</th><th>token</th><th>lemma</th><th>dep</th><th>coref</th>
    </tr></thead><tbody id="dependencyTable"></tbody></table>`)
    showDependencyTable(idx)
}

function initializeTable() {
    $('#phrasesTable').DataTable({
        initComplete: function() {
            this.api().columns([0, 1]).every(function() {
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
            this.api().columns([2]).every(function() {
                var column = this
                var input = $('<input type="text" placeholder="Search">')
                    .appendTo($(column.footer()).empty())
                    .on('keyup change clear', function() {
                        if(column.search() !== this.value) {
                            column.search(this.value).draw()
                        }
                    })
            })
        },
        'paging': false,
        'scrollY': '768px',
        'scrollCollapse': true
    })
    $('.dataTables_filter').css('display', 'none')
}

function populate(phrases) {
    $.each(phrases, function(participant, tasks) {
        $.each(tasks, function(task, captions) {
            $.each(captions, function(caption, phrases) {
                $.each(phrases, function(idx, phrase) {
                    let id = participant + '%' + task + '%' + caption + '%' + idx + '%' + phrase.phrase
                    let html = `
                        <tr id="` + id + `">
                            <td>` + participant + `</td>
                            <td>` + task + `</td>
                            <td>` + phrase.phrase + `</td>
                        </tr>
                    `
                    $('#phrasesBody').append(html)
                })
            })
        })
    })
    initializeTable()
    $('tbody tr').click(function(e) {
        e.preventDefault()
        select($(this).attr('id'))
    })
    $('tbody tr').hover(function() {
        $(this).css('background-color', '#eeeeee')
    }, function() {
        $(this).css('background-color', 'white')
    })
}

$(document).ready(function() {
    $.getJSON(origin + '/get_phrases', function(phrases) {
        populate(phrases)
    })
})
