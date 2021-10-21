# Copyright 2016 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import rclpy
from rclpy import publisher
from rclpy import time
from rclpy.node import Node
from rclpy.qos import QoSDurabilityPolicy, QoSHistoryPolicy, QoSReliabilityPolicy
from rclpy.qos import QoSProfile
from time import sleep
import random

from std_msgs.msg import String
from aerostack2_msgs.msg import TrajectoryWaypoints
from geometry_msgs.msg import PoseStamped


class MinimalPublisher(Node):

    def __init__(self, drone_id='drone0'):
        super().__init__('minimal_publisher')

        topic_name = 'motion_reference/waypoints'
        
        if self.get_namespace() == '/':
            topic_name = drone_id + '/' + topic_name

        self.publisher_ = self.create_publisher(TrajectoryWaypoints, topic_name, 10)
        # print('waiting')
        sleep(0.1)
        

    def send_points(self,point_list,speed,yaw_mode = TrajectoryWaypoints.KEEP_YAW):
        msg = TrajectoryWaypoints()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = "odom"
        # msg.yaw_mode = TrajectoryWaypoints.KEEP_YAW
        msg.yaw_mode = yaw_mode
        poses = []
        for point in point_list:
            pose = PoseStamped()
            x,y,z = point
            pose.pose.position.x = (float)(x)
            pose.pose.position.y = (float)(y)
            pose.pose.position.z = (float)(z)
            pose.pose.orientation.w=1.0
            poses.append(pose)
        msg.poses = poses
        msg.max_speed = (float)(speed)
        print("Sending message : ", point_list)
        self.publisher_.publish(msg)


def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher(drone_id="drone_sim_0")

    # point_lists = [[0,0,-2]]
    # point_lists = [[0.0,0,1],[-1,-1,1],[1,-1,1]]
    
    point_lists = [[0,0,1]]
    point_lists = [[3,2,5],[-3,4,3],[3,-4,4]]

    # add random noise to the last points of the list
    for i in range(len(point_lists)):
        point_lists[i][0] += 0.1*(2*random.random()-1)
        point_lists[i][1] += 0.1*(2*random.random()-1)
        point_lists[i][2] += 0.1*(2*random.random()-1)
         
 
    # point_lists = [[3,0,5],[0,0,5],[-3,0,5]]
    # point_lists = point_lists[::-1]
    # point_lists = [[3,2,5],[3,4,3],[3,-4,4],[3,2,5],[3,4,3],[3,-4,4],[3,2,5],[3,4,3],[3,-4,4],[3,2,5],[3,4,3],[3,-4,4],[3,2,5],[3,4,3],[3,-4,4]]
    minimal_publisher.send_points(point_lists,2.5,TrajectoryWaypoints.PATH_FACING)
    #sleep(6)
    # minimal_publisher.send_points(point_lists,6.5,TrajectoryWaypoints.PATH_FACING)
    #sleep(15)
    #point_lists = [[0,0,-5]]
    #minimal_publisher.send_points(point_lists,0.5,TrajectoryWaypoints.KEEP_YAW)


    # rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    
    minimal_publisher.destroy_node()
    # rclpy.shutdown()


if __name__ == '__main__':
    main()