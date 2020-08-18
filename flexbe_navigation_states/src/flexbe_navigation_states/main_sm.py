#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flexbe_states.subscriber_state import SubscriberState
from flexbe_utility_states.ADI import Amatricianna
from flexbe_navigation_states.navigation_sm import NavigationSM
from flexbe_navigation_states.parking_sm import ParkingSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Mon Aug 17 2020
@author: Aditya
'''
class MAINSM(Behavior):
	'''
	New integration test
	'''


	def __init__(self):
		super(MAINSM, self).__init__()
		self.name = 'MAIN'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(NavigationSM, 'Navigation')
		self.add_behavior(ParkingSM, 'Parking')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:1085 y:232, x:429 y:580
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.input_value = 1

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:117 y:87
			OperatableStateMachine.add('Get_pose',
										SubscriberState(topic='/pose', blocking=True, clear=False),
										transitions={'received': 'Calculate_Need', 'unavailable': 'failed'},
										autonomy={'received': Autonomy.Off, 'unavailable': Autonomy.Off},
										remapping={'message': 'curr_pose'})

			# x:373 y:214
			OperatableStateMachine.add('Calculate_Need',
										Amatricianna(),
										transitions={'Navigation': 'Navigation', 'Parking': 'Parking'},
										autonomy={'Navigation': Autonomy.Off, 'Parking': Autonomy.Off},
										remapping={'curr_pose': 'curr_pose', 'Direction': 'Direction'})

			# x:659 y:61
			OperatableStateMachine.add('Navigation',
										self.use_behavior(NavigationSM, 'Navigation'),
										transitions={'finished': 'Calculate_Need', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:652 y:250
			OperatableStateMachine.add('Parking',
										self.use_behavior(ParkingSM, 'Parking'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
