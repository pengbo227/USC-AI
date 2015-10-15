import mancParam as param
import copy
import mancMethods as method

class Game:
    def __init__(self, state, method, player_turn, depth, totalPits):
        self.currentState = state
        self.method = method
        self.playTurn = player_turn
        self.totalPits = totalPits
        self.maxDepth = depth
    
    def play(self):
        stateObj = self.call_method(self.currentState, self.playTurn)
        print '\nnew state selected\n'
        stateObj.print_info()
        #print output state
        fobj = open('next_state.txt','w')
        line = self.__output_pits_state(stateObj, param.PLAYER_ID2)
        fobj.write(line + '\n')
        line = self.__output_pits_state(stateObj, param.PLAYER_ID1)
        fobj.write(line + '\n')
        self.__output_score(fobj, stateObj, param.PLAYER_ID2)
        self.__output_score(fobj, stateObj, param.PLAYER_ID1)
        fobj.close()
        
    def __output_score(self, fobj, state, playerId):
        score = state.players[playerId].score
        line = str(score) + '\n'
        fobj.write(line)
        
        
    def __output_pits_state(self, state, playerId):
        line = ''
        pitsDict = state.players[playerId].pitsList
        pitsKeyList = sorted(pitsDict)
        for key in pitsKeyList:
            line=line+str(pitsDict[key]) + ' '
        line.strip()
        print 'board state - player id:', playerId, ' :',line 
        return line
        
    
    def call_method(self, stateObj, play_turn, nodeName=None):
        valid_pits_list = stateObj.players[play_turn].get_valid_list()
        if self.method == param.TASK_OPTION['GREEDY']:
            newState = self.nxtGreedyMv(stateObj, valid_pits_list)
        elif self.method == param.TASK_OPTION['MINIMAX']:
            if nodeName == None:
                nodeName = 'root'
            score, newState = self.nxtMnmxMv(nodeName, stateObj, param.MAX_NODE, 0, valid_pits_list, play_turn)
            
        elif self.method == param.TASK_OPTION['ALPHABETA']:
            pit_id, newState = self.nxtABMv(stateObj, valid_pits_list)
        else:
            return None, None
        return newState
    
    def nextState(self, stateObj, play_turn, pitid):    
        total_pits = self.totalPits
        (free_turn, next_pit_id, playerId, pl_list, pl_score) = self.distribute(stateObj, play_turn, pitid)
        # if free_turn:
            # print 'pl_list',pl_list
            # print 'next_pid',next_pit_id
            # print 'score',pl_score
            
        if not free_turn:
            #check if the last updated pit has count == 1
            if next_pit_id == 0:
                if playerId ==1:
                    last_filled_pit = total_pits
                elif playerId ==2:
                    last_filled_pit = 1
            else:
                if playerId == 1:
                    last_filled_pit = next_pit_id -1
                elif playerId == 2:
                    last_filled_pit = next_pit_id + 1
        
            #Now check if last update was in same half and count ==1
            valid_players = [1,2]
            if playerId == play_turn:
                real_id = playerId
                valid_players.remove(real_id)
                opp_id = valid_players[0]
                if pl_list[real_id][last_filled_pit] == 1:
                    pl_score[real_id]= pl_score[real_id] + pl_list[opp_id][last_filled_pit] + 1
                    pl_list[opp_id][last_filled_pit] = 0
                    pl_list[real_id][last_filled_pit] = 0
                    
        #create new pseudostate and recur
        #1. Create Player objects
        pl1 = GamePlayer(param.PLAYER_ID1, pl_list[param.PLAYER_ID1], pl_score[param.PLAYER_ID1])
        pl2 = GamePlayer(param.PLAYER_ID2, pl_list[param.PLAYER_ID2], pl_score[param.PLAYER_ID2])
        players = {}
        players[param.PLAYER_ID1] = pl1
        players[param.PLAYER_ID2] = pl2
        pseudoState = GameState(players)
        if free_turn and self.method ==  param.TASK_OPTION['MINIMAX']:
            pseudoState.freeTurn = True
            
            
        if free_turn and self.method ==  param.TASK_OPTION['GREEDY']:
            print 'free turn'
            #pseudoState.print_info()
            pseudoState = self.call_method(pseudoState, play_turn)
            #print 'state after free turn'
            #pseudoState.print_info()
            return pseudoState
        return pseudoState
    
    def nxtGreedyMv(self, stateObj, valid_pits_list):
        next_pstate = {}
        #get only valid moves
        for pit_id in valid_pits_list:
            print 'greedy pit_id:', pit_id
            next_pstate[pit_id] = self.nextState(stateObj, self.playTurn, pit_id)
        print '\noriginal state before evaluating'
        stateObj.print_info()
        pit_id = self.batch_evaluate(next_pstate)
        print 'pit selcted by greedy',pit_id
        #next_pstate[pit_id].print_info()
        return next_pstate[pit_id] 
    
    def batch_evaluate(self, stateList):
        #print 'stateList', stateList
        if self.playTurn == param.PLAYER_ID1:
            keyList = sorted(stateList)
        else:
            keyList = sorted(stateList, reverse=True)
        max_val = 0
        max_pid = 0
        for key in keyList:
            print '\nbatch evaluating key:',key
            stateList[key].print_info()
            score = self.evaluate(self.playTurn, stateList[key])
            if score > max_val:
                max_val = score
                max_pid = key
        if max_pid == 0:
            max_pid = keyList[0]
        return max_pid
    
    #1. If free turn then
           #case 1.a: if node_type == Min then return Max
           #case 1.b: if node_type == Max then return Min
        #2. If not free turn then
            #case 2.a: if node_type == Min then return Min
            #case 2.b: if node_type == Max then return Max
        #print '\n\nNodename:',nodeName, 'valid list:', valid_pits_list, 'current_depth',current_depth,'freeTurn',currentState.freeTurn, \
                #'play_turn',play_turn
    
    def nxtMnmxMv(self, nodeName, currentState, nodeType, current_depth, valid_pits_list, play_turn):
        #print currentState.print_info()
        returnValList = []
        returnStateList = []
        currentState.depth = current_depth
        if current_depth == self.maxDepth:
            # as lst depth evaluate and print
            eval_val = self.evaluate(self.playTurn, currentState)
            
            print nodeName, ',', current_depth, ',', eval_val
            if not currentState.freeTurn:
                return eval_val, currentState
            else: #if current state is free turn the return opposite value than its nodetype
                #what to do if terminating node extends
                # go through the valid pits list and call minimax
                for pit_id in valid_pits_list:
                    child_state = self.nextState(currentState, play_turn, pit_id)
                    child_valid_pits_list = []
                    next_depth = current_depth
                    if child_state.freeTurn:
                        #calculate the valid_pits_list for the child
                        child_valid_pits_list = child_state.players[play_turn].get_valid_list()
                    val, ret_state = self.nxtMnmxMv(method.get_node_name(play_turn, pit_id), \
                        child_state, nodeType, next_depth, child_valid_pits_list, play_turn)
                    returnValList.append(val)
                    returnStateList.append(ret_state)
                    print nodeName, ',',current_depth, ',', method.return_opposite_type(nodeType, returnValList)
                ret_val = method.return_opposite_type(nodeType, returnValList)
                idx = returnValList.index(ret_val) 
                if (returnStateList[idx].depth > currentState.depth) and currentState.depth!=0:
                    ret_state = currentState
                else:
                    ret_state = returnStateList[idx]
                return ret_val,ret_state
        
        else:
        #if current_depth!=maxDepth
            if nodeType == param.MAX_NODE:
                if currentState.freeTurn:
                    print nodeName, ',', current_depth, ',',param.NODE_TYPE_STR[param.MAX_NODE]
                else:
                    print nodeName, ',', current_depth, ',',param.NODE_TYPE_STR[param.MAX_NODE]
            else:
                if currentState.freeTurn:
                    print nodeName, ',', current_depth, ',',param.NODE_TYPE_STR[param.MAX_NODE]
                else:
                    print nodeName, ',', current_depth, ',',param.NODE_TYPE_STR[param.MIN_NODE]
            
            if currentState.freeTurn:
                #it will pass same nodetype, depth to child
                #valid pit list should from the same play_turn as it will now be extended
                for pit_id in valid_pits_list:
                    opponent_turn = method.get_opponent_id(play_turn)
                    child_state = self.nextState(currentState, play_turn, pit_id)
                    #child_valid_pits_list = child_state.players[play_turn].get_valid_list()
                    next_depth = current_depth
                    next_node_type = nodeType
                    if child_state.freeTurn:
                        child_valid_pits_list = child_state.players[play_turn].get_valid_list()
                        next_play_turn = play_turn
  
                    else:
                        child_valid_pits_list = child_state.players[opponent_turn].get_valid_list()
                        next_play_turn = opponent_turn
                        
                    val, ret_state = self.nxtMnmxMv(method.get_node_name(play_turn, pit_id), child_state, next_node_type,\
                                next_depth, child_valid_pits_list, next_play_turn)
                    returnValList.append(val)
                    returnStateList.append(ret_state)
                    #this node is free_turn so will return opposite vals from its node type
                    print nodeName, ',',current_depth, ',', method.return_opposite_type(nodeType, returnValList)
                ret_val = method.return_opposite_type(nodeType, returnValList)
                idx = returnValList.index(ret_val)
                if (returnStateList[idx].depth > currentState.depth) and currentState.depth!=0:
                    ret_state = currentState
                else:
                    ret_state = returnStateList[idx]
                return ret_val,ret_state
                
            else:
                #valid_pits_list should be the opponents valid pit list
                for pit_id in valid_pits_list:
                    opponent_turn = method.get_opponent_id(play_turn)
                    child_state = self.nextState(currentState, play_turn, pit_id)
                    #print 'child_state\n',child_state.print_info()
                    if child_state.freeTurn:
                        child_valid_pits_list = child_state.players[play_turn].get_valid_list()
                        next_play_turn = play_turn
                        next_depth = current_depth+1
                    else:
                        child_valid_pits_list = child_state.players[opponent_turn].get_valid_list()
                        next_play_turn = opponent_turn
                        next_depth = current_depth+1
                    val, ret_state = self.nxtMnmxMv(method.get_node_name(play_turn, pit_id), child_state, method.alternate_type(nodeType),\
                                next_depth, child_valid_pits_list, next_play_turn)
                    returnValList.append(val)
                    returnStateList.append(ret_state)
                    # this node is not free_turn --> so return same as nodetype
                    print nodeName, ',',current_depth, ',', method.return_same_type(nodeType, returnValList)
                ret_val = method.return_same_type(nodeType, returnValList)
                idx = returnValList.index(ret_val)
                if (returnStateList[idx].depth > currentState.depth) and currentState.depth!=0:
                    ret_state = currentState
                else:
                    ret_state = returnStateList[idx]
                return ret_val,ret_state
        
    def nxtABMv(self):
        pass
    
    def print_state(self):
        self.currentState.print_info()
    
    #for 2 player game it will be playerId - other_playerId
    def evaluate(self, plyId, pseudoStateObj):
        players = pseudoStateObj.players
        valid_players = [1,2]
        valid_players.remove(plyId)
        othrPlyId = valid_players[0]
        return players[plyId].score - players[othrPlyId].score
    
    def distribute(self, pseudoState, play_turn, pitid):
        pl_list = {}
        pl_score = {}
        free_turn = False
        totalPits = self.totalPits + 1
        pl_list[param.PLAYER_ID1] = copy.deepcopy(pseudoState.players[param.PLAYER_ID1].pitsList)
        pl_score[param.PLAYER_ID1] = pseudoState.players[param.PLAYER_ID1].score        
        pl_list[param.PLAYER_ID2] = copy.deepcopy(pseudoState.players[param.PLAYER_ID2].pitsList)
        pl_score[param.PLAYER_ID2] = pseudoState.players[param.PLAYER_ID2].score
        
        if play_turn == 1:
            step = 1
            playerId = 1
        elif play_turn == 2:
            step = -1
            playerId = 2
        
        stone_count = pl_list[play_turn][pitid]
        #print 'pitid ',pitid, ' stones:',stone_count
        
        #emptying the stones from selected pitid
        pl_list[play_turn][pitid] = 0
        next_pit_id = (pitid + step) % totalPits 
        while stone_count!=0:
            free_turn = False
            while next_pit_id!=0 and stone_count!=0:
                pl_list[playerId][next_pit_id]+=1
                stone_count-=1
                next_pit_id = (next_pit_id + step) % totalPits
            if stone_count==0:
                break
            else:
                if playerId == play_turn:
                    pl_score[play_turn]+=1
                    stone_count-=1
                    free_turn = True
                if playerId == param.PLAYER_ID2:
                    next_pit_id = 1
                    playerId = 1
                    step = 1
                else:
                    next_pit_id = totalPits -1
                    playerId = 2
                    step = -1
        return (free_turn, next_pit_id, playerId, pl_list, pl_score) 
    
    def get_pits_valid_state(self, stateObj, play_turn):
        player = stateObj.players[play_turn]
        return player.get_valid_list()
        
class GameState:
    def __init__(self, players):
        self.players = players  #dictionary for holding player objects against their ID
        self.freeTurn = False #indicates whether we have to continue playing 
        self.depth = None
        
    def print_info(self):
        for pid in sorted(self.players,reverse=True):
            self.players[pid].print_info() 
    
class GamePlayer:
    def __init__(self, id, pitsList, score):
        self.id = id
        self.pitsList = pitsList
        self.score = score
        self.pitsCount = len(pitsList)
    
    def hasValidMoves(self):
        return len(self.get_valid_list()) == 0
        
    def get_valid_list(self):
        valid = []
        for i in range(self.pitsCount):
            if self.pitsList[i+1]!=0:
                valid.append(i+1)
        return valid
    
    def print_info(self):
        #print 'Player Id:', self.id
        print 'score', self.score
        #print 'pits count', len(self.pitsList)
        print 'Player Id:', self.id, 'pitlist:', self.pitsList
