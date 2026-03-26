#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class CameraViewerNode(Node):
    def __init__(self):
        super().__init__('camera_viewer_node')
        
        # 1. Initialize the Translator
        self.bridge = CvBridge()
        
        # 2. Subscribe to the ROS 2 Image Topic
        self.image_sub = self.create_subscription(
            Image, 
            '/camera/image_raw', 
            self.image_callback, 
            10)
        
        self.get_logger().info('Camera Viewer Node Active. Waiting for /camera/image_raw...')

    def image_callback(self, msg):
        try:
            # 3. Translate: ROS 2 Image -> OpenCV Matrix (BGR 8-bit format)
            cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
            
            # 4. Display the image using OpenCV
            cv2.imshow("Nidar Drone - Live Nadir Feed", cv_image)
            
            # This 1ms delay is required for OpenCV to actually render the window
            cv2.waitKey(1) 
            
        except Exception as e:
            self.get_logger().error(f"Failed to convert image: {e}")

def main(args=None):
    rclpy.init(args=args)
    node = CameraViewerNode()
    rclpy.spin(node)
    
    # Clean up the OpenCV windows when the node shuts down
    cv2.destroyAllWindows()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()