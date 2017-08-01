# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import math
import time
from datetime import *
import common
import asyncore, socket
import threading
import clientlogic
import cPickle
import asyncore_with_timer, Timer



class EchoHandler(asyncore.dispatcher_with_send):

    def handle_read(self):
        data = self.recv(8192)
        if data:
            self.send(data)

class Client(asyncore.dispatcher):

	def __init__(self, host, port):
	    # asyncore.dispatcher.__init__(self)
	    asyncore.dispatcher.__init__(self, None)
	    self.peername = (host, port)
	    self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
	    # self.set_reuse_addr()
	    # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	    self.connect( self.peername )

	    # sock.setblocking(0)

	    # self.set_socket(sock)
	    # self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
	    self.w_buffer = []

	def handle_connect(self):
		print 'connected'
		cmd = ('reg_to_server', {'name': clientlogic.g_name})
		clientlogic.g_wbuffer.append(cPickle.dumps(cmd))


	def handle_read(self):
		"""读数据"""
		data = self.recv(4096)
		if data:
			cmd = cPickle.loads(data)
			print cmd
			#clientlogic.g_rbuffer.append(cmd)
			m, a = cmd
			if hasattr(self, m):
				getattr(self, m)(**a)

	def handle_write(self):
		"""数据可写"""
		if len(clientlogic.g_wbuffer) >0:
			data = clientlogic.g_wbuffer[0]
			sent = self.send(data)
			print 'send cnt', sent
			clientlogic.g_wbuffer.remove(data)
		# buff = self.w_buffer.getvalue()
		# if buff:
		# 	sent = self.send(buff)

	def handle_close(self):
		"""连接断开的时候回调"""
		asyncore.dispatcher.handle_close(self)
		print 'close'	

	#--------------------------------
	
	def reg_user(self, uid, server_frame_no):
		clientlogic.g_server_frame = server_frame_no
		clientlogic.g_players[0].uid = uid
		clientlogic.g_players[uid] = clientlogic.g_players[0]
		del clientlogic.g_players[0]
		clientlogic.g_player = uid
		print 'reg_user', uid
	
	def reg_other_user(self, info):
		clientlogic.g_players[info['uid']] = clientlogic.Player()
		clientlogic.g_players[info['uid']].init_from_dict(info)
		clientlogic.g_players[info['uid']].set_target_pos(clientlogic.g_players[info['uid']].x, clientlogic.g_players[info['uid']].y)
		print 'other', clientlogic.g_players[info['uid']].x

	def move_to(self, x, y, uid):
		clientlogic.g_players[uid].set_target_pos(x,y)

class ShapeWidget(QWidget):
	H = 500
	W = 900
	def __init__(self,parent=None):
		super(ShapeWidget,self).__init__(parent)
		palette1 = QtGui.QPalette(self)
		palette1.setColor(self.backgroundRole(), QColor(0,91,170))
		self.setPalette(palette1)
		self.setGeometry(400, 300, self.W, self.H)
		mylayout = QVBoxLayout()
		self.setLayout(mylayout)

		self.i = 1
		self.mypix()
		self.timer = QTimer()
		self.timer.setInterval(30)  # 500m秒秒
		self.timer.timeout.connect(self.timeChange)   
		self.timer.start()
		self.dragPosition=None
		self.cur_pos = None
		self.speed = 20
		
		cb = QtGui.QCheckBox('Show title', self)
		cb.move(20, 20)
		self.square = QtGui.QFrame(self)
		self.square.setGeometry(0, 0, 100, self.H)
		self.square.setStyleSheet("QWidget { background-color: Blue }")
		
		self.list = QListWidget(self)
		self.list.resize(300, self.H)
		for i in xrange(100):
			self.list.addItem('A use skill %s'%(common.get_cur_time_str()))
		
	
	def mypix(self):
		for _player in clientlogic.g_players.itervalues():
			_player.update()
		self.update()

	
	def mousePressEvent(self, event):
		if event.button() == Qt.LeftButton:
			print 'left button', datetime.now()
			event.accept()
		if event.button() == Qt.RightButton:
			self.close()
		self.dragPosition = event.globalPos()-self.frameGeometry().topLeft()
		clientlogic.g_players[clientlogic.g_player].update_target_pos(self.dragPosition.x(), self.dragPosition.y())
		#clientlogic.g_wbuffer.append(','.join([str(self.dragPosition.x()),str(self.dragPosition.y())]))
		#print event.globalPos().y(),  self.frameGeometry().topLeft().y()
		#print 11111,  dir(self.dragPosition)

	#def mouseMoveEvent(self, event):
	def paintEvent(self, event):
		painter = QPainter(self)
		#print 'event'
		p = QPainter(self)
		#p.begin(self)
		brush = QtGui.QBrush(QtCore.Qt.SolidPattern)
		p.setBrush(brush)

		
		# print 'WWWW'
		for _player in clientlogic.g_players.itervalues():
			# print 'HHHH', _player.x, _player.y
			# if not self.cur_pos:
			# 	_x = 350
			# 	_y = 350
			# else:
			# 	if not self.dragPosition:
			# 		_x = self.cur_pos.x()
			# 		_y = self.cur_pos.y()
			# 	else:
			# 		_x, _y = common.move_to_next_pos((self.dragPosition.x(), self.dragPosition.y()), (self.cur_pos.x(), self.cur_pos.y()), self.speed)
								
			rect = QRectF(_player.x, _player.y,50,50)
			# self.cur_pos = QPoint(_x, _y)
			
				
			p.drawRect(rect)
			if _player.uid == clientlogic.g_player:
				p.setPen(QColor(Qt.green))
			else:
				p.setPen(QColor(Qt.red))
			font = QFont('Arial',20,QFont.Bold,True)
			p.setFont(font)
			p.drawText(rect,Qt.AlignVCenter|Qt.AlignHCenter,_player.name)
		#p.end()
		#painter.drawPixmap(0, 0, self.pix.width(),self.pix.height(),self.pix)
 
	#每**秒修改paint
	def timeChange(self):
		self.i+=1
		self.mypix()


def net_thread():
	print 'begin loop'
	server = Client('localhost', 8081)
	# asyncore.loop()
	Timer.addRepeatTimer(common.FRAME_DETAL, lambda: tick())
	asyncore_with_timer.loop(0)
	print 'after loop'

def tick():
	pass
	# print 'client tick'

	
def main(argv):
	print 'MAIN:', argv
	clientlogic.g_name = argv[1]
	#client = HTTPClient('www.baidu.com', '/')
	# asyncore.loop()
	clientlogic.g_players[clientlogic.g_player] = clientlogic.Player(300,0, argv[1], clientlogic.g_speed)

	app=QApplication(sys.argv)
	form=ShapeWidget()
	form.show()
	
	t = threading.Thread(target=net_thread)

	t.start()
	# t.join()
	#asyncore.loop()
	print '158'
	app.exec_()
	print 'enddddd'



if __name__ == '__main__':
	
	# import pydevd

	# pydevd.settrace('localhost', port=11113, stdoutToServer=False, stderrToServer=False)
	main(sys.argv)