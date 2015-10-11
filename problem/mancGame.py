import mancParam as param
import copy

class Game:
	def __init__(self, state, method, player_turn, depth, totalPits):
		self.currentState = state
		self.method = method
		self.playTurn = player_turn
		self.totalPits = totalPits
	
	def play(self):
		stateObj = self.call_method(self.currentState)
		
	
	def call_method(self, stateObj)
		if self.method == param.TASK_OPTION['GREEDY']:
			self.nxtGreedyMv(stateObj)
		elif self.method == param.TASK_OPTION['MINIMAX']:
			self.nxtMnmxMv(stateObj)
		elif self.method == param.TASK_OPTION['ALPHABETA']
			self.nxtABMv(stateObj)
		else:
			pass
	
	def nextState(self, stateObj, play_turn, pitid):	
		total_pits = stateObj.players[1].pitsCount
		(free_turn, next_pit_id, playerId, pl_list, pl_score) = self.distribute(stateObj, play_turn, pitid)
			
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
		
			#Now check if there is lone count in last filled pit
			real_id = playerId-1
			opp_id = (real_id + 1) % 2
			if pl_list[real_id][last_filled_pit - 1] == 1:
				pl_score[real_id]= pl_score[real_id] + pl_list[opp_id][last_filled_pit - 1] + 1
				pl_list[opp_id][last_filled_pit - 1] = 0
				pl_list[real_id][last_filled_pit - 1] = 0
		#create new pseudostate and recur
		#1. Create Player objects
		pl1 = GamePlayer(param.PLAYER_ID1, pl_list[PLAYER_ID[1]], pl_score[PLAYER_ID[1]])
		pl2 = GamePlayer(param.PLAYER_ID2, pl_list[PLAYER_ID[2]], pl_score[PLAYER_ID[2]])
		players = {}
		players[param.PLAYER_ID[1]] = pl1
		players[param.PLAYER_ID[2]] = pl2
		pseudoState = GameState(players)
		if free_turn:
			return self.call_method(pseudoState)
		else
			return self.evaluate(play_turn, pseudoState)
	
	def nxtGreedyMv(self, stateObj):
		next_move_eval = {}
		for i in range(self.totalPits):
			pit_id = i+1
			next_move_eval[pit_id] = 0
			free_turn, pseudoStateObj = self.nextState(stateObj, self.playTurn, pit_id)
			if free_turn:
				next_move_eval[pit_id] = self.nxtGreedyMv(pseudoStateObj)
			else:
				next_move_eval[pit_id] = self.evaluate(self.playTurn, pseudoStateObj)
		
	
	def nxtMnmxMv(self):
		pass
		
	def nxtABMv(self):
		pass
	
	def print_state(self):
		self.currentState.print_info()
	
	#for 2 player game it will be playerId - other_playerId
	def evaluate(self, plyId, pseudoStateObj):
		players = pseudoStateObj.players
		othrPlyId = (playerId + 1) % 2 # for 2 players game.
		return players[plyId].score - players[othrPlyId].score
	
	def distribute(self, pseudoState, play_turn, pitid):
		pl_list = {}
		pl_score = {}
		free_turn = False
		totalPits = len(pseudoState.players[param.PLAYER_ID[1]].pitsCount + 1
		pl_list[param.PLAYER_ID[1]] = copy.deepcopy(pseudoState.players[param.PLAYER_ID[1]].pitsList
		pl_score[param.PLAYER_ID[1]] = pseudoState.players[param.PLAYER_ID[1]].score		
		pl_list[param.PLAYER_ID[2]] = copy.deepcopy(pseudoState.players[param.PLAYER_ID[2]].pitsList
		pl_score[param.PLAYER_ID[2]] = pseudoState.players[param.PLAYER_ID[2]].score
		
		if play_turn == 1:
			step = 1
			playerId = 1
		elif play_turn == 2:
			step = -1
			playerId = 2
		
		stone_count = pl_list[param.PLAYER_ID[play_turn]][pitid]
		next_pit_id = (pitid + step) % totalPits 
		while stone_count!=0:
			free_turn = False
			while next_pit_id!=0 and stone_count!=0:
				p1_list[param.PLAYER_ID[playerId]][next_pit_id-1]+=1
				stone_count-=1
				next_pit_id = (next_pit_id + step) % totalPits
			if stone_count==0:
				break
			else:
				if playerId == play_turn:
					pl_score[param.PLAYER_ID[play_turn]]+=1
					stone_count-=1
					free_turn = True
				if playerId == 2:
					next_pit_id = 1
					playerId = 1
				else
					next_pit_id = totalPits -1
					playerId = 2
		return (free_turn, next_pit_id, playerId, pl_list, pl_score) 
		
		
class GameState:
	def __init__(self, players):
		self.players = players  #dictionary for holding player objects
	def print_info(self):
		for pid in self.players:
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
		for i in range(len(self.pitsList)):
			if self.pitsList[i]!=0:
				valid.append(i)
		return valid
	
	def print_info(self):
		print 'Player Id:', self.id
		print 'score', self.score
		print 'pits count', len(self.pitsList)
		print 'pitlist:', self.pitsList

		
'''		
class Pit:
	def __init__(self, count, playerId):
		self.currentCount = count
		self.palyer = playerId
		#self.initialCount = count
	
	def isEmpty(self):
		return self.count == 0
	
	def 
'''