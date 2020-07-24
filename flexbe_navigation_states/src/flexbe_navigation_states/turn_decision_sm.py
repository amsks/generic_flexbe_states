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
from flexbe_navigation_states.turn_left_sm import turn_leftSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sat Jul 18 2020
@author: TG4
'''
class turn_decisionSM(Behavior):
	'''
	turn_decisione
	'''


	def __init__(self):
		super(turn_decisionSM, self).__init__()
		self.name = 'turn_decision'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(turn_rightSM, 'turn_right')
		self.add_behavior(turn_leftSM, 'turn_left')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:733 y:240, x:933 y:240
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.turn_left1 = "turn_left"

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:57 y:67
			OperatableStateMachine.add('w1',
										WaitState(wait_time=1),
										transitions={'done': 's1'},
										autonomy={'done': Autonomy.Off})

			# x:469 y:271
			OperatableStateMachine.add('turn_right',
										self.use_behavior(turn_rightSM, 'turn_right'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:51 y:224
			OperatableStateMachine.add('s1',
										SubscriberState(topic='/chatter', blocking=True, clear=False),
										transitions={'received': 'd1', 'unavailable': 'w1'},
										autonomy={'received': Autonomy.Off, 'unavailable': Autonomy.Off},
										remapping={'message': 'message'})

			# x:255 y:224
			OperatableStateMachine.add('d1',
										DecisionState(outcomes=["left", "right", "none"], conditions=lambda x: "left" if x.data=="Turn_Left" else("right" if x.data=="Turn_Right" else "none")),
										transitions={'left': 'turn_left', 'right': 'turn_right', 'none': 'finished'},
										autonomy={'left': Autonomy.Off, 'right': Autonomy.Off, 'none': Autonomy.Off},
										remapping={'input_value': 'message'})

			# x:469 y:171
			OperatableStateMachine.add('turn_left',
										self.use_behavior(turn_leftSM, 'turn_left'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
