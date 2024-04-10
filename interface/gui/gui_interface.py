def get_move_message(player_name, chosen_move, board):
    card_string = board.get_card_string(chosen_move[0], chosen_move[1])
    return '{} moved to card {} at position {}'.format(player_name, card_string, chosen_move)


def get_swap_message(player_name, joker_position, card_position, board):
    card_string = board.get_card_string(card_position[0], card_position[1])
    return '{} swapped a [ Joker ] at position {} with card {} at position {}'.format(player_name,
                                                                                      joker_position,
                                                                                      card_string,
                                                                                      card_position)
