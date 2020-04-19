from enum import Enum

class Side(Enum):
	'''
	Values of the enum are used throughout the code for indexing purposes, not to be changed
	'''
	Undef = -1
	Left  = 0
	Right = 1

	def opposite(self):
		return Side.Right if self is Side.Left else Side.Left