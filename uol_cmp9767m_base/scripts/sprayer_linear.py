#!/usr/bin/env python

import rospy
from gazebo_msgs.srv import SpawnModel, SpawnModelRequest
from uuid import uuid4
from uol_cmp9767m_base.srv import y_axes_diff, y_axes_diffResponse

BOX_SDF="""
<?xml version='1.0'?>
<sdf version="1.4">
<model name="killbox">
  <pose>0 0 0 0 0 0</pose>
  <static>true</static>
    <link name="link">
      <inertial>
        <mass>1.0</mass>
        <inertia> <!-- inertias are tricky to compute -->
          <!-- http://gazebosim.org/tutorials?tut=inertia&cat=build_robot -->
          <ixx>0.00083</ixx>       <!-- for a box: ixx = 0.083 * mass * (y*y + z*z) -->
          <ixy>0.0</ixy>         <!-- for a box: ixy = 0 -->
          <ixz>0.0</ixz>         <!-- for a box: ixz = 0 -->
          <iyy>0.00083</iyy>       <!-- for a box: iyy = 0.083 * mass * (x*x + z*z) -->
          <iyz>0.0</iyz>         <!-- for a box: iyz = 0 -->
          <izz>0.0000083</izz>       <!-- for a box: izz = 0.083 * mass * (x*x + y*y) -->
        </inertia>
      </inertial>
      <collision name="collision">
        <geometry>
          <cylinder>
            <radius>0.04</radius>
            <length>0.005</length>
          </cylinder>
        </geometry>
      </collision>
      <visual name="visual">
        <geometry>
          <cylinder>
            <radius>0.04</radius>
            <length>0.005</length>
          </cylinder>
        </geometry>
        <material>
            <ambient>1 0 0 1</ambient>
        </material>
      </visual>
    </link>
  </model>
</sdf>
"""

class Sprayer:
    # The request.initial_pose.position.y is the distance from the center of the sprayer
    def __init__(self):
        self.sdf = BOX_SDF
        #define the services
        self.srv = rospy.Service('/thorvald_002/dynamic_sprayer', y_axes_diff, self.spray)
        #call the service to spawn a little rectangle on gazebo
        self.spawner = rospy.ServiceProxy(
            '/gazebo/spawn_sdf_model', SpawnModel)

    def spray(self, r):
        request = SpawnModelRequest()
        request.model_name = 'killbox_%s' % uuid4()
        request.model_xml = self.sdf
        request.reference_frame = 'thorvald_002/base_link'
        request.initial_pose.position.z = 0.005
        request.initial_pose.position.x = -0.45
        request.initial_pose.orientation.w = 1.0
        request.initial_pose.position.y = r.y_diff

        res = y_axes_diffResponse()
        res.spray_completed = True

        # rospy.sleep(0.5)
        self.spawner(request)
        return res

if __name__ == "__main__":
    rospy.init_node('sprayer')
    Sprayer()
    rospy.spin()
