#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flexbe_states.subscriber_state import SubscriberState
from flexbe_utility_states.MARCO import Carbonara
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Mon Aug 17 2020
@author: Aditya
'''
class Main_NewSM(Behavior):
	'''
	New integration test
	'''


	def __init__(self):
		super(Main_NewSM, self).__init__()
		self.name = 'Main_New'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:1569 y:533, x:771 y:388
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.input_value = 1

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:106 y:98
			OperatableStateMachine.add('detect_object',
										SubscriberState(topic='/darknet_ros/bounding_boxes', blocking=True, clear=False),
										transitions={'received': 'Determine_Course', 'unavailable': 'failed'},
										autonomy={'received': Autonomy.Off, 'unavailable': Autonomy.Off},
										remapping={'message': 'detected'})

			# x:101 y:301
			OperatableStateMachine.add('Determine_Course',
										Carbonara(),
										transitions={'none': 'failed', 'Obstacle': 'failed', 'Left': 'failed', 'Right': 'failed'},
										autonomy={'none': Autonomy.Off, 'Obstacle': Autonomy.Off, 'Left': Autonomy.Off, 'Right': Autonomy.Off},
										remapping={'input_value': 'detected', 'Distance': 'Distance'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
