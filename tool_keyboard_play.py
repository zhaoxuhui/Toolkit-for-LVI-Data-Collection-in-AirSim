import time
import keyboard

def readData(file_path):
    keys = []
    actions = []
    timestamps = []
    fin = open(file_path, "r")
    line = fin.readline().strip()
    while line:
        parts = line.split(",")
        keys.append(parts[0])
        actions.append(parts[1])
        timestamps.append(float(parts[2]))

        line = fin.readline().strip()
    return keys, actions, timestamps

if __name__ == '__main__':
    file_path = './drive-nh.txt'

    start_time = time.time()

    keys, actions, timestamps = readData(file_path)

    print("Keyboard recording is loaded.")

    rst = input("Start to play?[y]/n\n")
    if rst == 'y' or rst == 'Y' or rst == 'YES' or rst == 'Yes' or rst == 'yes' or rst == '':
        
        print("Playing will be start in 5 seconds.")
        time.sleep(5)

        print("Playing start!")

        for i in range(1, len(keys)):
            last_ts = timestamps[i-1]
            cur_ts = timestamps[i]
            
            # actions
            if actions[i] == 'press':
                keyboard.press(keys[i].split(".")[1])
            elif actions[i] == 'release':
                keyboard.release(keys[i].split(".")[1])

            # 持续时间
            time.sleep(cur_ts - last_ts)