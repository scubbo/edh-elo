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
        actual_select.append('<option val="-1">Select Deck...</option>');
        for (deck of player_decks) {
            actual_select.append(`<option val="${deck.id}">${deck.name}</option>`);
        }
        // Just in case it's been previously hidden
        actual_select.show();
        
    }
}

function initialize_dropdowns() {
    console.log('TODO - initialize dropdowns');
}

$(document).ready(function() {
    $('#number_of_players').on("change", change_num_players)
    $('.player_select').on("change", change_player)


    initialize_dropdowns()
    // TODO - initialize dropdowns

    // TODO - submit logic should:
    // * Check that Players are unique
});