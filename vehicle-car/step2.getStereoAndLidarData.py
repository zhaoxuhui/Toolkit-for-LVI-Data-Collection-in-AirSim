import airsim
import os
import numpy as np

def readGT(file_path):
    fin = open(file_path, "r")

    timestamps = []
    positions = []
    orientations = []
    poses = []

    line = fin.readline().strip()
    line = fin.readline().strip()

    while line:
        parts = line.split(",")

        ts = parts[0]
        pos_x = float(parts[1])
        pos_y = float(parts[2])
        pos_z = float(parts[3])

        quat_x = float(parts[4])
        quat_y = float(parts[5])
        quat_z = float(parts[6])
        quat_w = float(parts[7])

        cur_pos = airsim.Vector3r(pos_x, pos_y, pos_z)
        cur_ori = airsim.Quaternionr(quat_x, quat_y, quat_z, quat_w)

        timestamps.append(ts)
        positions.append(cur_pos)
        orientations.append(cur_ori)
        poses.append(airsim.Pose(cur_pos, cur_ori))

        line = fin.readline().strip()

    fin.close()
    return timestamps, positions, orientations, poses

def saveData(out_path, pose_gt, timestamps):
    fout = open(out_path, "w")
    print("Saving ground truth poses.")
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

def isDirExist(path='output'):
    if not os.path.exists(path):
        os.makedirs(path)
        return False
    else:
        return True

if __name__ == '__main__':
    # parameters for proper data collection
    gt_pose_path = "./data-gt/pose_gt.txt"
    stereo_out_dir = "./data-cam/"
    lidar_out_dir = "./data-lidar/"
    stereo_interval = 5
    lidar_interval = 10

    isDirExist(stereo_out_dir)
    isDirExist(lidar_out_dir)

    # step1. load gt trajectory
    print("loading gt poses ...")
    timestamps, positions, orientations, poses = readGT(gt_pose_path)
    print("successfully loaded "+str(len(poses))+ " gt poses in total.")
    
    # step2. link to airsim simulator
    client = airsim.VehicleClient()
    client.confirmConnection()

    stereo_images = []
    stereo_timestamps = []
    lidar_points = []
    lidar_timestamps = []

    airsim.wait_key('Press any key to start stereo and lidar collection')
    print("Start to record stereo data ...")

    # step3. start to collect data in airsim
    for x in range(len(poses)):
        # step3.1 set the vehicle pose
        client.simSetVehiclePose(airsim.Pose(positions[x], orientations[x]), True)

        # step3.2 collect stereo data if the current time is wanted
        if x % stereo_interval == 0:
            responses = client.simGetImages([
                airsim.ImageRequest("front_left", airsim.ImageType.Scene),
                airsim.ImageRequest("front_right", airsim.ImageType.Scene)])
            stereo_images.append(responses)
            stereo_timestamps.append(timestamps[x])
            print("progress", x+1, "/", len(poses))
        
        # step3.3 collect lidar data if the current time is wanted
        if x % lidar_interval == 0:
            lidar_data = client.getLidarData()
            lidar_points.append(lidar_data.point_cloud)
            lidar_timestamps.append(timestamps[x])

    # step4 output collected data
    # step4.1 stereo images
    fout_stereo = open(stereo_out_dir + "/timestamps.txt", "w")
    isDirExist(stereo_out_dir + "/cam_left/")
    isDirExist(stereo_out_dir + "/cam_right/")
    for i in range(len(stereo_images)):
        image_left = stereo_images[i][0]
        image_right = stereo_images[i][1]

        airsim.write_file(os.path.normpath(stereo_out_dir + "/cam_left/" + stereo_timestamps[i] + '.png'), image_left.image_data_uint8)
        airsim.write_file(os.path.normpath(stereo_out_dir + "/cam_right/" + stereo_timestamps[i] + '.png'), image_right.image_data_uint8)
        fout_stereo.write(stereo_timestamps[i] + "\n")

        print("stereo images: ", i+1, "/", len(stereo_images))
    fout_stereo.close()

    # step4.2 lidar points
    fout_lidar = open(lidar_out_dir+"/timestamps.txt", "w")
    for i in range(len(lidar_points)):
        np.save(lidar_out_dir + lidar_timestamps[i], lidar_points[i])
        fout_lidar.write(lidar_timestamps[i] + "\n")

        print("lidar points: ", i+1, "/", len(lidar_points))
    fout_lidar.close()