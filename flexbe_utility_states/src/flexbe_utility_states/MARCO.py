#!/usr/bin/env python

from flexbe_core import EventState, Logger
import rospy

from flexbe_core.proxy import ProxyPublisher
from geometry_msgs.msg import PoseStamped


class Carbonara(EventState):
	"""
		Delicious! 

	-- topic 		string 			Topic to which the pose will be published.

	># pose			PoseStamped		Pose to be published.

	<= done							Pose has been published.

	"""
	
	def __init__(self):
		"""	Constructor
		"""
		super(Carbonara, self).__init__(outcomes=['none', 'Obstacle', 'Left', 'Right' ], input_keys=['input_value'], output_keys=['output_value'])
		
		self.ordered_list = []

		self.decision_threshold = 4.5
		self.obstacle_threshold = 3.5



	def execute(self, userdata):


		if(self.ordered_list[0].Class == 'Object'):
			userdata.output_value = [self.ordered_list[0].Class, self.ordered_list[0].z]
			Logger.logwarn('ELEMENT obstacle: %s' % str(userdata.output_value))
			
			if(self.ordere_list[0].z > self.obstacle_threshold):
				return 'none'
			else:
				return 'Obstacle'

		elif(self.ordered_list[0].Class == 'Left_Sign'):
			if(self.ordered_list[0].z < self.decision_threshold):
				userdata.output_value = self.ordered_list[0].Class
				return 'Left'
			else:
				return 'none'

		elif(self.ordered_list[0].Class == 'Left_Sign'): 
			if(self.ordered_list[0].z < self.decision_threshold):
				userdata.output_value = self.ordered_list[0].Class
				return 'Right'
			else:
				return 'none'
		else:
			return 'none'
		# else:
		# 	userdata.output_value = self.ordered_list[0].Class
		# 	return 'continue'
	


	def on_enter(self, userdata):

		self.ordered_list = sorted(userdata.input_value.bounding_boxes, key=self.extract_z)

		#for item in ordered_list:
		#	Logger.logwarn('ELEMENT: %s' % str(item.z))
		Logger.logwarn('ELEMENT: %s' % str(self.ordered_list[0].Class))
		Logger.logwarn('at distance: %s' % str(self.ordered_list[0].z))
		#userdata.output_value = ordered_list[0]



	def on_exit(self, userdata):
		pass



	def extract_z(self, elem):
		return elem.z
