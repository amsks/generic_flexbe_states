#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flexbe_states.wait_state import WaitState
from flexbe_navigation_states.go_to_destination_sm import go_to_destinationSM
from flexbe_states.subscriber_state import SubscriberState
from flexbe_navigation_states.battery_check_sm import battery_checkSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sun Jul 26 2020
@author: TG4
'''
class mainSM(Behavior):
	'''
	main
	'''


	def __init__(self):
		super(mainSM, self).__init__()
		self.name = 'main'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(go_to_destinationSM, 'go_to_destination')
		self.add_behavior(battery_checkSM, 'battery_check')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:133 y:540, x:133 y:440
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.input_value1 = 5
		_state_machine.userdata.reason1 = 5

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:107 y:74
			OperatableStateMachine.add('w1',
										WaitState(wait_time=3),
										transitions={'done': 's1'},
										autonomy={'done': Autonomy.Off})

			# x:519 y:521
			OperatableStateMachine.add('go_to_destination',
										self.use_behavior(go_to_destinationSM, 'go_to_destination'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'reason': 'main_goal'})

			# x:351 y:74
			OperatableStateMachine.add('s1',
										SubscriberState(topic='/set_waypoint', blocking=True, clear=False),
										transitions={'received': 'battery_check', 'unavailable': 'failed'},
										autonomy={'received': Autonomy.Off, 'unavailable': Autonomy.Off},
										remapping={'message': 'main_goal'})

			# x:669 y:49
			OperatableStateMachine.add('battery_check',
										self.use_behavior(battery_checkSM, 'battery_check'),
										transitions={'L_B': 'go_to_destination', 'M_B': 'go_to_destination', 'H_B': 'go_to_destination', 'failed': 'failed'},
										autonomy={'L_B': Autonomy.Inherit, 'M_B': Autonomy.Inherit, 'H_B': Autonomy.Inherit, 'failed': Autonomy.Inherit})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
