#!/usr/bin/env python

from flexbe_core import EventState, Logger
from flexbe_core.proxy import ProxyActionClient

from actionlib_msgs.msg import GoalStatus
from move_base_msgs.msg import *
from geometry_msgs.msg import Pose, Point, Quaternion, Pose2D
from tf import transformations
import math

class MoveBaseState(EventState):
    """
    Navigates a robot to a desired position and orientation using move_base.

    ># waypoint     Pose2D      Target waypoint for navigation.

    <= arrived                  Navigation to target pose succeeded.
    <= failed                   Navigation to target pose failed.
    """

    def __init__(self):
        """Constructor"""

        super(MoveBaseState, self).__init__(outcomes = ['arrived', 'failed'], input_keys = ['Direction', 'curr_pose'])

        self._action_topic = "/move_base"

        self._client = ProxyActionClient({self._action_topic: MoveBaseAction})

        self._arrived = False
        self._failed = False

        # Direction and Correction Parameters
        self.origin = [-12.0,-8.0]
        self.quadrant = 1
        self.turn_metric = [3.25,2.5]
        self.straight_metric = 2.0 
        self.back_metric = 1.0

        # Locations of the Goal and the Charging Stations
        self.charging_station_1=[-8.32, 4.97]
        self.charging_station_2=[6.79, 1.03]
        self.parking_sign=[11.0, -3.0]
        self.parking_point = [13.125, -9.36]
 

    # def init_metrics(self,userdata):
    #     self.turn_metric[0] = userdata.Turn_Metric['x']
    #     self.turn_metric[1] = userdata.Turn_Metric['y']
    #     self.straight_metric = userdata.Straight_Metric

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

            elif status in [GoalStatus.PREEMPTED, GoalStatus.REJECTED, GoalStatus.RECALLED, GoalStatus.ABORTED]:
                Logger.logwarn('Navigation failed: %s' % str(status))
                self._failed = True
                return 'failed'

    #else:
    #   return 'moving'

    def update_quadrant(self, userdata):
        curr_theta = transformations.euler_from_quaternion([0, 0, userdata.curr_pose.pose.orientation.z, userdata.curr_pose.pose.orientation.w])
        angle = curr_theta[2]	
        
        if(angle > - math.pi/4 and angle < math.pi/4 ):
            self.quadrant = 1 
        elif(angle >= math.pi/4 and angle < 3*math.pi/4):
            self.quadrant = 2
        elif(angle < - math.pi/4 and angle >= - 3*math.pi/4 ):
            self.quadrant = 4
        elif(angle < - 3*math.pi/4 or angle >= 3*math.pi/4):
            self.quadrant = 3

		

    def get_point_left(self,userdata):
        self.update_quadrant(userdata)

        # Extract the current pose
        curr_x = userdata.curr_pose.pose.position.x
        curr_y = userdata.curr_pose.pose.position.y
        curr_theta = transformations.euler_from_quaternion([0, 0, userdata.curr_pose.pose.orientation.z, userdata.curr_pose.pose.orientation.w])

        # Determine the new goal points based on the direction 
        if(self.quadrant == 1):
            new_x = curr_x + self.turn_metric[0] - self.origin[0]
            new_y = curr_y + self.turn_metric[1]- self.origin[1]
            new_theta = curr_theta[2] + math.pi/2

        elif(self.quadrant == 2):
            new_x = curr_x - turn_metric[0]- self.origin[0]
            new_y = curr_y + turn_metric[1] - self.origin[1]
            new_theta = curr_theta[2] + math.pi/2

        elif(self.quadrant == 3):
            new_x = curr_x - turn_metric[0] - self.origin[0]
            new_y = curr_y - turn_metric[1] - self.origin[1]
            new_theta = curr_theta[2] + math.pi/2

        elif(self.quadrant == 4):
            new_x = curr_x + turn_metric[0] + self.origin[0] 
            new_y = curr_y - turn_metric[1] - self.origin[1]
            new_theta = curr_theta[2] + math.pi/2

        # Log the changes
        Logger.logwarn("NEW_X: %s" % str(new_x))
        Logger.logwarn("NEW_Y: %s" % str(new_y))
        Logger.logwarn("NEW_theta: %s" % str(new_theta))
        
        Logger.logwarn("Quadrant: %s" % str(self.quadrant))

        # Return the the point that needs to be set for goal
        return (Point(x = new_x, y = new_y), transformations.quaternion_from_euler(0, 0, new_theta) )


    def get_point_right(self,userdata):
        self.update_quadrant(userdata)

        # Extract the current pose
        curr_x = userdata.curr_pose.pose.position.x
        curr_y = userdata.curr_pose.pose.position.y
        curr_theta = transformations.euler_from_quaternion([0, 0, userdata.curr_pose.pose.orientation.z, userdata.curr_pose.pose.orientation.w])

        # Determine the new goal points based on the direction 
        if(self.quadrant == 1):
            new_x = curr_x + self.turn_metric[0] - self.origin[0]
            new_y = curr_y - self.turn_metric[1]- self.origin[1]
            new_theta = curr_theta[2] - math.pi/2

        elif(self.quadrant == 2):
            new_x = curr_x + turn_metric[0] - self.origin[0]
            new_y = curr_y + turn_metric[1] - self.origin[1]
            new_theta = curr_theta[2] - math.pi/2

        elif(self.quadrant == 3):
            new_x = curr_x - turn_metric[0] - self.origin[0]
            new_y = curr_y + turn_metric[1] - self.origin[1]
            new_theta = curr_theta[2] - math.pi/2

        elif(self.quadrant == 4):
            new_x = curr_x - turn_metric[0] - self.origin[0] 
            new_y = curr_y - turn_metric[1] - self.origin[1]
            new_theta = curr_theta[2] - math.pi/2

        # Log the changes
        Logger.logwarn("NEW_X: %s" % str(new_x))
        Logger.logwarn("NEW_Y: %s" % str(new_y))
        Logger.logwarn("NEW_theta: %s" % str(new_theta))
        
        Logger.logwarn("Quadrant: %s" % str(self.quadrant))

        # Return the the point that needs to be set for goal
        return (Point(x = new_x, y = new_y), transformations.quaternion_from_euler(0, 0, new_theta) )


    def stop_point(self,userdata):

        # Extract the current pose
        curr_x = userdata.curr_pose.pose.position.x
        curr_y = userdata.curr_pose.pose.position.y
        curr_theta = transformations.euler_from_quaternion([0, 0, userdata.curr_pose.pose.orientation.z, userdata.curr_pose.pose.orientation.w])

        new_x = curr_x - self.origin[0] 
        new_y = curr_y - self.origin[1]
        new_theta = curr_theta[2]

        # Log the changes
        Logger.logwarn("NEW_X: %s" % str(new_x))
        Logger.logwarn("NEW_Y: %s" % str(new_y))
        Logger.logwarn("NEW_theta: %s" % str(new_theta))
        
        Logger.logwarn("Quadrant: %s" % str(self.quadrant))

        # Return the the point that needs to be set for goal
        return (Point(x = new_x, y = new_y), transformations.quaternion_from_euler(0, 0, new_theta) )

    def get_parking_point(self, userdata):
        # self.update_quadrant(userdata)

        curr_x = userdata.curr_pose.pose.position.x
        curr_y = userdata.curr_pose.pose.position.y
        curr_theta = transformations.euler_from_quaternion([0, 0, userdata.curr_pose.pose.orientation.z, userdata.curr_pose.pose.orientation.w])

        new_x = 7.00 
        new_y = 0.85
        new_theta = 1.4*math.pi/2

        return (Point(x = new_x, y = new_y), transformations.quaternion_from_euler(0, 0, new_theta) )

    def get_point_back(self, userdata):
        self.update_quadrant(userdata)

        curr_x = userdata.curr_pose.pose.position.x
        curr_y = userdata.curr_pose.pose.position.y
        curr_theta = transformations.euler_from_quaternion([0, 0, userdata.curr_pose.pose.orientation.z, userdata.curr_pose.pose.orientation.w])

        if(self.quadrant == 1):
            new_x = curr_x - self.back_metric - self.origin[0]
            new_y = curr_y - self.origin[1]
            new_theta = curr_theta[2]

        elif(self.quadrant == 2):
            new_x = curr_x - self.origin[0]
            new_y = curr_y - self.back_metric - self.origin[1]
            new_theta = curr_theta[2]

        elif(self.quadrant == 3):
            new_x = curr_x + self.back_metric - self.origin[0]
            new_y = curr_y - self.origin[1]
            new_theta = curr_theta[2]

        elif(self.quadrant == 4):
            new_x = curr_x - self.origin[0] 
            new_y = curr_y + self.back_metric - self.origin[1]
            new_theta = curr_theta[2]

        # Log the changes
        Logger.logwarn("NEW_X: %s" % str(new_x))
        Logger.logwarn("NEW_Y: %s" % str(new_y))
        Logger.logwarn("NEW_theta: %s" % str(new_theta))
        
        Logger.logwarn("Quadrant: %s" % str(self.quadrant))

        # Return the the point that needs to be set for goal
        return (Point(x = new_x, y = new_y), transformations.quaternion_from_euler(0, 0, new_theta) )

    def get_point_straight(self, userdata):
	
        #If the waypoint is a global co-ordinate	
    	# if(userdata.waypoint["increment"]["x"]=='none' and userdata.waypoint["increment"]["y"]=='none' and userdata.waypoint["increment"]["theta"]=='none'):

     #        Logger.logwarn("REACHING WAYPOINT COORDINATES:")    
     #        new_x = userdata.waypoint["coordinate"]["x"] - self.origin[0]
     #        new_y = userdata.waypoint["coordinate"]["y"] - self.origin[1]
     #        new_theta = userdata.waypoint["coordinate"]["theta"]
    	
    	# #If the waypoint is an increment
     #    elif(userdata.waypoint["coordinate"]["x"]=='none' and userdata.waypoint["coordinate"]["y"]=='none' and userdata.waypoint["coordinate"]["theta"]=='none'):

     #        #Extract the current pose from the /pose topic
     #        Logger.logwarn("USING CURRENT POSITION")
     #        curr_x = userdata.curr_pose.pose.position.x
     #        curr_y = userdata.curr_pose.pose.position.y
     #        curr_theta = transformations.euler_from_quaternion([0, 0, userdata.curr_pose.pose.orientation.z, userdata.curr_pose.pose.orientation.w])

     #        Logger.logwarn("C_X: %s" % str(curr_x))
     #        Logger.logwarn("C_Y: %s" % str(curr_y))
     #        Logger.logwarn("C_theta: %s" % str(curr_theta))

     #        # Math for Incrementing co-ordinates
     #        Logger.logwarn("INCREMENTING COORDINATES:")
     #        # new_x = curr_x + userdata.waypoint["increment"]["x"]*math.cos(curr_theta[2]) - userdata.waypoint["increment"]["y"]*math.sin(curr_theta[2])
     #        # new_y = curr_y + userdata.waypoint["increment"]["x"]*math.sin(curr_theta[2]) + userdata.waypoint["increment"]["y"]*math.cos(curr_theta[2])
     #        # new_theta = curr_theta[2] + userdata.waypoint["increment"]["theta"]

    	#     new_x = curr_x + userdata.waypoint["increment"]["x"] - self.origin[0]
     #        new_y = curr_y + userdata.waypoint["increment"]["y"] - self.origin[1]
     #        new_theta = curr_theta[2] + userdata.waypoint["increment"]["theta"]


     #    else:
     #        Logger.logwarn("TOO MANY INPUT: CAN'T SET WAYPOINT AND INCREMENT AT THE SAME TIME!")        
            
        
        self.update_quadrant(userdata)

        curr_x = userdata.curr_pose.pose.position.x
        curr_y = userdata.curr_pose.pose.position.y
        curr_theta = transformations.euler_from_quaternion([0, 0, userdata.curr_pose.pose.orientation.z, userdata.curr_pose.pose.orientation.w])

        if(self.quadrant == 1):
            new_x = curr_x + self.straight_metric - self.origin[0]
            new_y = curr_y - self.origin[1]
            new_theta = curr_theta[2]

        elif(self.quadrant == 2):
            new_x = curr_x - self.origin[0]
            new_y = curr_y + self.straight_metric - self.origin[1]
            new_theta = curr_theta[2]

        elif(self.quadrant == 3):
            new_x = curr_x - self.straight_metric - self.origin[0]
            new_y = curr_y - self.origin[1]
            new_theta = curr_theta[2]

        elif(self.quadrant == 4):
            new_x = curr_x - self.origin[0] 
            new_y = curr_y - self.straight_metric - self.origin[1]
            new_theta = curr_theta[2]

        # Log the changes
        Logger.logwarn("NEW_X: %s" % str(new_x))
        Logger.logwarn("NEW_Y: %s" % str(new_y))
        Logger.logwarn("NEW_theta: %s" % str(new_theta))
    	
    	Logger.logwarn("Quadrant: %s" % str(self.quadrant))

        # Return the the point that needs to be set for goal
    	return (Point(x = new_x, y = new_y), transformations.quaternion_from_euler(0, 0, new_theta) )


    def battery_point_in(self, userdata):
        # self.update_quadrant(userdata)

        curr_x = userdata.curr_pose.pose.position.x
        curr_y = userdata.curr_pose.pose.position.y
        curr_theta = transformations.euler_from_quaternion([0, 0, userdata.curr_pose.pose.orientation.z, userdata.curr_pose.pose.orientation.w])

        new_x = 2.4
        new_y = -0.8
        new_theta = - 1.2*math.pi/2

        return (Point(x = new_x, y = new_y), transformations.quaternion_from_euler(0, 0, new_theta) )

    def battery_point_out(self, userdata):

        new_x = 5 
        new_y = 0.0
        new_theta = 0.0

        return (Point(x = new_x, y = new_y), transformations.quaternion_from_euler(0, 0, new_theta) )
    
    def on_enter(self, userdata):
        """Create and send action goal"""
 
        # self.init_metrics(userdata)

        self._arrived = False
        self._failed = False
 
        # Create and populate action goal
        goal = MoveBaseGoal()

    	# Extract the point        
    	if(userdata.Direction == 'Straight'):
            pt, qt = self.get_point_straight(userdata)

        elif(userdata.Direction == 'Back'):
            pt, qt = self.get_point_back(userdata)

        elif(userdata.Direction == 'Left'):
            pt, qt = self.get_point_left(userdata)

        elif(userdata.Direction == 'Right'):
            pt, qt = self.get_point_right(userdata)

        elif(userdata.Direction == 'Stop'):
            pt, qt = self.stop_point(userdata)
        elif(userdata.Direction == 'Parking'):
            pt, qt = self.get_parking_point(userdata)

        elif(userdata.Direction == 'Battery_in'):
            pt, qt = self.battery_point_in(userdata)

        elif(userdata.Direction == 'Battery_out'):
            pt, qt = self.battery_point_out(userdata)

        else:
            Logger.logwarn("Direction not Detemined")


    	#Create Action goal        
    	goal.target_pose.pose = Pose(position = pt, orientation = Quaternion(*qt))

        goal.target_pose.header.frame_id = "map"
       
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
        pass

    def on_stop(self):
        self.cancel_active_goals()
        pass
