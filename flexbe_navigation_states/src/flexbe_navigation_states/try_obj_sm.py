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
from flexbe_utility_states.MARCO import Carbonara
from flexbe_utility_states.object_recognition import ObjectRecognition
from flexbe_states.subscriber_state import SubscriberState
from flexbe_navigation_states.turn_left_sm import turn_leftSM
from flexbe_navigation_states.turn_right_sm import turn_rightSM
from flexbe_navigation_states.go_straight_sm import go_straightSM
from flexbe_states.publisher_string_state import PublisherStringState
from flexbe_navigation_states.stop_sm import StopSM
from flexbe_states.decision_state import DecisionState
from flexbe_navigation_states.go_back_sm import go_backSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Wed Jul 29 2020
@author: TG4
'''
class Try_ObjSM(Behavior):
	'''
	try_obj
	'''


	def __init__(self):
		super(Try_ObjSM, self).__init__()
		self.name = 'Try_Obj'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(turn_leftSM, 'turn_left')
		self.add_behavior(turn_rightSM, 'turn_right')
		self.add_behavior(go_straightSM, 'go_straight')
		self.add_behavior(StopSM, 'Stop')
		self.add_behavior(go_backSM, 'go_back')
		self.add_behavior(go_straightSM, 'go_straight_2')
		self.add_behavior(StopSM, 'Stop_2')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:1683 y:440, x:1433 y:40, x:1433 y:790
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed', 'failed2'])
		_state_machine.userdata.pub_roadworks = 'Roadworks'
		_state_machine.userdata.pub_slippery_road = 'Slippery_Road'

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:57 y:24
			OperatableStateMachine.add('w1',
										WaitState(wait_time=1),
										transitions={'done': 's1'},
										autonomy={'done': Autonomy.Off})

			# x:143 y:224
			OperatableStateMachine.add('carb1',
										Carbonara(),
										transitions={'continue': 'or1', 'Obstacle': 'w4'},
										autonomy={'continue': Autonomy.Off, 'Obstacle': Autonomy.Off},
										remapping={'input_value': 'detected', 'output_value': 'closest_object'})

			# x:143 y:424
			OperatableStateMachine.add('or1',
										ObjectRecognition(),
										transitions={'Left_Sign': 'turn_left', 'Right_Sign': 'turn_right', 'Roadworks': 'p1', 'Slippery_Road': 'p2', 'Turn_Left_Sign': 'turn_left', 'Turn_Right_Sign': 'turn_right', 'Charging_Station': 'finished', 'Stop_Sign': 'Stop', 'Parking_Sign': 'finished', 'Parking_Spot': 'finished', 'none': 'go_straight'},
										autonomy={'Left_Sign': Autonomy.Off, 'Right_Sign': Autonomy.Off, 'Roadworks': Autonomy.Off, 'Slippery_Road': Autonomy.Off, 'Turn_Left_Sign': Autonomy.Off, 'Turn_Right_Sign': Autonomy.Off, 'Charging_Station': Autonomy.Off, 'Stop_Sign': Autonomy.Off, 'Parking_Sign': Autonomy.Off, 'Parking_Spot': Autonomy.Off, 'none': Autonomy.Off},
										remapping={'input_value': 'closest_object'})

			# x:251 y:24
			OperatableStateMachine.add('s1',
										SubscriberState(topic='/darknet_ros/bounding_boxes', blocking=True, clear=False),
										transitions={'received': 'carb1', 'unavailable': 'failed'},
										autonomy={'received': Autonomy.Off, 'unavailable': Autonomy.Off},
										remapping={'message': 'detected'})

			# x:619 y:721
			OperatableStateMachine.add('turn_left',
										self.use_behavior(turn_leftSM, 'turn_left'),
										transitions={'finished': 'finished', 'failed': 'failed2'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:619 y:621
			OperatableStateMachine.add('turn_right',
										self.use_behavior(turn_rightSM, 'turn_right'),
										transitions={'finished': 'finished', 'failed': 'failed2'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:619 y:821
			OperatableStateMachine.add('go_straight',
										self.use_behavior(go_straightSM, 'go_straight'),
										transitions={'finished': 'finished', 'failed': 'failed2'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:591 y:374
			OperatableStateMachine.add('p1',
										PublisherStringState(topic='/chatter'),
										transitions={'done': 'w2'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'pub_roadworks'})

			# x:591 y:474
			OperatableStateMachine.add('p2',
										PublisherStringState(topic='/chatter'),
										transitions={'done': 'w3'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'pub_slippery_road'})

			# x:857 y:324
			OperatableStateMachine.add('w2',
										WaitState(wait_time=3),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})

			# x:857 y:524
			OperatableStateMachine.add('w3',
										WaitState(wait_time=3),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})

			# x:769 y:221
			OperatableStateMachine.add('Stop',
										self.use_behavior(StopSM, 'Stop'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:457 y:74
			OperatableStateMachine.add('w4',
										WaitState(wait_time=1),
										transitions={'done': 'd1'},
										autonomy={'done': Autonomy.Off})

			# x:805 y:124
			OperatableStateMachine.add('d1',
										DecisionState(outcomes=['go', 'stop', 'back'], conditions=lambda input_value: 'go' if input_value[1]>3 else ('back' if input_value[1]<1.5 else 'stop')),
										transitions={'go': 'go_straight_2', 'stop': 'Stop_2', 'back': 'go_back'},
										autonomy={'go': Autonomy.Off, 'stop': Autonomy.Off, 'back': Autonomy.Off},
										remapping={'input_value': 'closest_object'})

			# x:1519 y:171
			OperatableStateMachine.add('go_back',
										self.use_behavior(go_backSM, 'go_back'),
										transitions={'finished': 'carb1', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:1169 y:221
			OperatableStateMachine.add('go_straight_2',
										self.use_behavior(go_straightSM, 'go_straight_2'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:469 y:156
			OperatableStateMachine.add('Stop_2',
										self.use_behavior(StopSM, 'Stop_2'),
										transitions={'finished': 'carb1', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
