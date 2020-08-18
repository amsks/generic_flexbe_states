#!/usr/bin/env python

from flexbe_core import EventState, Logger
import rospy

from flexbe_core.proxy import ProxyPublisher
from geometry_msgs.msg import PoseStamped

import math

class Amatricianna(EventState):
	"""
		Delicious! 

	-- topic 		string 			Topic to which the pose will be published.

	># pose			PoseStamped		Pose to be published.

	<= done							Pose has been published.

	"""
	
	def __init__(self):
		"""	Constructor
		"""
		super(Amatricianna, self).__init__(outcomes=['Navigation', 'Parking'], input_keys=['curr_pose'], output_keys=['Direction'])
		
		self.parking_sign = [11.0, -3.0]

		self.decision = False

		self.distance


	def execute(self, userdata):

		if(self.distance > math.sqrt(5)):
			return 'Navigation'
		else:
			return 'Parking'



	def on_enter(self, userdata):

		# Extract the current pose
        curr_x = userdata.curr_pose.pose.position.x
        curr_y = userdata.curr_pose.pose.position.y
        curr_theta = transformations.euler_from_quaternion([0, 0, userdata.curr_pose.pose.orientation.z, userdata.curr_pose.pose.orientation.w])
		
		#Calculate the distance from the goal 
		sq_distance = math.pow((curr_x - self.parking_sign[0]),2) + math.pow((curr_y - self.parking_sign[1]),2)
		self.distance = math.sqrt(sq_distance)


	def on_exit(self, userdata):
		pass



	def extract_z(self, elem):
		return elem.z
