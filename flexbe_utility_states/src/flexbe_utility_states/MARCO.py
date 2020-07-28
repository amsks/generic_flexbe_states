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
		super(Carbonara, self).__init__(outcomes=['done'], input_keys=['input_value'], output_keys=['closest_object'])
		
		self.ordered_list = []



	def execute(self, userdata):

		if(self.ordered_list[0].z<3.5):
			userdata.closest_object = str(self.ordered_list[0].Class)
			# nothing to check
			return 'done'

	


	def on_enter(self, userdata):

		self.ordered_list = sorted(userdata.input_value.bounding_boxes, key=self.extract_z)

		#for item in ordered_list:
		#	Logger.logwarn('ELEMENT: %s' % str(item.z))
		Logger.logwarn('ELEMENT: %s' % str(self.ordered_list[0].Class))
		Logger.logwarn('at distance: %s' % str(self.ordered_list[0].z))
		#userdata.closest_object = ordered_list[0]



	def on_exit(self, userdata):
		pass



	def extract_z(self, elem):
		return elem.z
