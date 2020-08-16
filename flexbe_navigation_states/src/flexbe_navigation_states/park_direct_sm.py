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
Created on Sat Jul 18 2020
@author: TG4
'''
class park_directSM(Behavior):
	'''
	park_direct
	'''


	def __init__(self):
		super(park_directSM, self).__init__()
		self.name = 'park_direct'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:683 y:490, x:740 y:211
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.incremental1 = {'coordinate':{'x':'none', 'y':'none', 'theta':'none'}, 'increment':{'x':1.0, 'y':0.0, 'theta':0.0}}
		_state_machine.userdata.incremental2 = {'coordinate':{'x':'none', 'y':'none', 'theta':'none'}, 'increment':{'x':0.2929, 'y':0.2929, 'theta':-3.1415/4}}
		_state_machine.userdata.incremental3 = {'coordinate':{'x':'none', 'y':'none', 'theta':'none'}, 'increment':{'x':0.0, 'y':1.0, 'theta':-3.1415/2}}
		_state_machine.userdata.incremental4 = {'coordinate':{'x':'none', 'y':'none', 'theta':'none'}, 'increment':{'x':0.0, 'y':-1.0, 'theta':-3.1415/2}}

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:107 y:74
			OperatableStateMachine.add('w1',
										WaitState(wait_time=1),
										transitions={'done': 's1'},
										autonomy={'done': Autonomy.Off})

			# x:301 y:74
			OperatableStateMachine.add('s1',
										SubscriberState(topic='/pose', blocking=True, clear=False),
										transitions={'received': 'w2', 'unavailable': 'failed'},
										autonomy={'received': Autonomy.Off, 'unavailable': Autonomy.Off},
										remapping={'message': 'curr_pose'})

			# x:281 y:174
			OperatableStateMachine.add('m1',
										MoveBaseState(),
										transitions={'arrived': 'w3', 'failed': 'failed'},
										autonomy={'arrived': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'waypoint': 'incremental1', 'curr_pose': 'curr_pose'})

			# x:281 y:274
			OperatableStateMachine.add('m2',
										MoveBaseState(),
										transitions={'arrived': 'w4', 'failed': 'failed'},
										autonomy={'arrived': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'waypoint': 'incremental2', 'curr_pose': 'curr_pose'})

			# x:281 y:374
			OperatableStateMachine.add('m3',
										MoveBaseState(),
										transitions={'arrived': 'w5', 'failed': 'failed'},
										autonomy={'arrived': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'waypoint': 'incremental3', 'curr_pose': 'curr_pose'})

			# x:107 y:174
			OperatableStateMachine.add('w2',
										WaitState(wait_time=1),
										transitions={'done': 'm1'},
										autonomy={'done': Autonomy.Off})

			# x:107 y:274
			OperatableStateMachine.add('w3',
										WaitState(wait_time=5),
										transitions={'done': 'm2'},
										autonomy={'done': Autonomy.Off})

			# x:107 y:374
			OperatableStateMachine.add('w4',
										WaitState(wait_time=5),
										transitions={'done': 'm3'},
										autonomy={'done': Autonomy.Off})

			# x:107 y:474
			OperatableStateMachine.add('w5',
										WaitState(wait_time=5),
										transitions={'done': 'm4'},
										autonomy={'done': Autonomy.Off})

			# x:281 y:474
			OperatableStateMachine.add('m4',
										MoveBaseState(),
										transitions={'arrived': 'finished', 'failed': 'failed'},
										autonomy={'arrived': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'waypoint': 'incremental4', 'curr_pose': 'curr_pose'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
