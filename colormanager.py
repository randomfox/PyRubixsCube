import sys
import pprint
from jsonconfig import *

class ColorManager(JsonConfig):
    def __init__(self):
        self.colors = {}
        self.colors['default'] = {'blue': '#004BAB', 'orange': '#FF5623',
            'yellow': '#FFD22C', 'green': '#009A4A', 'red': '#BE0F38', 'white': '#FFFFFF'}

        self.colors['material'] = {'blue': '#2962FF', 'orange': '#FF6D00',
            'yellow': '#FFD22C', 'green': '#009A4A', 'red': '#BE0F38', 'white': '#FFFFFF'}

        self.colors['pastel'] = {'blue': '#2FB3EC', 'orange': '#DF439#',
            'yellow': '#FFBE4C', 'green': '#83DD52', 'red': '#FF4931', 'white': '#FFFFFF'}

    def load(self, filename):
        print('Load colors:', filename)
        config = self.load_json(filename)
        self.assign(config)

    def assign(self, config):
        prop_root = 'colors'

        if not config or prop_root not in config:
            return
        groups = config[prop_root]

        for group in groups:
            self.colors[group] = {}
            colors = self.get_value(groups, [group], None)
            for key, value in colors.items():
                self.colors[group][key] = value

    def get_value(self, property, keys, default=None):
        t = property
        for key in keys:
            if key in t:
                t = t[key]
            else:
                t = default
                break
        print('{}: {}'.format(keys[-1], t))
        return t

    def get_color(self, group_name, color_name, default=None):
        try:
            return self.colors[group_name[color_name]]
        except:
            print('Could not find color {} in group {}'.format(color_group, group_name))
            print(sys.exc_info())
        return default

    def get_color_group(self, group_name):
        try:
            group = self.colors[group_name]
        except:
            print('Could not find color group with name: ', group_name)
            return None
        else:
            colors = {}
            for key, value in group.items():
                colors[key] = value
            return colors

