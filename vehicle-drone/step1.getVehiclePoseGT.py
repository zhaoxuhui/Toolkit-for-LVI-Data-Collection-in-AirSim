# coding=utf-8
import airsim
import time
import os

def saveData(out_path, pose_gt, timestamps):
    fout = open(out_path, "w")
    print("Saving ground truth poses.")

    fout.write("#timestamp(ns), pos_x, pos_y, pos_z, quat_x, quat_y, quat_z, quat_w\n")
    for i in range(len(pose_gt)):
        cur_pose = pose_gt[i]
        cur_quat_w = cur_pose.orientation.w_val
        cur_quat_x = cur_pose.orientation.x_val
        cur_quat_y = cur_pose.orientation.y_val
        cur_quat_z = cur_pose.orientation.z_val

        cur_pos_x = cur_pose.position.x_val
        cur_pos_y = cur_pose.position.y_val
        cur_pos_z = cur_pose.position.z_val

        fout.write(str(timestamps[i])+","+
                   str(cur_pos_x)+","+str(cur_pos_y)+","+str(cur_pos_z)+","+
                   str(cur_quat_x)+","+str(cur_quat_y)+","+str(cur_quat_z)+","+str(cur_quat_w)+"\n")
    fout.close()

    print("Saved all gt poses:", out_path)

def isDirExist(path='output'):
    if not os.path.exists(path):
        os.makedirs(path)
        return False
    else:
        return True

if __name__ == '__main__':
    gt_poses = []
    timestamps = []

    try:
        out_dir = "./data-gt/"
        isDirExist(out_dir)

        # 连接到AirSim模拟器
        client = airsim.MultirotorClient()
        client.confirmConnection()

        print("Recording Pose GT data ...\nPress Ctrl + C to stop.")
        
        cur_timestamp = 0
        last_timestamp = 0
        
        # 循环读取数据
        while True:
            cur_pose = client.simGetVehiclePose()
            cur_timestamp = client.getMultirotorState().timestamp

            if cur_timestamp != last_timestamp:
                gt_poses.append(cur_pose)
                timestamps.append(cur_timestamp)
                last_timestamp = cur_timestamp
    
    except KeyboardInterrupt:
        saveData(out_dir+"/pose_gt.txt", gt_poses, timestamps)