# coding=utf-8
import airsim
import os


def parseIMU(imu_data):
    angular_velocity = imu_data.angular_velocity
    linear_acceleration = imu_data.linear_acceleration
    orientation = imu_data.orientation
    time_stamp = imu_data.time_stamp

    # 参考EuRoC IMU数据格式
    data_item = [str(time_stamp),
                 str(angular_velocity.x_val),
                 str(angular_velocity.y_val),
                 str(angular_velocity.z_val),
                 str(linear_acceleration.x_val),
                 str(linear_acceleration.y_val),
                 str(linear_acceleration.z_val)]
    return data_item

def saveData(out_path, measurements):
    print("Saving recorded data ...")
    fout = open(out_path, "w")

    fout.write("# timestamp(ns),"
               " gyro_x(rad/s), gyro_y(rad/s), gyro_z(rad/s),"
               " accel_x(m/s^2), accel_y(m/s^2), accel_z(m/s^2)\n")

    for i in range(len(measurements)):
        data_item = parseIMU(measurements[i])
        fout.write(data_item[0] + "," +
                       data_item[1] + "," +
                       data_item[2] + "," +
                       data_item[3] + "," +
                       data_item[4] + "," +
                       data_item[5] + "," +
                       data_item[6] + "\n")
    
    fout.close()
    print("Saved record file:", out_path)

def isDirExist(path='output'):
    if not os.path.exists(path):
        os.makedirs(path)
        return False
    else:
        return True


if __name__ == '__main__':
    raw_measurements = []
    out_dir = "./data-imu/"
    isDirExist(out_dir)

    try:
        # 连接到AirSim模拟器
        client = airsim.CarClient()
        client.confirmConnection()
        
        print("Recording IMU data ...\nPress Ctrl + C to stop.")

        last_timestamp = 0

        # 循环读取数据
        while True:
            # 通过getImuData()函数即可获得IMU观测
            # 返回结果由角速度、线加速度、朝向(四元数表示)、时间戳(纳秒)构成
            imu_data = client.getImuData()
            cur_time_stamp = imu_data.time_stamp

            if cur_time_stamp != last_timestamp:
                raw_measurements.append(imu_data)
                last_timestamp = cur_time_stamp
    except KeyboardInterrupt:
        saveData(out_dir+"IMU.csv", raw_measurements)