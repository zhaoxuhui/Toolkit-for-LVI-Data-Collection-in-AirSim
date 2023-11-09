import time
from pynput.keyboard import Key, Listener

def on_press(key):
    timestamp = time.time()
    with open(out_path, 'a') as f:
        # f.write('{0} pressed at {1}\n'.format(key))
        f.write(str(key)+","+"press,"+str(timestamp-start_time)+"\n")

def on_release(key):
    timestamp = time.time()
    with open(out_path, 'a') as f:
        # f.write('{0} release at {1}\n'.format(key, timestamp-start_time))
        f.write(str(key)+","+"release,"+str(timestamp-start_time)+"\n")
    if key == Key.esc:
        # Stop listener
        return False

if __name__ == '__main__':
    out_path = "./drive-nh.txt"

    start_time = time.time()

    # Collect events until released
    with Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()