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
class battery_checkSM(Behavior):
    '''
    battery check
    '''
 
 
    def __init__(self):
        super(battery_checkSM, self).__init__()
        self.name = 'battery_check'
 
        # parameters of this behavior
 
        # references to used behaviors
 
        # Additional initialization code can be added inside the following tags
        # [MANUAL_INIT]
        
        # [/MANUAL_INIT]
 
        # Behavior comments:
 
 
 
    def create(self):
        # x:33 y:340, x:133 y:340, x:233 y:340, x:144 y:140
        _state_machine = OperatableStateMachine(outcomes=['L_B', 'M_B', 'H_B', 'failed'])
 
        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]
 
 
        with _state_machine:
            # x:107 y:24
            OperatableStateMachine.add('w1',
                                        WaitState(wait_time=4),
                                        transitions={'done': 's1'},
                                        autonomy={'done': Autonomy.Off})
 
            # x:351 y:24
            OperatableStateMachine.add('s1',
                                        SubscriberState(topic='/FourWD/battery', blocking=True, clear=False),
                                        transitions={'received': 'w2', 'unavailable': 'failed'},
                                        autonomy={'received': Autonomy.Off, 'unavailable': Autonomy.Off},
                                        remapping={'message': 'battery_level'})
 
            # x:357 y:224
            OperatableStateMachine.add('w2',
                                        WaitState(wait_time=1),
                                        transitions={'done': 'd1'},
                                        autonomy={'done': Autonomy.Off})
 
            # x:105 y:224
            OperatableStateMachine.add('d1',
                                        DecisionState(outcomes=['Low','Medium','High'], conditions=lambda x: 'Low' if x.data<98 else 'Medium'),
                                        transitions={'Low': 'L_B', 'Medium': 'M_B', 'High': 'H_B'},
                                        autonomy={'Low': Autonomy.Off, 'Medium': Autonomy.Off, 'High': Autonomy.Off},
                                        remapping={'input_value': 'battery_level'})
 
 
        return _state_machine
 
 
    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]