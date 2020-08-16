#!/usr/bin/env python

from flexbe_core import EventState, Logger
import rospy

from flexbe_core.proxy import ProxyPublisher
from geometry_msgs.msg import PoseStamped


class ObjectRecognition(EventState):
	"""
		Tokyo! 

	-- topic 		string 			Topic to which the pose will be published.

	># pose			PoseStamped		Pose to be published.

	<= done							Pose has been published.

	"""
	
	def __init__(self):
		"""	Constructor
		"""
		super(ObjectRecognition, self).__init__(outcomes=['Left_Sign', 'Right_Sign', 'Roadworks', 'Slippery_Road', 'Turn_Left_Sign', 'Turn_Right_Sign', 'Charging_Station', 'Stop_Sign', 'Parking_Sign', 'Parking_Spot', 'none'], input_keys=['input_value'])
		
		self.sign_list = ['Left_Sign', 'Right_Sign', 'Roadworks', 'Slippery_Road', 'Turn_Left_Sign', 'Turn_Right_Sign', 'Charging_Station', 'Stop_Sign', 'Parking_Sign', 'Parking_Spot']



	def execute(self, userdata):

		return self.output

	


	def on_enter(self, userdata):

		if(userdata.input_value[0] == 'Obstacle'):
			self.output = self.input_value
		elif(userdata.input_value[0] not in self.sign_list):
			self.output = 'none'
		else:
			self.output = str(userdata.input_value[0])



	def on_exit(self, userdata):
		pass
