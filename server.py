# -*- coding: utf-8 -*-
import common
import asyncore, socket
import threading
import clientlogic
import sys
import cPickle
from ServerEntity import *
import Timer
import asyncore_with_timer

class ClientHandler(asyncore.dispatcher):
	def __init__(self, sock, peername, owner):
		asyncore.dispatcher.__init__(self, sock)
		self.sock = sock
		self.peername = peername
		self.owner = owner
		self.wbuffer = []
		self.owner.handle_new_comm(self)
		

	def handle_read(self):
	    data = self.recv(8192)
	    if data:
			print data
			#self.wbuffer.append(data)
			cmd = cPickle.loads(data)
			self.owner.handle_cmd(cmd, self.peername)
			self.send(data)

	def send_cmd(self, cmd):
		self.wbuffer.append(cmd)

	def handle_write(self):
		print 32, self.wbuffer
		if len(self.wbuffer)> 0:
			print self.wbuffer
			_data = self.wbuffer[0]
			print _data
	    	sent = self.send(_data)
	    	self.wbuffer.remove(_data)
	
	def writable(self):
		return len(self.wbuffer) >0

	def handle_close(self):
		"""连接断开的时候回调"""
		print 'close socket'
		asyncore.dispatcher.handle_close(self)
		asyncore.dispatcher.close(self)


class Server(asyncore.dispatcher):

	def __init__(self, host, port, owner):
	    asyncore.dispatcher.__init__(self)
	    self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
	    self.set_reuse_addr()
	    self.bind((host, port))
	    self.listen(5)
	    self.buffer = []
	    self.readbuf = []
	    self.host = host
	    self.port = port
	    self.owner = owner

	def handle_accept(self):
	    pair = self.accept()
	    if pair is not None:
	        sock, addr = pair
	        print 'Incoming connection from %s' % repr(addr)
	        handler = ClientHandler(sock, addr, self.owner)

	def handle_close(self):
		#do something
		self.close()

	def handle_write(self):
		if len(self.buffer)> 0:
			data = self.buffer[0]
	    	sent = self.send(data)
	    	self.buffer.remove(data)

	def handle_read(self):
		data = self.recv(8192)
		if data:
			print data
			self.readbuf.append(data)

	

class ServerLogic(object):
	def __init__(self):
		self.clients = {}
		self.avatars = {}
		self.guid = 0
		self.server = Server('127.0.0.1', 8081, self)
		#服务器帧
		self.frame_num = 0


	def run(self):
		#每秒30
		Timer.addRepeatTimer(common.FRAME_DETAL, lambda: self.tick())
		# asyncore.loop()
		asyncore_with_timer.loop(0)

	def tick(self):
		for splayer in self.avatars.itervalues():
			if splayer.frame_no < self.frame_num+1:
				#等待玩家数据
				return
		self.frame_num += 1
		
		# print self.frame_num, common.get_cur_time_str()
		# print 'tick', common.get_cur_time_str()

	def handle_cmd(self, cmd, cid):
		_func, _args = cmd
		_args['cid'] = cid
		if hasattr(self, _func):
			getattr(self, _func)(**_args)



	def handle_new_comm(self, client):
		print 'new comm', client.peername
		self.clients[client.peername] = client
		#cmd = ('reg_user', {'uid': self.guid})
		#self.guid += 1
		#client.send_cmd(cPickle.dumps(cmd))
		#self.send_data(client, 'reg_user', {'uid': self.guid})
		#self.avatars[self.guid] = client.peername
		
	#----------------------------------------------------------cmd---
	def move_to(self,x,y, uid, cid):
		self.avatars[uid].target_x = x
		self.avatars[uid].target_y = y

		cmd = ('move_to', {'x':x, 'y':y, 'uid': uid})
		for suid, splayer in self.avatars.items():
			if suid != uid:
				self.clients[splayer.client].send_cmd(cPickle.dumps(cmd))
	
	def reg_to_server(self, name, cid):
		self.guid += 1
		cmd = ('reg_user', {'uid': self.guid})
		self.avatars[self.guid] = ServerPlayer(300, 0, name, clientlogic.g_speed, self.guid, cid)
		self.avatars[self.guid].set_frame_no(self.frame_num)
		self.send_data(self.clients[cid], 'reg_user', {'uid': self.guid, 'server_frame_no': self.frame_num})
		#告诉其他玩家
		for uid, splayer in self.avatars.items():
			_cid = splayer.client			
			if _cid != cid:
				self.send_data(self.clients[_cid], 'reg_other_user', {'info': self.avatars[self.guid].get_client_dict()})
				#其他玩家告诉我
				self.send_data(self.clients[cid], 'reg_other_user', {'info': splayer.get_client_dict()})
	
	#-----------------------------------common method -------------
	def send_data(self, client, method, args):
		cmd = (method, args)
		client.send_cmd(cPickle.dumps(cmd))
	

def main(argv):
	print 'MAIN SERVER:', argv
	server = ServerLogic()
	server.run()



if __name__ == '__main__':
	
	# import pydevd

	# pydevd.settrace('localhost', port=11113, stdoutToServer=False, stderrToServer=False)
	main(sys.argv)