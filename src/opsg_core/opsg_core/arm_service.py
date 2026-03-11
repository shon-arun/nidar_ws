#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_srvs.srv import SetBool

class ArmingService(Node):
    def __init__(self):
        super().__init__('arm_drone_node')
        # Create a service named 'arm_drone' using the SetBool type
        self.srv = self.create_service(SetBool, 'arm_drone', self.arm_callback)
        self.get_logger().info('Arming service is ready. Waiting for requests...')

    def arm_callback(self, request, response):
        # request.data is a boolean
        if request.data:
            response.success = True
            response.message = 'Drone has been ARMED.'
            self.get_logger().warn('Arming sequence initiated! Motors active.')
        else:
            response.success = True
            response.message = 'Drone has been DISARMED.'
            self.get_logger().info('Disarming sequence initiated. Motors safe.')
        
        return response

def main(args=None):
    rclpy.init(args=args)
    node = ArmingService()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()