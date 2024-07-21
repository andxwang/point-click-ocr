import numpy as np

def do_boxes_overlap(box1, box2):
    """
    Check if two bounding boxes overlap.
    
    :param box1: Tuple (x1, y1, x2, y2) representing the first bounding box.
    :param box2: Tuple (x1, y1, x2, y2) representing the second bounding box.
    :return: True if the bounding boxes overlap, False otherwise.
    """
    x1_min, y1_min, x1_max, y1_max = box1
    x2_min, y2_min, x2_max, y2_max = box2

    # Check if the bounding boxes overlap
    if (x1_min < x2_max and x1_max > x2_min and
        y1_min < y2_max and y1_max > y2_min):
        return True
    return False
