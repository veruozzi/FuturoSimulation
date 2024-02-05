import Sofa.Core
from Sofa.constants import *
"""
functionDict = {
	# Arrows
	Key.leftarrow : lambda:print("You pressed the left arrow"),
	Key.rightarrow : lambda:print("You pressed the right arrow"),
	Key.uparrow : lambda:print("You pressed the up arrow"),
	Key.downarrow : lambda:print("You pressed the down arrow"),
	# Special caracters
	Key.space: lambda:print("You pressed the space"),
	Key.plus: lambda:print("You pressed the plus"),
	Key.minus: lambda:print("You pressed the minux"),
	# Letters
	Key.I: lambda:print("You pressed the letter I"),
	# KeyPad
	Key.KP_0: lambda:print("You pressed the number 0 on the keypad"),
	Key.KP_1: lambda:print("You pressed the number 1 on the keypad"),
	Key.KP_2: lambda:print("You pressed the number 2 on the keypad"),
	Key.KP_3: lambda:print("You pressed the number 3 on the keypad"),
	Key.KP_4: lambda:print("You pressed the number 4 on the keypad"),
	Key.KP_5: lambda:print("You pressed the number 5 on the keypad"),
	Key.KP_6: lambda:print("You pressed the number 6 on the keypad"),
	Key.KP_7: lambda:print("You pressed the number 7 on the keypad"),
	Key.KP_8: lambda:print("You pressed the number 8 on the keypad"),
	Key.KP_9: lambda:print("You pressed the number 9 on the keypad")
		}


class KeyPressedController(Sofa.Core.Controller):

    def __init__(self, *args, **kwargs):
        Sofa.Core.Controller.__init__(self, *args, **kwargs)

        self.listening = True
        self.name = "keyPressedController"
	

    def onKeypressedEvent(self, event):
        if event['key'] in functionDict:
            functionDict[event['key']]()
        else:
            print("You pressed the key : " + event['key'])

    def onKeyreleasedEvent(self, event):
        print("You released a key!")
"""


class RotationController(Sofa.Core.Controller):
	""" This is a custom controller to perform actions when events are triggered """

	def __init__(self, *args, **kwargs):
		# These are needed (and the normal way to override from a python class)
		Sofa.Core.Controller.__init__(self, *args, **kwargs)
		print(" Python::__init__::" + str(self.name.value))

		self.engine = kwargs["tool"]

		self.inited = 0
		self.axe = 3
		self.iterations = 0
		self.step = 1
		self.max_iterations = 360
		self.other_direction = False
		self.move = 0

	def onAnimateBeginEvent(self, eventType):
		with self.engine.tooldofs.position.writeableArray() as pos:
			if self.axe == 1:
				pos[:,1] += self.step
			elif self.axe == 2:
				pos[:,2] += self.step
			elif self.axe == 0:
				pos[:,0] += self.step


	def onEvent(self, event):
		pass

	# print ("Different event in Sofa : "+str(event))

	def onKeypressedEvent(self, c):
		key = c['key']
		if key == "1":
			print("moving increasing X ")
			self.axe = 0
			self.step = 1

		if key == "2":
			print("moving decreasing X ")
			self.axe = 0
			self.step = -1

		if ord(key) == 19:  # up
			print("moving up on Y ")
			self.axe = 1
			self.step = 1

		if ord(key) == 21:  # down
			print(" moving down on Y ")
			self.axe = 1
			self.step = -1

		if ord(key) == 18:  # left
			print(" moving increasing Z ")
			self.axe = 2
			self.step = 1

		if ord(key) == 20:  # right
			print(" moving decreasing Z ")
			self.axe = 2
			self.step = -1


	def onKeyreleasedEvent(self, event):
		self.axe = 3

