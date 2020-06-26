# Using Robert Penner's easing functions
# http://robertpenner.com/easing

from enum import Enum
import math

class TweenEaseType(Enum):
    LINEAR = 0
    EASE_COSINE = 1
    EASE_IN_SINE = 2
    EASE_OUT_SINE = 3
    EASE_IN_OUT_SINE = 4
    EASE_IN_QUAD = 5
    EASE_OUT_QUAD = 6
    EASE_IN_OUT_QUAD = 7
    EASE_IN_CUBIC = 8
    EASE_OUT_CUBIC = 9
    EASE_IN_OUT_CUBIC = 10
    EASE_IN_QUART = 11
    EASE_OUT_QUART = 12
    EASE_IN_OUT_QUART = 13
    EASE_IN_QUINT = 14
    EASE_OUT_QUINT = 15
    EASE_IN_OUT_QUINT = 16

class Tween:
    def __init__(self):
        self.begin = 0
        self.end = 0
        self.duration = 0
        self.elapsed = 0

        self.current = 0
        self.delta = 0
        self.done = True

        self.ease_type = TweenEaseType.EASE_COSINE
        self.ease_foo = self.ease_cosine

        self.repeat = False
        self.count = 0

    def tween(self, begin, end, duration, ease_type=TweenEaseType.EASE_COSINE, repeat=False, count=0, jump_start01=0):
        self.begin = begin
        self.end = end
        self.duration = duration
        self.current = begin
        self.elapsed = 0
        self.done = False
        self.ease_foo = self.get_ease_func(ease_type)
        self.repeat = repeat
        self.count = count
        self.temp = None

        if jump_start01:
            self.init_jumpstart(jump_start01)

    def init_jumpstart(self, jump_start):
        if jump_start < 0:
            jump_start = 0
        elif jump_start > 1:
            jump_start = 1
        if jump_start == 0:
            return

        # calculate start point
        delta = self.end - self.begin
        point = self.begin + delta*jump_start
        # store begin and duration
        self.temp = (self.begin, self.duration)
        self.begin = point
        self.current = point
        self.duration = self.duration*(1.0 - jump_start)

    def get_ease_func(self, type):
        if type == TweenEaseType.EASE_COSINE: return self.ease_cosine
        if type == TweenEaseType.EASE_IN_SINE: return self.ease_in_sine
        if type == TweenEaseType.EASE_OUT_SINE: return self.ease_out_sine
        if type == TweenEaseType.EASE_IN_OUT_SINE: return self.ease_in_out_sine
        if type == TweenEaseType.EASE_IN_QUAD: return self.ease_in_quad
        if type == TweenEaseType.EASE_OUT_QUAD: return self.ease_out_quad
        if type == TweenEaseType.EASE_IN_OUT_QUAD: return self.ease_in_out_quad
        if type == TweenEaseType.EASE_IN_CUBIC: return self.ease_in_cubic
        if type == TweenEaseType.EASE_OUT_CUBIC: return self.ease_out_cubic
        if type == TweenEaseType.EASE_IN_OUT_CUBIC: return self.ease_in_out_cubic
        if type == TweenEaseType.EASE_IN_QUART: return self.ease_in_quart
        if type == TweenEaseType.EASE_OUT_QUART: return self.ease_out_quart
        if type == TweenEaseType.EASE_IN_OUT_QUART: return self.ease_in_out_quart
        if type == TweenEaseType.EASE_IN_QUINT: return self.ease_in_quint
        if type == TweenEaseType.EASE_OUT_QUINT: return self.ease_out_quint
        if type == TweenEaseType.EASE_IN_OUT_QUINT: return self.ease_in_out_quint
        return self.linear

    # I think these functions are rather pointless
    def is_done(self): return self.done
    def get_current(self): return self.current
    def get_delta(self): return self.delta

    def get_midpoint(self):
        return (self.end - self.start) / 2 + self.start

    def update(self, elapsed_time):
        if self.done:
            return

        value = self.elapsed/self.duration
        value = self.ease_foo(self.begin, self.end, value)
        self.delta = value - self.current
        self.current = value

        if self.elapsed >= self.duration: self.done = True

        self.elapsed = min(self.elapsed + elapsed_time, self.duration)

        if self.done and self.repeat: self.update_repetition()

    def update_repetition(self):
        skip_count = self.temp != None
        if self.temp:
            # restore original begin and duration after reaching the end for the first time
            self.begin = self.temp[0]
            self.duration = self.temp[1]
            self.temp = None
        self.begin, self.end = self.end, self.begin
        self.elapsed = 0

        self.done = False

        if skip_count or self.count == -1: return

        self.count -= 1
        if self.count < 0: self.done = True

    def ease_in_sine(self, begin, end, value):
        change = end - begin
        return -change*math.cos(value*(math.pi/2)) + change + begin

    def ease_out_sine(self, begin, end, value):
        change = end - begin
        return change * math.sin(value * (math.pi/2)) + begin

    def ease_in_out_sine(self, begin, end, value):
        change = end - begin
        return change * math.sin(value * (math.pi/2)) + begin

    def ease_in_quad(self, begin, end, value):
        change = end - begin
        return change * value * value + begin

    def ease_out_quad(self, begin, end, value):
        change = end - begin
        return -change * value * (value - 2) + begin

    def ease_in_out_quad(self, begin, end, value):
        change = end - begin
        value /= 0.5
        if value < 1:
            return change * 0.5 * value * value + begin
        value -= 1
        return -change * 0.5 * (value * (value - 2) - 1) + begin

    def ease_in_cubic(self, begin, end, value):
        change = end - begin
        return change * value * value * value + begin

    def ease_out_cubic(self, begin, end, value):
        change = end - begin
        value -= 1
        return change * (value * value * value + 1) + begin

    def ease_in_out_cubic(self, begin, end, value):
        change = end - begin
        value /= 0.5
        if value < 1:
            return change * 0.5 * value * value * value + begin
        value -= 2
        return change * 0.5 * (value * value * value + 2) + begin

    def ease_in_quart(self, begin, end, value):
        change = end - begin
        return change * value * value * value * value + begin

    def ease_out_quart(self, begin, end, value):
        change = end - begin
        value -= 1
        return -change * (value * value * value * value - 1) + begin

    def ease_in_out_quart(self, begin, end, value):
        change = end - begin
        value /= 0.5
        if value < 1:
            return change / 2 * value * value * value * value + begin
        value -= 2
        return -change / 2 * (value * value * value * value - 2) + begin

    def ease_in_quint(self, begin, end, value):
        change = end - begin
        return change * value * value * value * value * value + begin

    def ease_out_quint(self, begin, end, value):
        change = end - begin
        value -= 1
        return change * (value * value * value * value * value + 1) + begin

    def ease_in_out_quint(self, begin, end, value):
        change = end - begin
        value /= 0.5
        if value < 1:
            return change / 2 * value * value * value * value * value + begin
        value -= 2
        return change / 2 * (value * value * value * value * value + 2) + begin

    def ease_cosine(self, begin, end, value):
        t = (1 - math.cos(value * math.pi)) / 2
        return begin * (1 - t) + end * t

    def linear(self, begin, end, value):
        return (end - begin) * value + begin

    @staticmethod
    def get_ease_type_by_name(name):
        if name =='ease_cosine': return TweenEaseType.EASE_COSINE
        if name =='ease_in_sine': return TweenEaseType.EASE_IN_SINE
        if name =='ease_out_sine': return TweenEaseType.EASE_OUT_SINE
        if name =='ease_in_out_sine': return TweenEaseType.EASE_IN_OUT_SINE
        if name =='ease_in_quad': return TweenEaseType.EASE_IN_QUAD
        if name =='ease_out_quad': return TweenEaseType.EASE_OUT_QUAD
        if name =='ease_in_out_quad': return TweenEaseType.EASE_IN_OUT_QUAD
        if name =='ease_in_cubic': return TweenEaseType.EASE_IN_CUBIC
        if name =='ease_out_cubic': return TweenEaseType.EASE_OUT_CUBIC
        if name =='ease_in_out_cubic': return TweenEaseType.EASE_IN_OUT_CUBIC
        if name =='ease_in_quart': return TweenEaseType.EASE_IN_QUART
        if name =='ease_out_quart': return TweenEaseType.EASE_OUT_QUART
        if name =='ease_in_out_quart': return TweenEaseType.EASE_IN_OUT_QUART
        if name =='ease_in_quint': return TweenEaseType.EASE_IN_QUINT
        if name =='ease_out_quint': return TweenEaseType.EASE_OUT_QUINT
        if name =='ease_in_out_quint': return TweenEaseType.EASE_IN_OUT_QUINT
        return TweenEaseType.LINEAR
