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
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sat Jul 18 2020
@author: TG4
'''
class go_straightSM(Behavior):
	'''
	go_straight
	'''


	def __init__(self):
		super(go_straightSM, self).__init__()
		self.name = 'go_straight'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:133 y:340, x:333 y:340
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.incremental1 = [2, 0, 0]

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:107 y:124
			OperatableStateMachine.add('w1',
										WaitState(wait_time=1),
										transitions={'done': 's1'},
										autonomy={'done': Autonomy.Off})

			# x:81 y:224
			OperatableStateMachine.add('m1',
										MoveBaseState(),
										transitions={'arrived': 'finished', 'failed': 'failed'},
										autonomy={'arrived': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'waypoint': 'message', 'incremental': 'incremental1'})

			# x:301 y:174
			OperatableStateMachine.add('s1',
										SubscriberState(topic='/pose', blocking=True, clear=False),
										transitions={'received': 'm1', 'unavailable': 'failed'},
										autonomy={'received': Autonomy.Off, 'unavailable': Autonomy.Off},
										remapping={'message': 'message'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
