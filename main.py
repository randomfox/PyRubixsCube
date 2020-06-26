import argparse
import colorsys # ?

from app import App
from colormanager import ColorManager
from settings import Settings

parser = argparse.ArgumentParser()
parser.add_argument('--settings', help='Path to settings file', required=False)
parser.add_argument('--colors', help='Path to colors file', required=False)
parser.add_argument('--glinfo', help='Show OpenGL info', required=False, action='store_true')
parser.add_argument('--verbose', '-v', help='Show random info', required=False, action='store_true')
parser.add_argument('--size', help='Size of Rubiks cube (Getting Implanted)', default=3, type=int)
parser.add_argument('--draw-sphere', help='Show sphere in the center of the cube', default=False, action='store_true')
args = parser.parse_args()

# Parse colors
color_manager = ColorManager()
colors_file = 'cfg/colors.json'
if args.colors:
    color_manager.load(args.colors)

# Parse settings
settings = Settings()
settings_file = 'cfg/settings.json'
if args.settings:
    settings.load(args.settings)
if args.verbose:
    settings.verbose = args.verbose
size = 3
if args.size:
    size = args.size
    settings.cube_size = size

settings.cube_draw_sphere = args.draw_sphere
#display_glinfo = args.glinfo
app = App(settings, color_manager, args.glinfo, size, args.verbose)
if __name__ == '__main__':
    app.run()
