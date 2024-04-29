function change_num_players(eventData) {
    const num_players = $(eventData['target']).val();
    console.log('num_players ' + num_players)
    $('.player_div').each(function(_, elem) {
        id = elem.id;
        const player_id = parseInt(id.substring('div_for_player_'.length));
        if (player_id > num_players) {
            $(elem).hide();
        } else {
            $(elem).show();
        }
        
    })
}

function change_player(eventData) {
    target = $(eventData['target']);

    deck_select = target.siblings('.deck_select');
    console.log('Deck select is');
    console.log(deck_select);

    const target_val = parseInt(target.val());
    // Populate the per-player deck-choices
    if (target_val == -1) {
        deck_select.hide();
    } else {
        // A player has been selected. If the deck_select dropdown does not
        // already exist, create it. Either way, then (re-)populate it.
        if (deck_select.length == 0) {
            target.parent().append('<select class="deck_select"></select>');
            deck_select = target.siblings('.deck_select');
        }
        console.log('DEBUG - player_deck_data is');
        console.log($('#player_deck_data').val());
        player_deck_data = JSON.parse($('#player_deck_data').val());
        if (!(target_val.toString() in player_deck_data)) {
            alert(`Could not find player_id ${target_val} in player_deck_data.`)
            return;
        }
        player_decks = player_deck_data[target_val.toString()];
        actual_select = $(deck_select[0]);
        actual_select.empty();
        actual_select.append('<option value="-1">Select Deck...</option>');
        for (deck of player_decks) {
            actual_select.append(`<option value="${deck.id}">${deck.name}</option>`);
        }
        // Just in case it's been previously hidden
        actual_select.show();
    }

    // Update the "winning player" dropdown
    $('#winning_player_id').empty();
    $('.player_select').each(function () {
        if ($(this).val() != -1) {
            $('#winning_player_id').append(
                $('<option></option>')
                    .attr('value', $(this).val())
                    .text($(this).children("option:selected").text())
            )
        }
    });


}

$(document).ready(function() {
    $('#number_of_players').on("change", change_num_players)
    $('.player_select').on("change", change_player)
    
    $('#submit').click(function() {
        var data = {
            'date': $('#date').val(),
            'number_of_turns': $('#number_of_turns').val(),
            'first_player_out_turn': $('#first_player_out_turn').val(),
            'win_type_id': $('#win_type_id').val(),
            'description': $('#description').val()
        }
        winning_player_id = $('#winning_player_id option:selected').attr('value');
        data['winning_deck_id'] = getDeckForPlayerId(winning_player_id);

        for (i=0; i<$('#number_of_players').val(); i++) {
            data['deck_id_' + (i+1)] = $('#div_for_player_' + (i+1) + ' .deck_select option:selected').attr('value');
        }

        $.ajax({
            type: 'POST',
            url: '/api/game/',
            data: JSON.stringify(data),
            contentType: 'application/json',
            dataType: 'json',
            success: function(data) {
                window.location.href = '/game/' + data.id;
            }
        });
    });
});

function getDeckForPlayerId(player_id) {
    mapped = $('.player_div').map(function() {
        return {
            'player_id': $(this).find('.player_select option:selected').attr('value'),
            'deck_id': $(this).find('.deck_select option:selected').attr('value')
        }
    })

    filtered = mapped.filter((_, data) => parseInt(parseInt(data['player_id'])) == player_id)

    return filtered[0]['deck_id'];
}