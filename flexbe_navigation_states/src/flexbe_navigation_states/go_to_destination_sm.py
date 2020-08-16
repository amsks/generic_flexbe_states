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
from flexbe_navigation_states.move_base_state import MoveBaseState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sun Jul 26 2020
@author: TG4
'''
class go_to_destinationSM(Behavior):
	'''
	go to destination
	'''


	def __init__(self):
		super(go_to_destinationSM, self).__init__()
		self.name = 'go_to_destination'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:383 y:390, x:182 y:190
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['reason'])
		_state_machine.userdata.waypoint1 = {'coordinate':{'x':-7.0, 'y':-7.476, 'theta':0.0}, 'increment':{'x':'none', 'y':'none', 'theta':'none'}}
		_state_machine.userdata.reason = 0

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:107 y:74
			OperatableStateMachine.add('w1',
										WaitState(wait_time=3),
										transitions={'done': 's1'},
										autonomy={'done': Autonomy.Off})

			# x:351 y:74
			OperatableStateMachine.add('s1',
										SubscriberState(topic='/pose', blocking=True, clear=False),
										transitions={'received': 's2', 'unavailable': 'failed'},
										autonomy={'received': Autonomy.Off, 'unavailable': Autonomy.Off},
										remapping={'message': 'curr_pose'})

			# x:351 y:224
			OperatableStateMachine.add('s2',
										SubscriberState(topic='/set_waypoint', blocking=True, clear=False),
										transitions={'received': 'm1', 'unavailable': 'failed'},
										autonomy={'received': Autonomy.Off, 'unavailable': Autonomy.Off},
										remapping={'message': 'waypoint2'})

			# x:81 y:309
			OperatableStateMachine.add('m1',
										MoveBaseState(),
										transitions={'arrived': 'finished', 'failed': 'failed'},
										autonomy={'arrived': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'waypoint': 'waypoint1', 'curr_pose': 'curr_pose'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
