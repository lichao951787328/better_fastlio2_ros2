# ROS1 到 ROS2 迁移进度报告

## 项目信息
- **项目名称**: fast_lio_sam (better_fastlio2)
- **源版本**: ROS1 (Noetic)
- **目标版本**: ROS2 (Jazzy)  
- **迁移日期**: 2026年2月5日
- **完成度**: 约85%

## 已完成工作 ✅

### 1. 配置文件迁移
- ✅ **package.xml**: 升级到 format 3，替换所有依赖包名
  - catkin → ament_cmake
  - roscpp → rclcpp
  - 所有消息包名添加 `/msg/` 或 `/srv/` 后缀
  
- ✅ **CMakeLists.txt**: 完全重写为 ament_cmake 格式
  - 替换 catkin 宏为 ament_cmake
  - 添加 rosidl_generate_interfaces 生成消息
  - 配置 typesupport 链接
  - 添加安装规则

### 2. 消息和服务文件
- ✅ 重命名为驼峰命名: `cloud_info.msg` → `CloudInfo.msg`
- ✅ 更新字段名为 snake_case: `startRingIndex` → `start_ring_index`
- ✅ 服务文件重命名: `save_map.srv` → `SaveMap.srv`

### 3. 头文件更新
- ✅ **common_lib.h**: 所有 ROS 头文件已更新
  - `ros/ros.h` → `rclcpp/rclcpp.hpp`
  - `sensor_msgs/Imu.h` → `sensor_msgs/msg/imu.hpp`
  - `tf/...` → `tf2/...` 和 `tf2_ros/...`
  - `cv_bridge/cv_bridge.h` → `cv_bridge/cv_bridge.hpp`
  
- ✅ **preprocess.h**: 更新消息类型和函数签名
  - `ConstPtr` → `SharedPtr`
  - 添加 rclcpp::Publisher 声明

### 4. 依赖库安装
- ✅ GeographicLib
- ✅ GTSAM (ROS2 版本)
- ✅ Python 包: empy, catkin_pkg, numpy

### 5. Launch 文件
- ✅ 创建 ROS2 Python launch 文件示例
  - `mapping_hap_livox.launch.py`

### 6. CMake 配置
- ✅ 添加 GTSAM include 路径
- ✅ 配置消息生成依赖
- ✅ 为所有库添加 ROS2 依赖

## 剩余工作 ⚠️

### 需要修改的源文件（约15%工作量）

#### 1. pose_estimator.cpp (include/online-relo/)
```cpp
// 需要修改：
- nh.param<>(...) → node->declare_parameter() + get_parameter()
- ros::NodeHandle nh → 接受 rclcpp::Node::SharedPtr 参数
```

#### 2. laserMapping.cpp (约100+处修改)
```cpp
// 需要修改：
- ros::init() → rclcpp::init()
- ros::NodeHandle → rclcpp::Node
- nh.param<>() → node->declare_parameter() + get_parameter()
- ros::Publisher → node->create_publisher()
- ros::Subscriber → node->create_subscription()
- ros::Time::now() → node->now()
- ros::spin() → rclcpp::spin()
- 回调函数签名更新
```

#### 3. multi_session.cpp
```cpp
// 需要修改：
- ros::init()
- ros::NodeHandle 
- nh.param<>()
- ros::spinOnce()
```

#### 4. online_relocalization.cpp
```cpp
// 需要修改：
- ros::init()
- ros::spin()
```

#### 5. object_update.cpp
```cpp
// 需要修改：
- ros::init()
```

#### 6. preprocess.cpp
```cpp
// 可能需要修改：
- 消息类型引用
- 时间戳处理
```

## 编译状态

当前编译失败原因：
- 源文件中仍有 ROS1 API 调用（nh.param等）
- 需要将这些调用转换为 ROS2 API

## 建议的完成步骤

### 方案1: 手动逐文件迁移（推荐用于学习）
1. 从 `pose_estimator.cpp` 开始，将构造函数改为接受 `rclcpp::Node::SharedPtr`
2. 修改 `laserMapping.cpp` main 函数
3. 修改其他 cpp 文件
4. 逐个编译测试

### 方案2: 使用自动化工具
使用社区工具如：
- `ros2-migration-tools`
- 或参考 [ROS2 Migration Guide](https://docs.ros.org/en/jazzy/How-To-Guides/Migrating-from-ROS1.html)

### 方案3: 参考已迁移的项目
搜索 GitHub 上类似的 SLAM 项目的 ROS2 版本作为参考。

## ROS API 转换参考

### NodeHandle & 参数
```cpp
// ROS1
ros::NodeHandle nh;
nh.param<std::string>("topic", topic_name, "/default");

// ROS2
auto node = std::make_shared<rclcpp::Node>("node_name");
node->declare_parameter("topic", "/default");
topic_name = node->get_parameter("topic").as_string();
```

### Publisher
```cpp
// ROS1
ros::Publisher pub = nh.advertise<sensor_msgs::PointCloud2>("/topic", 100);

// ROS2
auto pub = node->create_publisher<sensor_msgs::msg::PointCloud2>("/topic", 100);
```

### Subscriber
```cpp
// ROS1
ros::Subscriber sub = nh.subscribe("/topic", 100, callback);
void callback(const sensor_msgs::PointCloud2::ConstPtr& msg) {}

// ROS2
auto sub = node->create_subscription<sensor_msgs::msg::PointCloud2>(
    "/topic", 100, callback);
void callback(const sensor_msgs::msg::PointCloud2::SharedPtr msg) {}
```

### Time
```cpp
// ROS1
ros::Time::now()

// ROS2
node->now()
// 或
rclcpp::Clock().now()
```

### Spin
```cpp
// ROS1
ros::spin();
ros::spinOnce();

// ROS2
rclcpp::spin(node);
rclcpp::spin_some(node);
```

## 文件清单

### 已修改文件
- package.xml
- CMakeLists.txt
- include/common_lib.h
- include/ros2_compat.h (新增)
- src/preprocess.h
- msg/CloudInfo.msg (重命名)
- srv/SaveMap.srv (重命名)
- srv/SavePose.srv (重命名)
- launch/mapping_hap_livox.launch.py (新增)

### 待修改文件
- include/online-relo/pose_estimator.cpp (~752行)
- src/laserMapping.cpp (~2584行)
- src/multi_session.cpp
- src/online_relocalization.cpp  
- src/object_update.cpp

## 测试建议

完成迁移后，建议进行以下测试：
1. 编译测试: `colcon build --packages-select fast_lio_sam`
2. 话题检查: `ros2 topic list`
3. 参数检查: `ros2 param list`
4. 运行测试: `ros2 launch fast_lio_sam mapping_hap_livox.launch.py`
5. 功能测试: 使用rosbag数据进行SLAM测试

## 注意事项

1. **Livox驱动**: 需要使用 `livox_ros_driver2` 而不是 ROS1 的 `livox_ros_driver`
2. **darknet_ros**: ROS2 版本可能不可用，已暂时注释相关代码
3. **GTSAM**: 使用 ROS2 Jazzy 提供的版本 (4.2.0)
4. **Python环境**: 确保使用系统Python或正确配置的conda环境
5. **消息兼容性**: ROS2 消息字段名必须是 snake_case

## 联系与支持

如遇到问题，可参考：
- [ROS2 官方文档](https://docs.ros.org/en/jazzy/)
- [ROS Answers](https://answers.ros.org/)
- GitHub Issues

---
生成时间: 2026年2月5日
