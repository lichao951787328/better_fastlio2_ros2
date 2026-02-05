#include "multi-session/Incremental_mapping.hpp"

std::string sessions_dir;
std::string central_sess_name;
std::string query_sess_name;
std::string save_directory;

int iteration;  // >= 4

bool keyFrameSort(const std::pair<int, KeyFrame>& frame1, const std::pair<int, KeyFrame>& frame2){
    return frame1.first < frame2.first;
}

int main(int argc, char** argv){
    rclcpp::init(argc, argv);
    auto node = rclcpp::Node::make_shared("multi_session");

    node->declare_parameter("multi_session/sessions_dir", " ");
    node->declare_parameter("multi_session/central_sess_name", " ");
    node->declare_parameter("multi_session/query_sess_name", " ");
    node->declare_parameter("multi_session/save_directory", " ");
    node->declare_parameter("multi_session/iteration", 5);
    
    sessions_dir = node->get_parameter("multi_session/sessions_dir").as_string();
    central_sess_name = node->get_parameter("multi_session/central_sess_name").as_string();
    query_sess_name = node->get_parameter("multi_session/query_sess_name").as_string();
    save_directory = node->get_parameter("multi_session/save_directory").as_string();
    iteration = node->get_parameter("multi_session/iteration").as_int();

    std::cout << ("\033[1;32m----> multi-session starts.\033[0m");
    MultiSession::IncreMapping multi_session(sessions_dir, central_sess_name, query_sess_name, save_directory);

    // pcl::PointCloud<PointType>::Ptr cloud(new pcl::PointCloud<PointType>);
    // pcl::PointCloud<PointTypePose>::Ptr pose(new pcl::PointCloud<PointTypePose>());
    // std::string pose_name = "/home/fyx/fastlio2/src/sessions/0102/aft_tansformation2.pcd";
    // pcl::io::loadPCDFile(pose_name, *pose);
    // int i = 0;
    // for(auto& it : multi_session.sessions_.at(multi_session.source_sess_idx).cloudKeyFrames){
    //     *cloud += *transformPointCloud(it.all_cloud, &pose->points[i]);
    //     i++;
    // }
    // pcl::io::savePCDFile("/home/fyx/fastlio2/src/sessions/0102/map.pcd", *cloud);

    std::cout << ("\033[1;32m----> pose-graph optimization.\033[0m");
    multi_session.run(iteration);  
    
    std::cout << ("\033[1;32m----> publish cloud.\033[0m");
    std::sort(multi_session.reloKeyFrames.begin(), multi_session.reloKeyFrames.end(), keyFrameSort);
    int it = multi_session.reloKeyFrames.size();
    int i = 0;
    rclcpp::Rate rate(0.5);
    while((rclcpp::ok()) && (i < it)){
        rclcpp::spin_some(node);
        publishCloud(multi_session.pubCentralGlobalMap, multi_session.centralMap_, multi_session.publishTimeStamp, "camera_init");
        publishCloud(multi_session.pubCentralTrajectory, multi_session.traj_central, multi_session.publishTimeStamp, "camera_init");
        publishCloud(multi_session.pubRegisteredTrajectory, multi_session.traj_regis, multi_session.publishTimeStamp, "camera_init");
        multi_session.visualizeLoopClosure();
        publishCloud(multi_session.pubReloCloud, multi_session.reloKeyFrames[i].second.all_cloud, multi_session.publishTimeStamp, "camera_init");
        std::cout << "relo name(Idx): " << multi_session.reloKeyFrames[i].first << " target  name(Idx): " << multi_session.reloKeyFrames[i].second.reloTargetIdx
                            << " score: " << multi_session.reloKeyFrames[i].second.reloScore << std::endl; 
        i ++;
        rate.sleep();
    }
    return 0;
}