import rclpy

import math

from rclpy.node import Node

from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class AvoidNode(Node):

    def __init__(self):
        super().__init__('avoid_node')

        self.scan_sub = self.create_subscription(LaserScan,'/scan',self.scan_callback,10)

        self.cmd_pub = self.create_publisher(Twist,'/cmd_vel',10)



        self.get_logger().info("Avoid node started")

    def scan_callback(self,msg):

        cmd = Twist()

        front_ranges = []


        for i,distance in enumerate(msg.ranges):
            angle = msg.angle_min + i * msg.angle_increment

            if -math.pi / 3.5 <= angle <= math.pi / 3.5:
                if math.isfinite(distance):

                    #Appending all distance figures and corresponding angle
                    front_ranges.append((distance,angle)) 

        front_distance, front_angle = min(front_ranges, key=lambda p: p[0], default=(float('inf') , 0.0))
        



        if front_distance < 0.8:
            cmd.linear.x = 0.0
            if front_angle < 0:
                cmd.angular.z = -math.pi / 2
            elif front_angle > 0:
                cmd.angular.z = math.pi / 2
        else:
            cmd.linear.x = 0.3

        self.cmd_pub.publish(cmd)
        




def main(args=None):
    rclpy.init(args=args)
    node = AvoidNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()