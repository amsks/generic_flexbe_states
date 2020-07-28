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
from flexbe_navigation_states.go_to_battery_charging_station_sm import go_to_battery_charging_stationSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sat Jul 25 2020
@author: TG4
'''
class go_to_battery_charging_stationSM(Behavior):
	'''
	go to battery charging station
	'''


	def __init__(self):
		super(go_to_battery_charging_stationSM, self).__init__()
		self.name = 'go_to_battery_charging_station'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(go_to_battery_charging_stationSM, 'go_to_battery_charging_station')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:30 y:365, x:458 y:366
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.waypoint1 = [0.7081,-2.5405, 0.0]
		_state_machine.userdata.incremental1 = [0.0, 0.0, 0.0]

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:164 y:156
			OperatableStateMachine.add('w1',
										WaitState(wait_time=3),
										transitions={'done': 'go_to_battery_charging_station'},
										autonomy={'done': Autonomy.Off})

			# x:398 y:156
			OperatableStateMachine.add('go_to_battery_charging_station',
										self.use_behavior(go_to_battery_charging_stationSM, 'go_to_battery_charging_station'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
