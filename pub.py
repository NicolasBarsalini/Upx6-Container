import zenoh
import json
import time
import random

json_data = {
    "temperature": random.randint(0, 50), 
    "humidity": random.randint(30, 100), 
    "fanSpeed": random.randint(0, 100), 
    "lightStatus": random.choice([True, False])
    }

# json_data = {"status" : "completed", "message" : "Process finished!"}

if __name__ == "__main__":
    session = zenoh.open(zenoh.Config())
    key = 'demo/example/zenoh_sub'
    pub = session.declare_publisher(key)

    while True:
        json_data = {
            "temperature": random.randint(0, 50),
            "humidity": random.randint(30, 100),
            "fanSpeed": random.randint(0, 100),
            "lightStatus": random.choice([True, False])
        }

        json_dumps = json.dumps(json_data)

        buf = f"{json_dumps}"
        print(f"Putting Data ('{key}': '{buf}')...")
        pub.put(buf)
        time.sleep(3)
