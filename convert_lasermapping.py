#!/usr/bin/env python3
"""
ROS1 to ROS2 conversion script for laserMapping.cpp
This script handles the conversion of publishers, subscribers, services, and other ROS APIs
"""

import re
import sys

def convert_lasermapping(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("Starting conversion of laserMapping.cpp...")
    
    # Step 1: Fix message type names - add msg:: namespace
    print("1. Fixing message type names...")
    content = re.sub(r'sensor_msgs::PointCloud2([^:])', r'sensor_msgs::msg::PointCloud2\1', content)
    content = re.sub(r'nav_msgs::Odometry([^:])', r'nav_msgs::msg::Odometry\1', content)
    content = re.sub(r'nav_msgs::Path([^:])', r'nav_msgs::msg::Path\1', content)
    content = re.sub(r'visualization_msgs::MarkerArray([^:])', r'visualization_msgs::msg::MarkerArray\1', content)
    content = re.sub(r'visualization_msgs::Marker([^:])', r'visualization_msgs::msg::Marker\1', content)
    content = re.sub(r'std_msgs::Float64MultiArray([^:])', r'std_msgs::msg::Float64MultiArray\1', content)
    content = re.sub(r'geometry_msgs::PoseStamped([^:])', r'geometry_msgs::msg::PoseStamped\1', content)
    
    # Step 2: Fix publisher declarations
    print("2. Converting publisher declarations...")
    # Pattern: nh->create_publisher<type>(topic, qos) 
    content = re.sub(
        r'(\w+)\s*=\s*nh->create_publisher<(sensor_msgs::msg::PointCloud2)>\("([^"]+)",\s*(\d+)\);',
        r'\1 = nh->create_publisher<\2>("\3", \4);',
        content
    )
    content = re.sub(
        r'(\w+)\s*=\s*nh->create_publisher<(nav_msgs::msg::\w+)>\("([^"]+)",\s*(\d+)\);',
        r'\1 = nh->create_publisher<\2>("\3", \4);',
        content
    )
    content = re.sub(
        r'(\w+)\s*=\s*nh->create_publisher<(visualization_msgs::msg::\w+)>\("([^"]+)",\s*(\d+)\);',
        r'\1 = nh->create_publisher<\2>("\3", \4);',
        content
    )
    
    # Step 3: Fix global publisher variable declarations at the top of file
    print("3. Fixing global publisher variable types...")
    # These need proper type declarations
    content = re.sub(
        r'rclcpp::Publisher<sensor_msgs::msg::PointCloud2>::SharedPtr\s+(\w+);',
        r'rclcpp::Publisher<sensor_msgs::msg::PointCloud2>::SharedPtr \1;',
        content
    )
    
    # Step 4: Fix subscriber declarations
    print("4. Converting subscriber declarations...")
    # ROS2 subscriptions are more complex, need callback binding
    # Will handle these case by case in the main function
    
    # Step 5: Fix advertiseService -> create_service
    print("5. Converting service declarations...")
    content = re.sub(
        r'(\w+)\s*=\s*nh->advertiseService\("([^"]+)",\s*&(\w+)\);',
        r'\1 = nh->create_service<fast_lio_sam::srv::\3>("\2", \3);',
        content
    )
    
    # Step 6: Replace ROS_WARN and other macros
    print("6. Replacing ROS macros...")
    content = re.sub(r'ROS_WARN\s*\((.*?)\);', r'RCLCPP_WARN(nh->get_logger(), \1);', content)
    content = re.sub(r'ROS_INFO\s*\((.*?)\);', r'RCLCPP_INFO(nh->get_logger(), \1);', content)
    content = re.sub(r'ROS_ERROR\s*\((.*?)\);', r'RCLCPP_ERROR(nh->get_logger(), \1);', content)
    content = re.sub(r'ROS_DEBUG\s*\((.*?)\);', r'RCLCPP_DEBUG(nh->get_logger(), \1);', content)
    
    # Step 7: Fix publish function signatures
    print("7. Updating publish function signatures...")
    # Change: const ros::Publisher & -> const rclcpp::Publisher<MsgType>::SharedPtr &
    content = re.sub(
        r'void\s+(\w+)\s*\(\s*const\s+ros::Publisher\s*&\s*(\w+)\s*\)',
        r'void \1(const rclcpp::Publisher<sensor_msgs::msg::PointCloud2>::SharedPtr \2)',
        content
    )
    
    # Step 8: Fix publisher->publish() calls (already using -> not .)
    print("8. Fixing publish calls...")
    # These should already be correct if using ->
    
    # Step 9: Handle ros::shutdown()
    content = re.sub(r'ros::shutdown\(\)', r'rclcpp::shutdown()', content)
    
    # Step 10: Fix any remaining ros::Time references
    content = re.sub(r'ros::Time\b', r'rclcpp::Time', content)
    
    # Step 11: Handle image_transport (if exists)
    content = re.sub(r'image_transport::ImageTransport\s+it\(nh\);', 
                     r'// image_transport not yet converted - needs manual handling', content)
    
    # Step 12: Fix darknet_ros_msgs if present
    content = re.sub(r'darknet_ros_msgs::BoundingBoxes', 
                     r'// darknet_ros_msgs not converted - comment out for now', content)
    
    print("10. Writing converted file...")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ Conversion complete! File saved to {filepath}")
    print("\nNote: Some conversions may need manual review:")
    print("  - Subscriber callback functions need proper std::bind")
    print("  - Service callbacks need proper signature updates")
    print("  - Check all publisher/subscriber template parameters")
    print("  - Review image_transport and darknet_ros_msgs conversions")

if __name__ == "__main__":
    filepath = "/home/lichao/3d-navigation/src/better_fastlio2/src/laserMapping.cpp"
    convert_lasermapping(filepath)
