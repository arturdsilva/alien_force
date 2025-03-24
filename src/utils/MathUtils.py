import numpy as np


class MathUtils:
    def rotate_point(self, point, center, angle):
        x, y = point
        cx, cy = center
        x -= cx
        y -= cy
        x_new = x * np.cos(angle) - y * np.sin(angle)
        y_new = x * np.sin(angle) + y * np.cos(angle)
        return x_new + cx, y_new + cy
