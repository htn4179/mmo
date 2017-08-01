g_players = {}
g_player = 0
g_uid = g_player
g_speed = 20
g_wbuffer = []
g_rbuffer = []
g_name = None
g_server_frame = 0

import common
import cPickle

class Player(object):
	def __init__(self, _x = 0, _y = 0, _name = '', _speed = 0):
		self.x = _x
		self.y = _y
		self.name = _name

		self.target_x = self.x
		self.target_y = self.y
		self.speed = _speed
		
		self.uid = -1

		self.cmd_cache = []

	def init_from_dict(self, dic):
		for k, v in dic.items():
			if hasattr(self, k):
				setattr(self, k,v)
				print k, v , getattr(self, k)

	def update(self):
		self.x, self.y = common.move_to_next_pos((self.target_x, self.target_y), (self.x, self.y), self.speed)
		#g_wbuffer.append(cPickle.dumps(('move_to', {'x':self.x, 'y':self.y})))

	
	def reg_user(self, uid):
		self.uid = uid
		print 'reg_user', uid
		
	def update_target_pos(self, _x, _y):
		self.target_x = _x
		self.target_y = _y
		cmd = ('move_to', {'x': self.target_x, 'y': self.target_y, 'uid': self.uid})
		g_wbuffer.append(cPickle.dumps(cmd))

	def set_target_pos(self, _x, _y):
		self.target_x = _x
		self.target_y = _y