import asyncore_with_timer
def addTimer( delay, func, *args, **kwargs ):
	"""
	- (float) delay: the number of seconds to wait. The timer granularity
		depends on the timeout value of asyncore_with_timer.loop
	- (obj) func: the callable object to call later
	- args: the arguments to call it with
	- kwargs: the keyword arguments to call it with; a special
		'_errback' parameter can be passed: it is a callable
		called in case target function raises an exception.
	- return a timer object can reset or cancel
	"""
	return asyncore_with_timer.CallLater( delay, func, *args, **kwargs )

def addRepeatTimer( delay, func, *args, **kwargs ):
	"""
	- (float) delay: call it every 'delay' seconds
	- (obj) func: the callable object to call later
	- args: the arguments to call it with
	- kwargs: the keyword arguments to call it with; a special
		'_errback' parameter can be passed: it is a callable
		called in case target function raises an exception.
	- return a timer object can reset or cancel
	"""
	return asyncore_with_timer.CallEvery( delay, func, *args, **kwargs )

def tickTimer():
	pass