#!/usr/bin/env python

from flexbe_core import EventState, Logger
import rospy

from flexbe_core.proxy import ProxyPublisher
from geometry_msgs.msg import PoseStamped

import math

class Battery_value(EventState):
	"""
		Delicious! 

	"""
	
	def __init__(self):
		"""	Constructor
		"""
		super(Battery_value, self).__init__(outcomes=['L_B', 'M_B', 'H_B'], input_keys=['battery_level'], output_keys=['Direction'])
		
		self.low_threshold = 40.0

		self.high_threshold = 90.0


	def execute(self, userdata):
		if(userdata.battery_level < self.low_threshold):
			return 'L_B'
		
		elif(userdata.battery_level	 > self.high_threshold):
			return 'H_B'

		else:
			return 'M_B'

		pass

	def on_enter(self, userdata):

		Logger.logwarn("Battery Level: %s" % str(userdata.battery_level))

	def on_exit(self, userdata):
		pass



	# def extract_z(self, elem):
	# 	return elem.z
