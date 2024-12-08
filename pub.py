import zenoh
import json
import time

json_data = {"temperature": 50, "humidity": 15, "fanSpeed": 56, "lightStatus": True}

# json_data = {"status" : "completed", "message" : "Process finished!"}

json_dumps = json.dumps(json_data)

if __name__ == "__main__":
    session = zenoh.open(zenoh.Config())
    key = 'demo/example/zenoh_sub'
    pub = session.declare_publisher(key)
    while True:
        buf = f"{json_dumps}"
        print(f"Putting Data ('{key}': '{buf}')...")
        pub.put(buf)
        time.sleep(3)
