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
from flexbe_navigation_states.stop_sm import StopSM
from flexbe_utility_states.Obs_av import Avoidance_Check
from flexbe_navigation_states.go_back_sm import go_backSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Wed Jul 29 2020
@author: TG4
'''
class object_recognition_reactionSM(Behavior):
	'''
	object recognition reaction
	'''


	def __init__(self):
		super(object_recognition_reactionSM, self).__init__()
		self.name = 'object_recognition_reaction'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(StopSM, 'Stop')
		self.add_behavior(go_backSM, 'go_back')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:822 y:88, x:146 y:424
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:152 y:124
			OperatableStateMachine.add('s1',
										SubscriberState(topic='/darknet_ros/bounding_boxes', blocking=True, clear=False),
										transitions={'received': 'Obs_check', 'unavailable': 'failed'},
										autonomy={'received': Autonomy.Off, 'unavailable': Autonomy.Off},
										remapping={'message': 'input_value'})

			# x:846 y:355
			OperatableStateMachine.add('Stop',
										self.use_behavior(StopSM, 'Stop'),
										transitions={'finished': 'Obs_check', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:427 y:102
			OperatableStateMachine.add('Obs_check',
										Avoidance_Check(),
										transitions={'Stop': 'Stop', 'Back': 'go_back', 'Done': 'finished'},
										autonomy={'Stop': Autonomy.Off, 'Back': Autonomy.Off, 'Done': Autonomy.Off},
										remapping={'input_value': 'input_value', 'Distance': 'Distance'})

			# x:378 y:273
			OperatableStateMachine.add('go_back',
										self.use_behavior(go_backSM, 'go_back'),
										transitions={'finished': 'Obs_check', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
