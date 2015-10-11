import mancParam as param
import copy

class Game:
	def __init__(self, state, method, player_turn, depth):
		self.currentState = state
		self.method = method
		self.playTurn = player_turn
	
	def play(self):
		self.print_state()
	
	def nxtGreedyMv(self):
		pass
	
	def nxtMnmxMv(self):
		pass
		
	def nxtABMv(self):
		pass
	
	def print_state(self):
		self.currentState.print_info()
	
	def distribute(self, pseudoState, play_turn, pitid):
		pl_list = {}
		pl_score = {}
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
				if playerId == 2:
					next_pit_id = 1
					playerId = 1
				else
					next_pit_id = totalPits -1
					playerId = 2
		
class GameState:
	def __init__(self, players):
		self.players = players  #dictionary for holding player objects
		
	#for 2 player game it will be playerId - other_playerId
	def evaluate(self, plyId, stateObj):
		players = stateObj.players
		othrPlyId = (playerId + 1) % 2 # for 2 players game.
		return players[plyId].score - players[othrPlyId].score
	
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