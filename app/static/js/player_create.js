$(document).ready(function() {
    $('#create_button').click(function() {
        $.post({
            url: '/api/player',
            data: JSON.stringify({
                'name': $('#name').val()
            }),
            contentType: 'application/json; charset=utf-8'
        }).done(function (response) {
            player_id = response['id'];
            window.location.href = '/player/' + player_id
        });
    })
})