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
			print self.players[pid].print_info()
	
class GamePlayer:
	def __init__(self, id, pitsList, score, pitsCnt):
		self.id = id
		self.pitsList = pitsList
		self.score = score
		self.pitCount = pitsCnt
	
	def print_info(self):
		print 'Player Id:', self.id
		print 'score', self.score
		print 'pits count', self.pitCount
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