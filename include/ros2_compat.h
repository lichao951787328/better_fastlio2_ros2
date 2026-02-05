#ifndef ROS2_COMPAT_H
#define ROS2_COMPAT_H

// ROS2 compatibility layer to minimize code changes
#include <rclcpp/rclcpp.hpp>
#include <memory>

// Helper macros for easier migration
#define ROS_INFO RCLCPP_INFO
#define ROS_WARN RCLCPP_WARN  
#define ROS_ERROR RCLCPP_ERROR
#define ROS_DEBUG RCLCPP_DEBUG

// Helper class to wrap node handle functionality
class NodeHandleWrapper {
public:
    explicit NodeHandleWrapper(std::shared_ptr<rclcpp::Node> node) : node_(node) {}
    
    template<typename T>
    void param(const std::string& name, T& variable, const T& default_value) {
        node_->declare_parameter(name, default_value);
        variable = node_->get_parameter(name).get_value<T>();
    }
    
    template<typename MessageT, typename CallbackT>
    typename rclcpp::Subscription<MessageT>::SharedPtr subscribe(
        const std::string& topic, 
        size_t queue_size, 
        CallbackT&& callback) {
        return node_->create_subscription<MessageT>(topic, queue_size, callback);
    }
    
    template<typename MessageT>
    typename rclcpp::Publisher<MessageT>::SharedPtr advertise(
        const std::string& topic, 
        size_t queue_size) {
        return node_->create_publisher<MessageT>(topic, queue_size);
    }
    
    std::shared_ptr<rclcpp::Node> getNode() { return node_; }
    
private:
    std::shared_ptr<rclcpp::Node> node_;
};

// Helper functions
namespace ros {
    inline rclcpp::Time Time(int sec, int nsec) {
        return rclcpp::Time(sec, nsec);
    }
    
    struct Time {
        static rclcpp::Time now() {
            return rclcpp::Clock().now();
        }
    };
    
    inline bool ok() {
        return rclcpp::ok();
    }
    
    inline void spinOnce() {
        // In ROS2, spinning is handled differently
        // This is a placeholder
    }
    
    inline void spin(std::shared_ptr<rclcpp::Node> node) {
        rclcpp::spin(node);
    }
}

#endif // ROS2_COMPAT_H
