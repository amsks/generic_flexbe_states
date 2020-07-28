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
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Tue Jul 28 2020
@author: TG4
'''
class object_recognitionSM(Behavior):
	'''
	object recognition
	'''


	def __init__(self):
		super(object_recognitionSM, self).__init__()
		self.name = 'object_recognition'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:733 y:490, x:733 y:140
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:107 y:124
			OperatableStateMachine.add('w1',
										WaitState(wait_time=3),
										transitions={'done': 's1'},
										autonomy={'done': Autonomy.Off})

			# x:501 y:224
			OperatableStateMachine.add('s1',
										SubscriberState(topic='/darknet_ros/bounding_boxes', blocking=True, clear=True),
										transitions={'received': 'c1', 'unavailable': 'failed'},
										autonomy={'received': Autonomy.Off, 'unavailable': Autonomy.Off},
										remapping={'message': 'detection'})

			# x:343 y:474
			OperatableStateMachine.add('c1',
										Carbonara(),
										transitions={'done': 'w1'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'detection'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
