$(document).ready(function() {
    $('#create_button').click(function() {
        $.post({
            url: '/api/deck',
            data: JSON.stringify({
                'name': $('#name').val(),
                'description': $('#description').val(),
                'owner_id': $('#owner_id').val()
            }),
            contentType: 'application/json; charset=utf-8'
        }).done(function (response) {
            deck_id = response['id'];
            window.location.href = '/deck/' + deck_id
        });
    })
})