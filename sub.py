import zenoh, time

def listener(sample):
    print(f"Received {sample.kind} ('{sample.key_expr}': '{sample.payload.to_string()}')")
    
if __name__ == "__main__":
    session = zenoh.open(zenoh.Config())
    sub = session.declare_subscriber('demo/example/zenoh_pub', listener)
    time.sleep(60)