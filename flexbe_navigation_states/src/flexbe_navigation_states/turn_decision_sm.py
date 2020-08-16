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
from flexbe_navigation_states.turn_right_sm import turn_rightSM
from flexbe_states.subscriber_state import SubscriberState
from flexbe_utility_states.MARCO import Carbonara
from flexbe_navigation_states.turn_left_sm import turn_leftSM
from flexbe_navigation_states.go_straight_sm import go_straightSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sat Jul 18 2020
@author: TG4
'''
class turn_decisionSM(Behavior):
	'''
	turn_decision
	'''


	def __init__(self):
		super(turn_decisionSM, self).__init__()
		self.name = 'turn_decision'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(turn_rightSM, 'turn_right')
		self.add_behavior(turn_leftSM, 'turn_left')
		self.add_behavior(go_straightSM, 'go_straight')
		self.add_behavior(go_straightSM, 'go_straight_2')
		self.add_behavior(go_straightSM, 'go_straight_3')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:144 y:532, x:605 y:337
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.waypoint_left = {'coordinate':{'x':'none', 'y':'none', 'theta':'none'}, 'increment':{'x':2.0, 'y':2.0, 'theta':3.1415/2}}
		_state_machine.userdata.waypoint_right = {'coordinate':{'x':'none', 'y':'none', 'theta':'none'}, 'increment':{'x':2.0, 'y':-2.0, 'theta':-3.1415/2}}
		_state_machine.userdata.waypoint_straight = {'coordinate':{'x':'none', 'y':'none', 'theta':'none'}, 'increment':{'x':2.0, 'y':0.0, 'theta':0.0}}

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:58 y:69
			OperatableStateMachine.add('w1',
										WaitState(wait_time=1),
										transitions={'done': 's1'},
										autonomy={'done': Autonomy.Off})

			# x:1090 y:488
			OperatableStateMachine.add('turn_right',
										self.use_behavior(turn_rightSM, 'turn_right'),
										transitions={'finished': 'w2', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:55 y:196
			OperatableStateMachine.add('s1',
										SubscriberState(topic='/darknet_ros/bounding_boxes', blocking=True, clear=False),
										transitions={'received': 'carb1', 'unavailable': 'w1'},
										autonomy={'received': Autonomy.Off, 'unavailable': Autonomy.Off},
										remapping={'message': 'detected'})

			# x:173 y:276
			OperatableStateMachine.add('carb1',
										Carbonara(),
										transitions={'none': 'go_straight', 'Obstacle': 'finished', 'Left': 'go_straight_2', 'Right': 'go_straight_3'},
										autonomy={'none': Autonomy.Off, 'Obstacle': Autonomy.Off, 'Left': Autonomy.Off, 'Right': Autonomy.Off},
										remapping={'input_value': 'detected', 'output_value': 'closest_object'})

			# x:1180 y:246
			OperatableStateMachine.add('w2',
										WaitState(wait_time=1),
										transitions={'done': 'w5'},
										autonomy={'done': Autonomy.Off})

			# x:1161 y:64
			OperatableStateMachine.add('w5',
										WaitState(wait_time=1),
										transitions={'done': 'w1'},
										autonomy={'done': Autonomy.Off})

			# x:958 y:119
			OperatableStateMachine.add('turn_left',
										self.use_behavior(turn_leftSM, 'turn_left'),
										transitions={'finished': 'w2', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:906 y:276
			OperatableStateMachine.add('go_straight',
										self.use_behavior(go_straightSM, 'go_straight'),
										transitions={'finished': 'w2', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:679 y:118
			OperatableStateMachine.add('go_straight_2',
										self.use_behavior(go_straightSM, 'go_straight_2'),
										transitions={'finished': 'turn_left', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:715 y:484
			OperatableStateMachine.add('go_straight_3',
										self.use_behavior(go_straightSM, 'go_straight_3'),
										transitions={'finished': 'turn_right', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
