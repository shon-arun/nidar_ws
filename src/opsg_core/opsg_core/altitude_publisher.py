#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from px4_msgs.msg import VehicleOdometry
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy, HistoryPolicy

class AltitudePublisher(Node):
    def __init__(self):
        super().__init__('altitude_node')
        
        # Create a QoS profile matching PX4's DDS bridge
        px4_qos_profile = QoSProfile(reliability=ReliabilityPolicy.BEST_EFFORT, durability=DurabilityPolicy.TRANSIENT_LOCAL, history=HistoryPolicy.KEEP_LAST, depth=1)
    
        # Subscribe to the LIVE PX4 telemetry from the DDS Bridge
        self.odom_sub = self.create_subscription(VehicleOdometry, '/fmu/out/vehicle_odometry', self.odom_callback, px4_qos_profile)
        
        # Create the publisher for /drone_altitude
        self.publisher_ = self.create_publisher(Float32, '/drone_altitude', 10)
        
        # # Publish exactly twice a second (0.5 seconds)
        # self.timer = self.create_timer(0.5, self.timer_callback)
        # self.current_altitude = 0.0

        self.get_logger().info('Live Altitude Node Active: Translating PX4 Odometry to /drone_altitude...')

    def timer_callback(self):
        msg = Float32()
        msg.data = self.current_altitude
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing Drone Altitude: {msg.data} m')
        
        # Simulate the drone slowly ascending
        self.current_altitude += 0.5

    def odom_callback(self, msg):
        # Of course.... Poof.....
        # The Secret Hack: PX4 uses NED (North, East, Down).
        # Because Z is 'Down', we have to multiply by -1 to get real altitude!
        real_altitude = -msg.position[2]
        
        alt_msg = Float32()
        alt_msg.data = float(real_altitude)
        self.publisher_.publish(alt_msg)

def main(args=None):
    rclpy.init(args=args)
    node = AltitudePublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()