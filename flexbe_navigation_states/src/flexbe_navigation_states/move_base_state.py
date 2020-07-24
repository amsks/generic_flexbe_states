#!/usr/bin/env python

from flexbe_core import EventState, Logger
from flexbe_core.proxy import ProxyActionClient

from actionlib_msgs.msg import GoalStatus
from move_base_msgs.msg import *
from geometry_msgs.msg import Pose, Point, Quaternion, Pose2D
from tf import transformations
import math

"""
Created on 11/19/2015

@author: Spyros Maniatopoulos
"""

class MoveBaseState(EventState):
    """
    Navigates a robot to a desired position and orientation using move_base.

    ># waypoint     Pose2D      Target waypoint for navigation.

    <= arrived                  Navigation to target pose succeeded.
    <= failed                   Navigation to target pose failed.
    """

    def __init__(self):
        """Constructor"""

        super(MoveBaseState, self).__init__(outcomes = ['arrived', 'failed'],
                                            input_keys = ['waypoint', 'incremental'])

        self._action_topic = "/move_base"

        self._client = ProxyActionClient({self._action_topic: MoveBaseAction})

        self._arrived = False
        self._failed = False


    def execute(self, userdata):
        """Wait for action result and return outcome accordingly"""

        if self._arrived:
            return 'arrived'
        if self._failed:
            return 'failed'

        if self._client.has_result(self._action_topic):
            status = self._client.get_state(self._action_topic)
            if status == GoalStatus.SUCCEEDED:
                self._arrived = True
                return 'arrived'
            elif status in [GoalStatus.PREEMPTED, GoalStatus.REJECTED,
                            GoalStatus.RECALLED, GoalStatus.ABORTED]:
                Logger.logwarn('Navigation failed: %s' % str(status))
                self._failed = True
                return 'failed'


    def on_enter(self, userdata):
        """Create and send action goal"""

        self._arrived = False
        self._failed = False

        # Create and populate action goal
        goal = MoveBaseGoal()





	#DEFINE COMMON POINTS################################
	if(userdata.waypoint=="ZER0"):
		curr_x = -12
		curr_y = -8
		curr_theta = [0, 0, 0]

	else:
        	Logger.logwarn("USING CURRENT POSITION")
		curr_x = userdata.waypoint.pose.position.x
		curr_y = userdata.waypoint.pose.position.y	
		curr_theta = transformations.euler_from_quaternion([0, 0, userdata.waypoint.pose.orientation.z, userdata.waypoint.pose.orientation.w])


	new_x = curr_x + userdata.incremental[0]*math.cos(curr_theta[2]) - userdata.incremental[1]*math.sin(curr_theta[2])
	new_y = curr_y + userdata.incremental[0]*math.sin(curr_theta[2]) + userdata.incremental[1]*math.cos(curr_theta[2])
	new_theta = curr_theta[2] + userdata.incremental[2]



        Logger.logwarn("NEW_X: %s" % str(new_x))
        Logger.logwarn("C_X: %s" % str(curr_x))
        Logger.logwarn("NEW_Y: %s" % str(new_y))
        Logger.logwarn("C_Y: %s" % str(curr_y))
        Logger.logwarn("NEW_Z: %s" % str(new_theta))
        Logger.logwarn("C_Z: %s" % str(curr_theta))


        pt = Point(x = new_x, y = new_y)
        qt = transformations.quaternion_from_euler(0, 0, new_theta)

        goal.target_pose.pose = Pose(position = pt,
                                     orientation = Quaternion(*qt))

        goal.target_pose.header.frame_id = "odom"
        # goal.target_pose.header.stamp.secs = 5.0

        # Send the action goal for execution
        try:
            self._client.send_goal(self._action_topic, goal)
        except Exception as e:
            Logger.logwarn("Unable to send navigation action goal:\n%s" % str(e))
            self._failed = True
            
    def cancel_active_goals(self):
        if self._client.is_available(self._action_topic):
            if self._client.is_active(self._action_topic):
                if not self._client.has_result(self._action_topic):
                    self._client.cancel(self._action_topic)
                    Logger.loginfo('Cancelled move_base active action goal.')

    def on_exit(self, userdata):
        self.cancel_active_goals()

    def on_stop(self):
        self.cancel_active_goals()
