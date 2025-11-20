import datetime

LOG_FILE = "traffic_log.txt"

def log_event(message):
    """
    Ghi sự kiện nhận dạng vào log file.
    """
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.datetime.now():%Y-%m-%d %H:%M:%S}] {message}\n")

def alert_user(message):
    """
    Hiển thị cảnh báo realtime.
    """
    print(f"⚠️ {message}")
