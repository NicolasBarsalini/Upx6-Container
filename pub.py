import zenoh
import json
import time

json_data = {"temperature": 38, "humidity": 20, "fanSpeed": 100, "lightStatus": False}

json_dumps = json.dumps(json_data)

if __name__ == "__main__":
    session = zenoh.open(zenoh.Config())
    key = 'demo/example/zenoh_sub'
    pub = session.declare_publisher(key)
    while True:
        buf = f"{json_dumps}"
        print(f"Putting Data ('{key}': '{buf}')...")
        pub.put(buf)
        time.sleep(1)
