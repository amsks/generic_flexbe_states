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
from flexbe_navigation_states.battery_check_sm import battery_checkSM
from flexbe_navigation_states.go_straight_sm import go_straightSM
from flexbe_navigation_states.go_back_sm import go_backSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Wed Jul 29 2020
@author: TG4
'''
class ENTER_BATTERYSM(Behavior):
	'''
	enter battery
	'''


	def __init__(self):
		super(ENTER_BATTERYSM, self).__init__()
		self.name = 'ENTER_BATTERY'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(battery_checkSM, 'battery_check')
		self.add_behavior(go_straightSM, 'go_straight')
		self.add_behavior(battery_checkSM, 'battery_check_2')
		self.add_behavior(go_backSM, 'go_back')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:30 y:365, x:83 y:290
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:157 y:24
			OperatableStateMachine.add('w1',
										WaitState(wait_time=1),
										transitions={'done': 'battery_check'},
										autonomy={'done': Autonomy.Off})

			# x:169 y:121
			OperatableStateMachine.add('battery_check',
										self.use_behavior(battery_checkSM, 'battery_check'),
										transitions={'L_B': 'go_straight', 'M_B': 'w2', 'H_B': 'w2', 'failed': 'failed'},
										autonomy={'L_B': Autonomy.Inherit, 'M_B': Autonomy.Inherit, 'H_B': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:407 y:24
			OperatableStateMachine.add('w2',
										WaitState(wait_time=2),
										transitions={'done': 'w1'},
										autonomy={'done': Autonomy.Off})

			# x:519 y:171
			OperatableStateMachine.add('go_straight',
										self.use_behavior(go_straightSM, 'go_straight'),
										transitions={'finished': 'battery_check_2', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:519 y:271
			OperatableStateMachine.add('battery_check_2',
										self.use_behavior(battery_checkSM, 'battery_check_2'),
										transitions={'L_B': 'w3', 'M_B': 'go_back', 'H_B': 'go_back', 'failed': 'failed'},
										autonomy={'L_B': Autonomy.Inherit, 'M_B': Autonomy.Inherit, 'H_B': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:557 y:424
			OperatableStateMachine.add('w3',
										WaitState(wait_time=2),
										transitions={'done': 'battery_check_2'},
										autonomy={'done': Autonomy.Off})

			# x:269 y:371
			OperatableStateMachine.add('go_back',
										self.use_behavior(go_backSM, 'go_back'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
