from datetime import *
import math

FRAME_DETAL = 0.1

def get_cur_time_str():
	return str(datetime.now()).split(' ')[1]

def move_to_next_pos(pos_a, pos_b, speed):
	dx = pos_a[0]
	dy = pos_a[1]
	cx = pos_b[0]
	cy = pos_b[1]
	ts = math.sqrt((dx-cx)**2 + (dy-cy)**2)
	if ts <= speed:
		_x = dx
		_y = dy
	else:
		_x = cx + (dx - cx) * speed / ts
		_y = cy + (dy - cy) * speed / ts
	return _x, _y