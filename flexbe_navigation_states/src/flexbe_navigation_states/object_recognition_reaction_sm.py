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
from flexbe_states.subscriber_state import SubscriberState
from flexbe_utility_states.MARCO import Carbonara
from flexbe_navigation_states.go_straight_sm import go_straightSM
from flexbe_navigation_states.stop_sm import StopSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Wed Jul 29 2020
@author: TG4
'''
class object_recognition_reactionSM(Behavior):
	'''
	object recognition reaction
	'''


	def __init__(self):
		super(object_recognition_reactionSM, self).__init__()
		self.name = 'object_recognition_reaction'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(go_straightSM, 'go_straight')
		self.add_behavior(StopSM, 'Stop')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:467 y:617, x:633 y:340
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:357 y:174
			OperatableStateMachine.add('w1',
										WaitState(wait_time=1),
										transitions={'done': 's1'},
										autonomy={'done': Autonomy.Off})

			# x:51 y:324
			OperatableStateMachine.add('s1',
										SubscriberState(topic='/darknet_ros/bounding_boxes', blocking=True, clear=False),
										transitions={'received': 'carb1', 'unavailable': 'failed'},
										autonomy={'received': Autonomy.Off, 'unavailable': Autonomy.Off},
										remapping={'message': 'detected'})

			# x:43 y:474
			OperatableStateMachine.add('carb1',
										Carbonara(),
										transitions={'continue': 'go_straight', 'Obstacle': 'Stop'},
										autonomy={'continue': Autonomy.Off, 'Obstacle': Autonomy.Off},
										remapping={'input_value': 'detected', 'output_value': 'output_value'})

			# x:569 y:171
			OperatableStateMachine.add('go_straight',
										self.use_behavior(go_straightSM, 'go_straight'),
										transitions={'finished': 'w1', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:569 y:471
			OperatableStateMachine.add('Stop',
										self.use_behavior(StopSM, 'Stop'),
										transitions={'finished': 'w1', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
