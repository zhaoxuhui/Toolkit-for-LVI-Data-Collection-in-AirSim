from matplotlib import pyplot as plt


def readCamTimestamp(file_path):
    fin = open(file_path, "r")
    timestamps = []

    line = fin.readline().strip()

    while line:
        ts = float(line)/1e9
        timestamps.append(ts)

        line = fin.readline().strip()
    fin.close()
    return timestamps

def readGTTimestamp(file_path):
    fin = open(file_path, "r")
    timestamps = []

    line = fin.readline().strip()
    line = fin.readline().strip()

    while line:
        ts = float(line.split(",")[0])/1e9
        timestamps.append(ts)

        line = fin.readline().strip()
    fin.close()
    return timestamps

def readIMUTimestamp(file_path):
    fin = open(file_path, "r")
    timestamps = []

    line = fin.readline().strip()
    line = fin.readline().strip()

    while line:
        ts = float(line.split(",")[0])/1e9
        timestamps.append(ts)

        line = fin.readline().strip()
    fin.close()
    return timestamps

def readLidarTimestamp(file_path):
    fin = open(file_path, "r")
    timestamps = []

    line = fin.readline().strip()

    while line:
        ts = float(line)/1e9
        timestamps.append(ts)

        line = fin.readline().strip()
    fin.close()
    return timestamps


cam_timestamp_path = "./vehicle-drone/data-cam/timestamps.txt"
gt_timestamp_path = "./vehicle-drone/data-gt/pose_gt.txt"
imu_timestamp_path = "./vehicle-drone/data-imu/IMU.csv"
lidar_timestamp_path = "./vehicle-drone/data-lidar/timestamps.txt"

cam_ts = readCamTimestamp(cam_timestamp_path)
gt_ts = readGTTimestamp(gt_timestamp_path)
imu_ts = readIMUTimestamp(imu_timestamp_path)
lidar_ts = readLidarTimestamp(lidar_timestamp_path)

cam_fps = len(cam_ts)/(cam_ts[-1] - cam_ts[0])
gt_fps = len(gt_ts)/(gt_ts[-1] - gt_ts[0])
imu_fps = len(imu_ts)/(imu_ts[-1] - imu_ts[0])
lidar_fps = len(lidar_ts)/(lidar_ts[-1] - lidar_ts[0])

print((cam_ts[-1] - cam_ts[0])/1e9)
print("stereo camera fps:", cam_fps)
print("groundtruth fps:", gt_fps)
print("imu fps:", imu_fps)
print("lidar fps:", lidar_fps)

cam_index = []
for i in range(len(cam_ts)):
    cam_index.append(1)

gt_index = []
for i in range(len(gt_ts)):
    gt_index.append(2)

imu_index = []
for i in range(len(imu_ts)):
    imu_index.append(3)

lidar_index = []
for i in range(len(lidar_ts)):
    lidar_index.append(4)

plt.scatter(cam_ts, cam_index, label='Camera')
plt.scatter(gt_ts, gt_index, label='Ground Truth')
plt.scatter(imu_ts, imu_index, label='IMU')
plt.scatter(lidar_ts, lidar_index, label='LiDAR')
plt.legend()
plt.show()