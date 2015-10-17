import mancParam as param

def get_node_name(playerId, pit_id):
    return param.PLAYER_LABEL[playerId] + str(pit_id+1)
 
def return_opposite_type(nodeType, return_list):
    if nodeType == param.MAX_NODE:
        return min(return_list);
    else:
        return max(return_list);

def return_same_type(nodeType, return_list):
    if nodeType == param.MAX_NODE:
        return max(return_list)
    else:
        return min(return_list)

def write_title(fobj, title):
    fobj.write(title)

def get_opponent_id(playId):
    #check whether removal makes changes in param.PLAYER_LIST
    if playId == param.PLAYER_ID1:
        return param.PLAYER_ID2
    else:
        return param.PLAYER_ID1

def alternate_type(nodeType):
    if nodeType == param.MAX_NODE:
        return param.MIN_NODE
    else:
        return param.MAX_NODE
        
def should_prune(alpha, beta):
    if beta > alpha:
        return False
    return True

def print_alphabeta(value):
    if value == param.PLUS_INFINITY:
        return param.NODE_TYPE_STR[param.MIN_NODE]
    elif value == param.MINUS_INFINITY:
        return param.NODE_TYPE_STR[param.MAX_NODE]
    else:
        return value
'''
 def return_alphabeta(returnValList, nodeType):
    if nodeType == param.MAX_NODE:
        return 
'''

def get_eval(nodeType, alpha, beta, isFreeturn):
    if not isFreeturn:
        if nodeType == param.MAX_NODE:
            return alpha
        else:
            return beta
    else:
        if nodeType == param.MAX_NODE:
            return beta
        else:
            return alpha

def intermediate_value(nodeType, isFreeturn):
    val = ''
    if isFreeturn:
        if nodeType == param.MAX_NODE:
            val = param.NODE_TYPE_STR[param.MIN_NODE]
        else:
            val = param.NODE_TYPE_STR[param.MAX_NODE]
    else:
        if nodeType == param.MAX_NODE:
            val = param.NODE_TYPE_STR[param.MAX_NODE]
        else:
            val = param.NODE_TYPE_STR[param.MIN_NODE]
    return val

def write_entry_log(nodeName, nodeType, max_depth, current_depth, alpha, beta, isFreeturn, eval_val=None, fobj=None):
    if max_depth == current_depth and not isFreeturn: #this is leaf
        print nodeName, ',', current_depth, ',', eval_val,',', print_alphabeta(alpha), ',', print_alphabeta(beta)
    else:
        eval_value = intermediate_value(nodeType, isFreeturn)
        print nodeName, ',', current_depth, ',', eval_val,',', print_alphabeta(alpha), ',', print_alphabeta(beta)
            
            