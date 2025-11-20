import math

def estimate_distance(x1, y1, x2, y2, known_width=0.6, focal_length=700):
    """
    Ước lượng khoảng cách đến biển báo (đơn vị: mét)
    Dựa vào kích thước bounding box và thông số camera giả định.
    - known_width: chiều rộng thực tế trung bình biển báo (m)
    - focal_length: tiêu cự camera (px)
    """
    width_in_frame = x2 - x1
    if width_in_frame <= 0:
        return None
    distance = (known_width * focal_length) / width_in_frame
    return round(distance, 2)
