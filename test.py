import threading

buff=[]
def w():
	while True:
		buff.append('12345678901234567890')

t = threading.Thread(target=w)

t.start()

while True:
	if len(buff) >0:
		print buff
		buff = []
