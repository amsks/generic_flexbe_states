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
from flexbe_navigation_states.go_straight_sm import go_straightSM
from flexbe_navigation_states.turn_decision_sm import turn_decisionSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sat Jul 18 2020
@author: TG4
'''
class aSM(Behavior):
	'''
	a
	'''


	def __init__(self):
		super(aSM, self).__init__()
		self.name = 'a'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(go_straightSM, 'go_straight')
		self.add_behavior(turn_decisionSM, 'turn_decision')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:658 y:463, x:511 y:525
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:107 y:167
			OperatableStateMachine.add('w1',
										WaitState(wait_time=1),
										transitions={'done': 'turn_decision'},
										autonomy={'done': Autonomy.Off})

			# x:603 y:148
			OperatableStateMachine.add('go_straight',
										self.use_behavior(go_straightSM, 'go_straight'),
										transitions={'finished': 'w1', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:311 y:265
			OperatableStateMachine.add('turn_decision',
										self.use_behavior(turn_decisionSM, 'turn_decision'),
										transitions={'finished': 'go_straight', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
