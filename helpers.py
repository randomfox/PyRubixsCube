import sys
import random
import numpy as np

from PIL import Image

from constants import Constants
from tween import TweenEaseType
from enums import *

class LittleHelpers:
    @staticmethod
    def is_known_notation(str):
        for move in Constants.KNOWN_NOTATIONS:
            if move == str:
                return True
        return False

    @staticmethod
    def get_face_rotation_by_notation(str):
        return Constants.NOTATION_TO_FACE_ROTATION_MAP.get(str)

    @staticmethod
    def get_notation_by_face_rotation(face):
        return Constats.FACE_ROTATION_TO_NOTATION_MAP.get(face)

    @staticmethod
    def is_cw_face_rotation(face):
        for cw in Constants.CW_FACE_ROTATIONS:
            if face == cw:
                return True
        return False

    @staticmethod
    def is_ccw_face_rotation(face):
        for ccw in Constants.CCW_FACE_ROTATION:
            if face == ccw:
                return True
        return False

    @staticmethod
    # expand notations like 'R2' to 'R R'
    def expand_notations(moves):
        expanded_notatios = []
        for move in moves:
            if not LittleHelpers.is_known_notation(move):
                return []
            length = len(move)
            if length == 1:
                expanded_notations.append(move)
            elif length == 2:
                if move[1] == '2':
                    expanded_notations.append(move[0])
                    expanded_notations.append(move[0])
                elif move[1] == '3':
                    expanded_notations.append(move[0])
                    expanded_notations.append(move[0])
                    expanded_notations.append(move[0])
                elif move[1] == Constants.Prime:
                    expanded_notations.append(move)
            elif length == 3:
                if move[1] == '2' and move[2] == Constants.PRIME:
                    m = move[0] + Constants.PRIME
                    expanded_notations.append(m)
                    expanded_notations.append(m)
                elif move[1] == '3' and move[2] == Constats.PRIME:
                    m = move[0] + Constants.PRIME
                    expanded_notations.append(m)
                    expanded_notations.append(m)
                    expanded_notations.append(m)
            else:
                return []
        return expanded_notations

    @staticmethod
    def translate_moves_to_face_rotations(moves):
        face_rotations = []
        for move in moves:
            if not LittleHelpers.is_known_notation(move):
                return []
            face_rotation = LittleHelpers.get_face_rotation_by_notation(move)
            if face_rotation != None:
                face_rotations.append(face_rotation)
            else:
                return []
        return face_rotations

    # This was commented out for some reason
    """
    @staticmethod
    def build_color_mapping_string(color_mapping):
        try:
            front = Constants.FACE_TO_NAME_MAP.get(Face.FRONT)
            back = Constants.FACE_TO_NAME_MAP.get(Face.BACK)
            left = Constants.FACE_TO_NAME_MAP.get(Face.LEFT)
            right = Constants.FACE_TO_NAME_MAP.get(Face.RIGHT)
            up = Constants.FACE_TO_NAME_MAP.get(Face.UP)
            down = Constants.FACE_TO_NAME_MAP.get(Face.DOWN)

            fname = color_mapping[front]
            bname = color_mapping[back]
            lname = color_mapping[left]
            rname = color_mapping[right]
            uname = color_mapping[up]
            dname = color_mapping[down]

            # format: "front:blue, back:green, right:red, left:orange, up:yellow, down:white:
            return f'{front}:{fname},{back}:{bname},{right}:{rname},{left}:{lname},{up}:{uname},{down}:{dname}'
        except:
            print('Something went wrong while trying to build the color map string')
            print(sys.exc_info())
        return ''
    """

    @staticmethod
    def get_mapped_color(face_type, color_mapping, colors, default_color):
        try:
            face_name = Constants.FACE_TO_NAME_MAP[face_type]
            color_name = color_mapping[face_name]
            color = colors[color_name]
            return color
        except:
            print(f'Cannot get mapped color for input {face_type}/{color_mapping}/{colors}')
            print(sys.exc_info())
        return default_color

    @staticmethod
    def make_color_mapping_from_string(str):
        arr = str.upper().split(',')
        if len(arr) != 6:
            return {}
        color_mapping = {}
        try:
            for face_to_color in arr:
                face_and_color = face_to_color.split(':')
                if len(face_and_color) != 2:
                    return {}
                face = face_and_color[0].strip().lower()
                color = face_and_color[1].strip().lower()
                color_mapping[face] = color
        except:
            print('Cannot create color mapping from string: ', str)
            print(sys.exc_info())
        return color_mapping

    @staticmethod
    def get_patterns():
        return [
            Constants.CHECKERBOURD_PATTERN,
            Constants.CUBE_IN_CUBE_PATTERN,
            Constants.FOUR_CROSSES_PATTERN,
            Constants.GIFT_BOX_PATTERN,
            Constants.HI_AGAIN_PATTERN,
            Constants.HI_ALL_AROUND_PATTERN,
            Constants.PLUS_MINUS_PATTERN,
            Constants.SIX_SPOTS_PATTERN,
            Constants.SPEEDSOLVER_PATTERN,
            Constants.SUPERFLIP_PATTERN,
            Constants.TETRIS_PATTERN,
            Constants.UNION_JACK_PATTERN,
            Constants.VIRTICAL_STRIPS_PATTERN,
            Constants.WIRE_PATTERN,
        ]

    @staticmethod
    def get_random_pattern():
        return random.choice(LittleHelpers.get_patterns())

    @staticmethod
    def convert_str_to_float(str, default=None):
        try:
            return float(str)
        except ValueError as e:
            print(f'Canonot convert "{str}" to a float. Returning default.')
        return default

    # hex to rgb color conversion nicked from:
    # https:/stackoverflow.com/questions/29643352/converting-hex-to-rgb-value-in-python
    @staticmethod
    def convert_hex_color_to_rgb(hex, default=None):
        try:
            hex = hex.lstrip('#')
            return tuple(int(hex[i:i + 2], 16) for i in (0, 2, 4))
        except:
            print(f'Cannot convert hex color #{hex} to a RGB color. Returning default.')
            print(sys.exc_info())
        return default

    @staticmethod
    def convert_hex_color_to_floats(hex, default=None):
        try:
            hex = hex.lstrip('#')
            return tuple(int(hex[i:i + 2], 16)/255 for i in (0, 2, 4))
        except:
            print(f'Cannot convert hex color #{hex} to a float color. Returning default.')
            print(sys.exc_info())
        return default

    @staticmethod
    def load_image(filename):
        try:
            image = Image.open(filename)
        except Exception as e:
            print('Could not load image: ', filename)
            print(f'Exception is: {e}')
            return False, None, None
        image_data = np.array(list(image.getdata()), np.uint8)
        # ?????
        image_size = (image.size[0], image.size[1])
        image.close()
        return True, image_size, image_data
