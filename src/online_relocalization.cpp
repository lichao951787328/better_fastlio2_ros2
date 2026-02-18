#include "online-relo/pose_estimator.h"

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = rclcpp::Node::make_shared("OR_LIO");
    // ros::console::set_logger_level(ROSCONSOLE_DEFAULT_NAME, ros::console::levels::Debug); 
    std::cout << ("\033[1;32m----> Online Relocalization Started.\033[0m");

    auto lol = std::make_shared<pose_estimator>(node);
    std::thread opt_thread(&pose_estimator::run, lol.get());
    std::thread pub_thread(&pose_estimator::publishThread, lol.get());
    
    rclcpp::spin(node);

    if (opt_thread.joinable()) {
        opt_thread.join();
    }
    if (pub_thread.joinable()) {
        pub_thread.join();
    }

    return 0;
}