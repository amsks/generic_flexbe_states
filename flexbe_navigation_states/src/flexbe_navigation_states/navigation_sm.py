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
from flexbe_navigation_states.obstacle_avoidance_sm import Obstacle_AvoidanceSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sat Jul 18 2020
@author: TG4
'''
class NavigationSM(Behavior):
	'''
	Integrated behaviour
	'''


	def __init__(self):
		super(NavigationSM, self).__init__()
		self.name = 'Navigation'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(turn_rightSM, 'turn_right')
		self.add_behavior(turn_leftSM, 'turn_left')
		self.add_behavior(go_straightSM, 'go_straight')
		self.add_behavior(go_straightSM, 'go_straight_2')
		self.add_behavior(go_straightSM, 'go_straight_3')
		self.add_behavior(Obstacle_AvoidanceSM, 'Obstacle_Avoidance')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:1683 y:419, x:605 y:337
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

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

			# x:286 y:212
			OperatableStateMachine.add('carb1',
										Carbonara(),
										transitions={'none': 'go_straight', 'Obstacle': 'Obstacle_Avoidance', 'Left': 'go_straight_2', 'Right': 'go_straight_3'},
										autonomy={'none': Autonomy.Off, 'Obstacle': Autonomy.Off, 'Left': Autonomy.Off, 'Right': Autonomy.Off},
										remapping={'input_value': 'detected', 'Distance': 'Distance'})

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

			# x:381 y:495
			OperatableStateMachine.add('Obstacle_Avoidance',
										self.use_behavior(Obstacle_AvoidanceSM, 'Obstacle_Avoidance'),
										transitions={'finished': 's1', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
