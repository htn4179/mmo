# -*- coding: utf-8 -*-
class ServerPlayer(object):
	def __init__(self, _x, _y, _name, _speed, _uid, _client):
		self.x = _x
		self.y = _y
		self.name = _name
		self.speed = _speed
			
		self.uid = _uid
		self.client = _client
		self.target_x = self.x
		self.target_y = self.y

		self.frame_no = 0
		self.cmd_cache = []

	def set_frame_no(self, frame_no):
		self.frame_no = frame_no

	def get_client_dict(self):
		cdic = {
		'x': self.x,
		'y': self.y,
		'name': self.name,
		'speed': self.speed,
		'uid': self.uid,
		}
		return cdic