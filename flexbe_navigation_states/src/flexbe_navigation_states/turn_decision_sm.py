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
from flexbe_states.decision_state import DecisionState
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
		# x:1033 y:540, x:933 y:540
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.waypoint_left = {'coordinate':{'x':'none', 'y':'none', 'theta':'none'}, 'increment':{'x':2.0, 'y':2.0, 'theta':3.1415/2}}
		_state_machine.userdata.waypoint_right = {'coordinate':{'x':'none', 'y':'none', 'theta':'none'}, 'increment':{'x':2.0, 'y':-2.0, 'theta':-3.1415/2}}
		_state_machine.userdata.waypoint_straight = {'coordinate':{'x':'none', 'y':'none', 'theta':'none'}, 'increment':{'x':1.0, 'y':0.0, 'theta':0.0}}

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:57 y:74
			OperatableStateMachine.add('w1',
										WaitState(wait_time=1),
										transitions={'done': 's1'},
										autonomy={'done': Autonomy.Off})

			# x:819 y:321
			OperatableStateMachine.add('turn_right',
										self.use_behavior(turn_rightSM, 'turn_right'),
										transitions={'finished': 'w2', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:51 y:224
			OperatableStateMachine.add('s1',
										SubscriberState(topic='/darknet_ros/bounding_boxes', blocking=True, clear=False),
										transitions={'received': 'carb1', 'unavailable': 'w1'},
										autonomy={'received': Autonomy.Off, 'unavailable': Autonomy.Off},
										remapping={'message': 'detected'})

			# x:214 y:221
			OperatableStateMachine.add('d1',
										DecisionState(outcomes=["left", "right", "none"], conditions=lambda input_value: "left" if input_value=="Left_Sign" else("right" if input_value=="Right_Sign" else "none")),
										transitions={'left': 'w3', 'right': 'w4', 'none': 'go_straight'},
										autonomy={'left': Autonomy.Off, 'right': Autonomy.Off, 'none': Autonomy.Off},
										remapping={'input_value': 'closest_object'})

			# x:43 y:374
			OperatableStateMachine.add('carb1',
										Carbonara(),
										transitions={'done': 'd1'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'detected', 'closest_object': 'closest_object'})

			# x:1107 y:224
			OperatableStateMachine.add('w2',
										WaitState(wait_time=1),
										transitions={'done': 'w5'},
										autonomy={'done': Autonomy.Off})

			# x:357 y:124
			OperatableStateMachine.add('w3',
										WaitState(wait_time=5),
										transitions={'done': 'go_straight_2'},
										autonomy={'done': Autonomy.Off})

			# x:357 y:324
			OperatableStateMachine.add('w4',
										WaitState(wait_time=5),
										transitions={'done': 'go_straight_3'},
										autonomy={'done': Autonomy.Off})

			# x:1107 y:74
			OperatableStateMachine.add('w5',
										WaitState(wait_time=1),
										transitions={'done': 'w1'},
										autonomy={'done': Autonomy.Off})

			# x:819 y:121
			OperatableStateMachine.add('turn_left',
										self.use_behavior(turn_leftSM, 'turn_left'),
										transitions={'finished': 'w2', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:819 y:221
			OperatableStateMachine.add('go_straight',
										self.use_behavior(go_straightSM, 'go_straight'),
										transitions={'finished': 'w2', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:519 y:121
			OperatableStateMachine.add('go_straight_2',
										self.use_behavior(go_straightSM, 'go_straight_2'),
										transitions={'finished': 'turn_left', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:519 y:321
			OperatableStateMachine.add('go_straight_3',
										self.use_behavior(go_straightSM, 'go_straight_3'),
										transitions={'finished': 'turn_right', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
