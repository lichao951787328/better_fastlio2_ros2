#!/bin/bash
# ROS1 to ROS2 migration helper script

echo "Starting ROS1 to ROS2 migration for source files..."

# Backup original files
backup_dir="ros1_backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$backup_dir"
cp -r src/*.cpp "$backup_dir/"
cp -r include/*.h "$backup_dir/" 2>/dev/null || true
echo "Backup created in $backup_dir"

# Function to replace in all cpp and h files
replace_in_files() {
    find src include -type f \( -name "*.cpp" -o -name "*.h" -o -name "*.hpp" \) -exec sed -i "$1" {} +
}

# Replace ROS1 message types with ROS2
echo "Replacing ROS1 headers..."
replace_in_files 's|<ros/ros\.h>|<rclcpp/rclcpp.hpp>|g'
replace_in_files 's|#include <sensor_msgs/Imu\.h>|#include <sensor_msgs/msg/imu.hpp>|g'
replace_in_files 's|#include <sensor_msgs/PointCloud2\.h>|#include <sensor_msgs/msg/point_cloud2.hpp>|g'
replace_in_files 's|#include <nav_msgs/Odometry\.h>|#include <nav_msgs/msg/odometry.hpp>|g'
replace_in_files 's|#include <nav_msgs/Path\.h>|#include <nav_msgs/msg/path.hpp>|g'
replace_in_files 's|#include <std_msgs/|#include <std_msgs/msg/|g'
replace_in_files 's|#include <geometry_msgs/|#include <geometry_msgs/msg/|g'
replace_in_files 's|#include <visualization_msgs/|#include <visualization_msgs/msg/|g'

# Replace message type names
echo "Replacing message type names..."
replace_in_files 's|sensor_msgs::Imu|sensor_msgs::msg::Imu|g'
replace_in_files 's|sensor_msgs::PointCloud2|sensor_msgs::msg::PointCloud2|g'
replace_in_files 's|nav_msgs::Odometry|nav_msgs::msg::Odometry|g'
replace_in_files 's|nav_msgs::Path|nav_msgs::msg::Path|g'
replace_in_files 's|std_msgs::Header|std_msgs::msg::Header|g'
replace_in_files 's|geometry_msgs::PoseStamped|geometry_msgs::msg::PoseStamped|g'
replace_in_files 's|geometry_msgs::Quaternion|geometry_msgs::msg::Quaternion|g'

echo "Migration script completed. Please review changes and compile."
echo "Original files backed up to: $backup_dir"
