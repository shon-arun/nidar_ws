#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_srvs.srv import SetBool
from px4_msgs.msg import VehicleCommand

class ArmingService(Node):
    def __init__(self):
        super().__init__('arm_drone_node')

        # Create a service named 'arm_drone' using the SetBool type
        self.srv = self.create_service(SetBool, 'arm_drone', self.arm_callback)
        
        # The Publisher: Sends the physical command to PX4
        self.command_pub = self.create_publisher(VehicleCommand, '/fmu/in/vehicle_command', 10)
        
        self.get_logger().info('Arming service is ready. Send True to Arm, False to Disarm. Waiting for requests...')

    def arm_callback(self, request, response):
        command_msg = VehicleCommand()

        # The MAVLink command ID for arming/disarming
        command_msg.command = VehicleCommand.VEHICLE_CMD_COMPONENT_ARM_DISARM

        # request.data is a boolean
        if request.data:
            command_msg.param1 = 1.0  # 1.0 = Arm
            response.success = True
            response.message = 'Drone has been ARMED.'
            self.get_logger().warn('Arming sequence initiated! Motors active.')
        else:
            command_msg.param1 = 0.0  # 0.0 = Disarm
            response.success = True
            response.message = 'Drone has been DISARMED.'
            self.get_logger().info('Disarming sequence initiated. Motors safe.')
        
        # Required PX4 Target/Source IDs
        command_msg.target_system = 1
        command_msg.target_component = 1
        command_msg.source_system = 1
        command_msg.source_component = 1
        command_msg.from_external = True

        # Stamp it with the current time
        command_msg.timestamp = int(self.get_clock().now().nanoseconds / 1000)
        
        self.command_pub.publish(command_msg)
        
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