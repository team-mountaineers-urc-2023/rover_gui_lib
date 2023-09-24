#!/usr/bin/env python3.8

from urc_gui_common import RosLink

from PyQt5.QtCore import pyqtSignal as Signal

import rospy

from std_srvs.srv import SetBool, SetBoolRequest, SetBoolResponse

from rover_gui_lib.msg import EDWaypointList

class RoverRosLink(RosLink):
	"""Supply signals for the Qt app, originating from topic callbacks."""

	ed_waypoint_list = Signal(EDWaypointList)

	def __init__(self):
		super().__init__()

		### ed ###############################################################

		ed_waypoint_list_topic = rospy.get_param("~ed_waypoint_list_topic")
		self.ed_waypoint_list_sub = self.make_subscriber(ed_waypoint_list_topic, EDWaypointList, self.ed_waypoint_list)
		self.ed_waypoint_list_pub = rospy.Publisher(ed_waypoint_list_topic, EDWaypointList, queue_size=1)

		### drivetrain #######################################################

		drive_forward_service = rospy.get_param("~drive_forward_service")
		car_style_turning_service = rospy.get_param("~car_style_turning_service")

		self.drive_forward_serv = rospy.ServiceProxy(drive_forward_service, SetBool)
		self.car_style_turning_serv = rospy.ServiceProxy(car_style_turning_service, SetBool)

	### ed ###################################################################

	def publish_ed_waypoints(self, ed_waypoint_list: EDWaypointList):
		self.ed_waypoint_list_pub.publish(ed_waypoint_list)

	### drivetrain ###########################################################

	def change_drive_direction(self, forward: bool) -> SetBoolResponse:
		return self.drive_forward_serv(SetBoolRequest(data=forward))

	def change_car_turning_style(self, car: bool) -> SetBoolResponse:
		return self.car_style_turning_serv(SetBoolRequest(data=car))
	
if __name__ == "__main__":
	rospy.loginfo("Starting GUI Rover ROS link")
	roslink = RoverRosLink()
	rospy.spin()
