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

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:83 y:490, x:83 y:290
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.waypoint_charging = {'coordinate':{'x':0.0, 'y':0.0, 'theta':0.0}, 'increment':{'x':'none', 'y':'none', 'theta':'none'}}
		_state_machine.userdata.curr_pose = 'none'

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:157 y:74
			OperatableStateMachine.add('w1',
										WaitState(wait_time=1),
										transitions={'done': 'm1'},
										autonomy={'done': Autonomy.Off})

			# x:481 y:74
			OperatableStateMachine.add('m1',
										MoveBaseState(),
										transitions={'arrived': 's1', 'failed': 'failed'},
										autonomy={'arrived': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'waypoint': 'waypoint_charging', 'curr_pose': 'curr_pose'})

			# x:501 y:174
			OperatableStateMachine.add('s1',
										SubscriberState(topic='/FourWD/battery', blocking=True, clear=False),
										transitions={'received': 'd1', 'unavailable': 'failed'},
										autonomy={'received': Autonomy.Off, 'unavailable': Autonomy.Off},
										remapping={'message': 'battery_level'})

			# x:505 y:424
			OperatableStateMachine.add('d1',
										DecisionState(outcomes=['full', 'not_full'], conditions=lambda x: 'full' if x.data>99.9 else 'not_full'),
										transitions={'full': 'finished', 'not_full': 'w2'},
										autonomy={'full': Autonomy.Off, 'not_full': Autonomy.Off},
										remapping={'input_value': 'battery_level'})

			# x:357 y:324
			OperatableStateMachine.add('w2',
										WaitState(wait_time=1),
										transitions={'done': 's1'},
										autonomy={'done': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
