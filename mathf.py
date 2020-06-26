import math

class Mathf:
    DEG_TO_RAD = math.pi * 2 / 360
    RAD_TO_DEG = 1 / (math.pi * 2 / 360)

    @staticmethod
    def clamp01(value):
        if value < 0: return 0
        if value > 1: return 1
        return value

    def clamp(value, min, max):
        if value < min: return min
        if value > max: return max
        return value

    def lerp(a, b, t):
        return a + (b - a) * Mathf.clamp01(t)
