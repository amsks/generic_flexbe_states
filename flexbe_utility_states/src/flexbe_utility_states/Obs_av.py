#!/usr/bin/env python

from flexbe_core import EventState, Logger
import rospy

from flexbe_core.proxy import ProxyPublisher
from geometry_msgs.msg import PoseStamped


class Avoidance_Check(EventState):
	"""
		Delicious! 

	-- topic 		string 			Topic to which the pose will be published.

	># pose			PoseStamped		Pose to be published.

	<= done							Pose has been published.

	"""
	
	def __init__(self):
		"""	Constructor
		"""
		super(Avoidance_Check, self).__init__(outcomes=['Stop', 'Back', 'Done'], input_keys=['input_value'], output_keys=['Distance'])
		
		self.ordered_list = []

		self.obstacle_threshold = 3.5
		self.stop_threshold = 1.0



	def execute(self, userdata):


		if(self.ordered_list[0].Class == 'Obstacle'):
			# userdata.Distance = [self.ordered_list[0].Class, self.ordered_list[0].z]
			# Logger.logwarn('ELEMENT obstacle: %s' % str(userdata.Distance))
			
			if(self.ordered_list[0].z > self.obstacle_threshold):
				return 'Done'
			elif(self.ordered_list[0].z < self.stop_threshold):
				return 'Back'
			else:
				return 'Stop'

		else:
			return 'Done'
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
