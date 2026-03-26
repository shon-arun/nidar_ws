#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import Point
from cv_bridge import CvBridge
import cv2
from ultralytics import YOLO

class YoloDetectionNode(Node):
    def __init__(self):
        super().__init__('yolo_detection_node')
        
        self.bridge = CvBridge()
        
        # Load the pretrained YOLOv8 Nano model (super lightweight)
        self.get_logger().info('Loading YOLOv8 model...')
        self.model = YOLO('yolov8n.pt') 
        self.get_logger().info('Model loaded successfully!')
        
        # 1. The Subscriber: Grabbing the raw feed
        self.image_sub = self.create_subscription(
            Image, '/camera/image_raw', self.image_callback, 10)
            
        # 2. The Publisher: Broadcasting the detection coordinates
        self.detection_pub = self.create_publisher(
            Point, '/human_detection', 10)

    def image_callback(self, msg):
        try:
            # Translate ROS -> OpenCV
            cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
            
            # Run YOLO inference. classes=[0] forces it to ONLY look for humans.
            results = self.model(cv_image, classes=[0], verbose=False)
            
            # Loop through the detections
            for r in results:
                boxes = r.boxes
                for box in boxes:
                    # Extract bounding box coordinates (Top-Left and Bottom-Right)
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    
                    # Calculate center point and extract confidence
                    center_x = float((x1 + x2) / 2)
                    center_y = float((y1 + y2) / 2)
                    confidence = float(box.conf[0])
                    
                    # Construct and publish the message
                    det_msg = Point()
                    det_msg.x = center_x
                    det_msg.y = center_y
                    det_msg.z = confidence # Z doubles as our confidence score
                    self.detection_pub.publish(det_msg)
                    
                    # Draw the bounding box and label on the image for the deliverable
                    cv2.rectangle(cv_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    label = f"Human: {confidence:.2f}"
                    cv2.putText(cv_image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Display the annotated feed
            cv2.imshow("Nidar Drone - YOLO Human Detection", cv_image)
            cv2.waitKey(1) 
            
        except Exception as e:
            self.get_logger().error(f"Detection error: {e}")

def main(args=None):
    rclpy.init(args=args)
    node = YoloDetectionNode()
    rclpy.spin(node)
    cv2.destroyAllWindows()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()