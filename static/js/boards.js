$(document).on('submit', '.board-delete-form', e => {
    e.preventDefault()

    let form = $(e.target)
    $.ajax({
        url: form.attr('data-action'),
        data: form.serialize(),
        type: form.attr('method'),
        dataType: 'json',
        success: data => {
            if (data.form_is_valid)
                $('.table > tbody').html(data.html_board_list)
        },
        error: err => console.log(err)
    })

    return false
})


