import mancParam as param

def get_node_name(playerId, pit_id):
    return param.PLAYER_LABEL[playerId] + str(pit_id)