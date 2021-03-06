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
Created on Tue Jul 28 2020
@author: TG4
'''
class TRYWHYSM(Behavior):
	'''
	TRYWHY
	'''


	def __init__(self):
		super(TRYWHYSM, self).__init__()
		self.name = 'TRYWHY'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:30 y:365, x:239 y:368
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.waypoint_left = {'coordinate':{'x':'none', 'y':'none', 'theta':'none'}, 'increment':{'x':2.0, 'y':2.0, 'theta':3.1415/2}}

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:30 y:40
			OperatableStateMachine.add('w1',
										WaitState(wait_time=3),
										transitions={'done': 's1'},
										autonomy={'done': Autonomy.Off})

			# x:201 y:167
			OperatableStateMachine.add('m1',
										MoveBaseState(),
										transitions={'arrived': 'finished', 'failed': 'failed'},
										autonomy={'arrived': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'waypoint': 'waypoint_left', 'curr_pose': 'curr_pose'})

			# x:551 y:124
			OperatableStateMachine.add('s1',
										SubscriberState(topic='/pose', blocking=True, clear=False),
										transitions={'received': 'm1', 'unavailable': 'failed'},
										autonomy={'received': Autonomy.Off, 'unavailable': Autonomy.Off},
										remapping={'message': 'curr_pose'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
