import sys
import pprint
from jsonconfig import *

class Settings(JsonConfig):
    def __init__(self):
        self.verbose = False
        self.cube_default_colors = {
            'blue': '#BA55D3',
            'orange': '#EE82EE',
            'yellow': '#8B008B',
            'green': '#FF00FF',
            'red': '#DA70D6',
            'white': '#DDA0DD'
        }

        # cube settings
        self.cube_draw_cubies = True
        self.cube_draw_sphere = True
        self.cube_draw_lines = False
        self.cube_padding = 0.1
        self.cube_line_width = 4.0
        self.cube_angular_drag = 0.7
        self.cube_scale_drag = 4.2
        self.cube_min_scale = 3
        self.cube_max_scale = 1.5
        self.cube_inner_color = '#000000'
        self.cube_sphere_color = '#000000'
        self.cube_color_group = 'material'
        self.cube_colors = {}
        self.cube_color_mapping = {
            'front': 'green',
            'back': 'blue',
            'left': 'orange',
            'right': 'red',
            'up': 'white',
            'down': 'yellow',
        }
        self.cube_face_rotation_tween_time = 0.5
        self.cube_face_rotation_ease_type = 'ease_cosine'
        self.rotate_y_before_x_initially = True
        self.cube_initial_rotation_x = -30
        self.cube_initial_rotation_y = 35

        self.cube_auto_rot_x_enabled = False
        self.cube_auto_rot_x_begin = -30
        self.cube_auto_rot_x_end = 30
        self.cube_auto_rot_x_time = 8
        self.cube_auto_rot_x_jump_start = 0.5
        self.cube_auto_rot_x_ease_type = 'ease_cosine'

        self.cube_auto_rot_y_enabled = False
        self.cube_auto_rot_y_begin = 135
        self.cube_auto_rot_y_end = -135
        self.cube_auto_rot_y_time = 16
        self.cube_auto_rot_y_jump_start = 0.5
        self.cube_auto_rot_y_ease_type = 'ease_cosine'

        # fps settings
        self.fps_show = False
        self.fps_update_interval = 30

        # mouse settings
        self.mouse_sensitivity = 5

        self.image_resources = {'rounded-sticker': 'res/sticker-rounded.jpg',
                                'squared-sticker': 'res/sticker-squared.jpg',
                                'no-sticker': 'res/stickerless.jpg',
                                'checker2x2': 'res/checker-2x2.jpg',
                                'checker8x8': 'res/checker-8x8.jpg'}

        self.texture_mapping_enabled = True
        self.texture_mapping_active_texture = 'rounded-sticker'

        # window settings
        self.window_caption = 'NxNxN Rubiks Cube Solver'
        self.window_position = (0, 0)
        self.window_size = (600, 600)
        self.window_background_color = '#343D46'

    def load(self, filename):
        print('Loading settings file: ', filename)
        config = self.load_json(filename)
        self.assign(config)

    def print(self, config):
        print('# Json')
        pretty_printer = pprint.PrettyPrinter(indent=2, width=42, compact=True)
        pretty_printer.pprint(config)

    def assign(self, config):
        prop_root = 'settings'
        prop_cube = 'cube'
        prop_fps = 'fps'
        prop_mouse = 'mouse'
        prop_resources = 'resources'
        prop_texture_mapping = 'texture_mapping'
        prop_window = 'window'

        if not config or prop_root not in config:
            return
        settings = config[prop_root]

        try:
            if prop_cube in settings:
                cube = settings[prop_cube]
                self.cube_draw_cubies = self.get_value(cube, ['draw_cubies'], self.cube_draw_cubies)
                self.cube_draw_sphere = self.get_value(cube, ['draw_sphere'], self.cube_draw_sphere)
                self.cube_draw_lines = self.get_value(cube, ['draw_lines'], self.cube_draw_lines)
                self.cube_padding = self.get_value(cube, ['padding'], self.cube_padding)
                self.cube_line_width = self.get_value(cube, ['line_width'], self.cube_line_width)
                self.cube_inner_color = self.get_value(cube, ['inner_color'], self.cube_inner_color)
                self.cube_sphere_color = self.get_value(cube, ['sphere_color'], self.cube_sphere_color)
                self.cube_angular_drag = self.get_value(cube, ['angular_drag'], self.cube_angular_drag)
                self.cube_scale_drag = self.get_value(cube, ['scale_drag'], self.cube_scale_drag)
                self.cube_min_scale = self.get_value(cube['scaling'], ['min'], self.cube_min_scale)
                self.cube_max_scale = self.get_value(cube['scaling'], ['max'], self.cube_max_scale)
                self.rotate_y_before_x_initially = self.get_value(cube['initial_rotation'], ['rotate_y_before_x'], self.rotate_y_before_x_initially)
                self.cube_initial_rotation_x = self.get_value(cube['initial_rotation'], ['x_angle'], self.cube_initial_rotation_x)
                self.cube_initial_rotation_y = self.get_value(cube, ['y_angle'], self.cube_initial_rotation_y)
                self.cube_face_rotation_tween_time = self.get_value(cube['tween'], ['face_rotation_tween_time'], self.cube_face_rotation_tween_time)
                self.cube_face_rotation_ease_type = self.get_value(cube['tween'], ['face_rotation_ease_type'], self.cube_face_rotation_ease_type)
                self.cube_colors = self.get_value(cube, ['colors'], self.cube_colors)
                self.cube_color_mapping = self.get_value(cube, ['color_mapping'], self.cube_color_mapping)
                self.cube_color_group = self.get_value(cube, ['color_group'], self.cube_color_group)

                cube_auto_rotation_x = cube['auto_rotation']['x_axis']
                self.cube_auto_rot_x_enabled = self.get_value(cube_auto_rotation_x, ['enabled'], self.cube_auto_rot_x_enabled)
                self.cube_auto_rot_x_begin = self.get_value(cube_auto_rotation_x, ['begin_angle'], self.cube_auto_rot_x_begin)
                self.cube_auto_rot_x_end = self.get_value(cube_auto_rotation_x, ['end_angle'], self.cube_auto_rot_x_end)
                self.cube_auto_rot_x_time = self.get_value(cube_auto_rotation_x, ['time'], self.cube_auto_rot_x_time)
                self.cube_auto_rot_x_jump_start = self.get_value(cube_auto_rotation_x, ['jump_start'], self.cube_auto_rot_x_jump_start)
                self.cube_auto_rot_x_ease_type = self.get_value(cube_auto_rotation_x, ['ease_type'], self.cube_auto_rot_x_ease_type)

                cube_auto_rotation_y = cube['auto_rotation']['y_axis']
                self.cube_auto_rot_y_enabled = self.get_value(cube_auto_rotation_y, ['enabled'], self.cube_auto_rot_y_enabled)
                self.cube_auto_rot_y_begin = self.get_value(cube_auto_rotation_y, ['begin_angle'], self.cube_auto_rot_y_begin)
                self.cube_auto_rot_y_end = self.get_value(cube_auto_rotation_y, ['end_angle'], self.cube_auto_rot_y_end)
                self.cube_auto_rot_y_time = self.get_value(cube_auto_rotation_y, ['time'], self.cube_auto_rot_y_time)
                self.cube_auto_rot_y_jump_start = self.get_value(cube_auto_rotation_y, ['jump_start'], self.cube_auto_rot_y_jump_start)
                self.cube_auto_rot_y_ease_type = self.get_value(cube_auto_rotation_y, ['ease_type'], self.cube_auto_rot_y_ease_type)

            if prop_fps in settings:
                fps = settings[prop_fps]
                self.fps_update_interval = self.get_value(fps, ['update_interval'], self.fps_update_interval)
                self.fps_show = self.get_value(fps, ['show'], self.fps_show)

            if prop_mouse in settings:
                self.mouse_sensitivity = self.get_value(settings[prop_mouse], ['sensitivity'], self.mouse_sensitivity)

            if prop_resources in settings:
                resources = settings[prop_resources]
                self.image_resources = self.get_value(settings[prop_resources], ['images'], self.image_resources)

            if prop_texture_mapping in settings:
                texture_mapping = settings[prop_texture_mapping]
                self.texture_mapping_enabled = self.get_value(texture_mapping, ['enabled'], self.texture_mapping_enabled)
                self.texture_mapping_active_texture = self.get_value(texture_mapping, ['active_texture'], self.texture_mapping_active_texture)

            if prop_window in settings:
                window = settings[prop_window]
                self.window_caption = self.get_value(window, ['caption'], self.window_caption)
                px = self.get_value(window['position'], ['x'], self.window_position[0])
                py = self.get_value(window['position'], ['y'], self.window_position[1])
                self.window_position = (px, py)
                ww = self.get_value(window['size'], ['width'], self.window_size[0])
                wh = self.get_value(window['size'], ['height'], self.window_size[1])
                self.window_size = (ww, wh)
                self.window_background_color = self.get_value(window, ['background_color'], self.window_background_color)
        except:
            print('An error occurred while trying to retrieve the settings.')
            print(sys.exc_info())

    def get_value(self, property, keys, default=None):
        t = property
        for key in keys:
            if key in t:
                t = t[key]
            else:
                t = default
                break
        if self.verbose: print(f'{keys[-1]} : {t} :: {type(t)}')
        return t
