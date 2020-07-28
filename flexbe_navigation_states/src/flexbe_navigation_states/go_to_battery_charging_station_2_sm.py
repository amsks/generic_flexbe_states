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
from flexbe_navigation_states.move_base_state import MoveBaseState
from flexbe_states.subscriber_state import SubscriberState
from flexbe_states.decision_state import DecisionState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sat Jul 25 2020
@author: TG4
'''
class go_to_battery_charging_station_2SM(Behavior):
	'''
	go to battery charging station 2
	'''


	def __init__(self):
		super(go_to_battery_charging_station_2SM, self).__init__()
		self.name = 'go_to_battery_charging_station_2'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(battery_checkSM, 'battery_check')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:533 y:440, x:583 y:190
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.waypoint_charging = {'coordinate':{'x':'none', 'y':'none', 'theta':'none'}, 'increment':{'x':2.0, 'y':2.0, 'theta':3.1415/2}}
		_state_machine.userdata.curr_pose = 0

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:57 y:224
			OperatableStateMachine.add('w1',
										WaitState(wait_time=2),
										transitions={'done': 'battery_check'},
										autonomy={'done': Autonomy.Off})

			# x:219 y:321
			OperatableStateMachine.add('battery_check',
										self.use_behavior(battery_checkSM, 'battery_check'),
										transitions={'L_B': 'm1', 'M_B': 'w2', 'H_B': 'w2', 'failed': 'failed'},
										autonomy={'L_B': Autonomy.Inherit, 'M_B': Autonomy.Inherit, 'H_B': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:257 y:74
			OperatableStateMachine.add('w2',
										WaitState(wait_time=2),
										transitions={'done': 'w1'},
										autonomy={'done': Autonomy.Off})

			# x:581 y:24
			OperatableStateMachine.add('m1',
										MoveBaseState(),
										transitions={'arrived': 's1', 'failed': 'failed'},
										autonomy={'arrived': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'waypoint': 'waypoint_charging', 'curr_pose': 'curr_pose'})

			# x:751 y:174
			OperatableStateMachine.add('s1',
										SubscriberState(topic='/FourWD/battery', blocking=True, clear=False),
										transitions={'received': 'd1', 'unavailable': 'failed'},
										autonomy={'received': Autonomy.Off, 'unavailable': Autonomy.Off},
										remapping={'message': 'battery_level'})

			# x:755 y:424
			OperatableStateMachine.add('d1',
										DecisionState(outcomes=['full', 'not_full'], conditions=lambda x: 'full' if x.data>99.9 else 'not_full'),
										transitions={'full': 'finished', 'not_full': 'w3'},
										autonomy={'full': Autonomy.Off, 'not_full': Autonomy.Off},
										remapping={'input_value': 'battery_level'})

			# x:607 y:324
			OperatableStateMachine.add('w3',
										WaitState(wait_time=1),
										transitions={'done': 's1'},
										autonomy={'done': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
