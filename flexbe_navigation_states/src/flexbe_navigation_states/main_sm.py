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
from flexbe_navigation_states.try_obj_sm import Try_ObjSM
from flexbe_navigation_states.battery_check_sm import battery_checkSM
from flexbe_navigation_states.go_to_battery_charging_station_2_sm import go_to_battery_charging_station_2SM
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
		self.add_behavior(Try_ObjSM, 'Try_Obj')
		self.add_behavior(battery_checkSM, 'battery_check')
		self.add_behavior(go_to_battery_charging_station_2SM, 'go_to_battery_charging_station_2')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:183 y:590, x:933 y:290
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.input_value1 = 5
		_state_machine.userdata.reason1 = 5

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:257 y:167
			OperatableStateMachine.add('w1',
										WaitState(wait_time=1),
										transitions={'done': 'Try_Obj'},
										autonomy={'done': Autonomy.Off})

			# x:519 y:149
			OperatableStateMachine.add('Try_Obj',
										self.use_behavior(Try_ObjSM, 'Try_Obj'),
										transitions={'finished': 'battery_check', 'failed': 'failed', 'failed2': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'failed2': Autonomy.Inherit})

			# x:257 y:374
			OperatableStateMachine.add('w2',
										WaitState(wait_time=1),
										transitions={'done': 'w1'},
										autonomy={'done': Autonomy.Off})

			# x:519 y:291
			OperatableStateMachine.add('battery_check',
										self.use_behavior(battery_checkSM, 'battery_check'),
										transitions={'L_B': 'go_to_battery_charging_station_2', 'M_B': 'w2', 'H_B': 'w2', 'failed': 'failed'},
										autonomy={'L_B': Autonomy.Inherit, 'M_B': Autonomy.Inherit, 'H_B': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:492 y:456
			OperatableStateMachine.add('go_to_battery_charging_station_2',
										self.use_behavior(go_to_battery_charging_station_2SM, 'go_to_battery_charging_station_2'),
										transitions={'finished': 'w2', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
