import time

def poll_status(api_client, build_id, poll_interval, max_wait):
    start_time = time.time()
    while True:
        status_resp = api_client.query_build_status(build_id)
        status = status_resp["status"]
        if status in ["success", "failed"]:
            return status
        if time.time() - start_time > max_wait:
            return "timeout"
        time.sleep(poll_interval)
