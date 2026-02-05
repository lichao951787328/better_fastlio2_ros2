#!/bin/bash

# 修复IMU_Processing.hpp中剩余的toSec()调用
sed -i '
275s/if (tail->header\.stamp\.sec + ->header\.stamp\.nanosec \* 1e-9 </if ((tail->header.stamp.sec + tail->header.stamp.nanosec * 1e-9) </
290s/if (head->header\.stamp\.sec + ->header\.stamp\.nanosec \* 1e-9 </if ((head->header.stamp.sec + head->header.stamp.nanosec * 1e-9) </
292s/dt = tail->header\.stamp\.sec + ->header\.stamp\.nanosec \* 1e-9 -/dt = (tail->header.stamp.sec + tail->header.stamp.nanosec * 1e-9) -/
296s/dt = tail->header\.stamp\.sec + ->header\.stamp\.nanosec \* 1e-9 - head->header\.stamp\.sec + ->header\.stamp\.nanosec \* 1e-9;/dt = (tail->header.stamp.sec + tail->header.stamp.nanosec * 1e-9) - (head->header.stamp.sec + head->header.stamp.nanosec * 1e-9);/
319s/double &&offs_t = tail->header\.stamp\.sec + ->header\.stamp\.nanosec \* 1e-9 - pcl_beg_time;/double offs_t = (tail->header.stamp.sec + tail->header.stamp.nanosec * 1e-9) - pcl_beg_time;/
' IMU_Processing.hpp

echo "Fixed toSec() calls"
