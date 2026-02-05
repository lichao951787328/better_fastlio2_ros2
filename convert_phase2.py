#!/usr/bin/env python3
"""
Phase 2: Handle complex conversions for laserMapping.cpp
- Global publisher variable declarations
- Subscriber creation with proper types
- Service definitions
"""

import re

def phase2_conversion(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print("Phase 2: Handling complex conversions...")
    
    # Find the section with global publishers (around line 175-210)
    in_publisher_section = False
    modified_lines = []
    
    for i, line in enumerate(lines):
        # Detect publisher declarations that need type fixing
        if 'rclcpp::Publisher<sensor_msgs::msg::PointCloud2>::SharedPtr' in line and '=' not in line:
            # This is a global variable declaration, needs specific types
            if 'pubLaserCloudSurround' in line:
                modified_lines.append('rclcpp::Publisher<sensor_msgs::msg::PointCloud2>::SharedPtr pubLaserCloudSurround;\n')
            elif 'pubOptimizedGlobalMap' in line:
                modified_lines.append('rclcpp::Publisher<sensor_msgs::msg::PointCloud2>::SharedPtr pubOptimizedGlobalMap;\n')
            elif 'pubLidarPCL' in line:
                modified_lines.append('rclcpp::Publisher<sensor_msgs::msg::PointCloud2>::SharedPtr pubLidarPCL;\n')
            elif 'pubHistoryKeyFrames' in line:
                modified_lines.append('rclcpp::Publisher<sensor_msgs::msg::PointCloud2>::SharedPtr pubHistoryKeyFrames;\n')
            elif 'pubIcpKeyFrames' in line:
                modified_lines.append('rclcpp::Publisher<sensor_msgs::msg::PointCloud2>::SharedPtr pubIcpKeyFrames;\n')
            elif 'pubLoopConstraintEdge' in line:
                modified_lines.append('rclcpp::Publisher<visualization_msgs::msg::MarkerArray>::SharedPtr pubLoopConstraintEdge;\n')
            else:
                modified_lines.append(line)
        
        # Fix subscriber declarations - these are trickier
        elif 'rclcpp::Subscription<sensor_msgs::msg::PointCloud2>::SharedPtr sub_pcl' in line:
            # This needs complete rewrite, will be handled in main function
            modified_lines.append('// Subscriber declarations - see main function\n')
        elif 'rclcpp::Subscription<sensor_msgs::msg::PointCloud2>::SharedPtr sub_imu' in line:
            modified_lines.append('// IMU subscriber - see main function\n')
        
        # Fix livox_ros_driver -> livox_ros_driver2
        elif 'livox_ros_driver::' in line:
            modified_lines.append(line.replace('livox_ros_driver::', 'livox_ros_driver2::msg::'))
        
        # Fix service definitions
        elif 'srvSaveMap' in line and '=' in line:
            modified_lines.append('// Service declarations handled below\n')
        elif 'srvSavePose' in line and '=' in line:
            modified_lines.append('// Service declarations handled below\n')
        
        else:
            modified_lines.append(line)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(modified_lines)
    
    print("✓ Phase 2 complete!")

if __name__ == "__main__":
    filepath = "/home/lichao/3d-navigation/src/better_fastlio2/src/laserMapping.cpp"
    phase2_conversion(filepath)
