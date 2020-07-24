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
from flexbe_states.decision_state import DecisionState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sat Jul 18 2020
@author: TG4
'''
class batterySM(Behavior):
	'''
	battery
	'''


	def __init__(self):
		super(batterySM, self).__init__()
		self.name = 'battery'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:133 y:340, x:583 y:40
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.waypoint1 = "ZER0"
		_state_machine.userdata.incremental1 = [0, 0, 0]

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:107 y:24
			OperatableStateMachine.add('w1',
										WaitState(wait_time=1),
										transitions={'done': 's1'},
										autonomy={'done': Autonomy.Off})

			# x:301 y:24
			OperatableStateMachine.add('s1',
										SubscriberState(topic='/FourWD/battery', blocking=True, clear=False),
										transitions={'received': 'w2', 'unavailable': 'failed'},
										autonomy={'received': Autonomy.Off, 'unavailable': Autonomy.Off},
										remapping={'message': 'message1'})

			# x:307 y:174
			OperatableStateMachine.add('w2',
										WaitState(wait_time=1),
										transitions={'done': 'd1'},
										autonomy={'done': Autonomy.Off})

			# x:105 y:174
			OperatableStateMachine.add('d1',
										DecisionState(outcomes=['Low','Medium','High'], conditions=lambda x: 'Low' if x.data<49 else 'Medium'),
										transitions={'Low': 'finished', 'Medium': 'w1', 'High': 'w1'},
										autonomy={'Low': Autonomy.Off, 'Medium': Autonomy.Off, 'High': Autonomy.Off},
										remapping={'input_value': 'message1'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
