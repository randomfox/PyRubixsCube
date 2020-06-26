#!/bin/python3

import pygame
from pygame.locals import *

from OpenGL.GL import *

#from OpenGl.GLU import *
import random

from OpenGL.GLU import *

from constants import Constants

# to sramble white on top facing green facing
#colors = {
#    'blue': '#DDA0DD',
#    'orange': '#EE82EE',
#    'yellow': '#8B008B',
#    'green': '#FF00FF',
#    'red': '#DA70D6',
#    'white': '#BA55D3',
#}
colors = (
    (1, 1, 0), # Back Yellow
    (1, 0, 0), # Left Red
    (1, 1, 1), # Face White
    (1, 0.5, 0), # Right Orange
    (0, 1, 0), # Up Green
    (0, 0, 1), # Down Blue
)

vertices = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1),
)

surfaces = (
    (0,1,2,3),
    (3,2,7,6),
    (6,7,5,4),
    (4,5,1,0),
    (1,5,7,2),
    (4,0,3,6),
)

def draw_Cube(vertices):
    glBegin(GL_QUADS)
    x = 0
    for surface in surfaces:
        glColor3fv(colors[x])
        for vertex in surface:
            glVertex3fv(vertices[vertex])
        x += 1
    glEnd()

def main():
    # Setup
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    glEnable(GL_DEPTH_TEST)
    # Pre-inishilize variables so I don't get a referenced before assignment error
    x_move = 0
    y_move = 0
    z_move = 0
    roll = 0


    gluPerspective(45, (display[0]/display[1]), 0.1, 50)
    # Move back
    glTranslatef(0, 0, -5)
    #glRotatef(90, 1, 0, 0)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_KP4:
                    x_move = 0.3
                if event.key == pygame.K_KP6:
                    x_move = -0.3

                if event.key == pygame.K_KP8:
                    y_move = -0.3
                if event.key == pygame.K_KP2:
                    y_move = 0.3

                if event.key == pygame.K_w:
                    z_move = 0.3
                if event.key == pygame.K_s:
                    z_move = -0.3

                if event.key == pygame.K_KP7:
                    roll = 0.3
                if event.key == pygame.K_KP9:
                    roll = -0.3

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_KP4 or event.key == pygame.K_KP6:
                    x_move = 0

                if event.key == pygame.K_KP8 or event.key == pygame.K_KP2:
                    y_move = 0

                if event.key == pygame.K_w or event.key == pygame.K_s:
                    z_move = 0

                if event.key ==pygame.K_KP7 or event.key == pygame.K_KP9:
                    roll = 0

        glRotatef(1, y_move, x_move, roll)
        x = glGetDoublev(GL_MODELVIEW_MATRIX)

        camera_x = x[3][0]
        camera_y = x[3][1]
        camera_z = x[3][2]
        glTranslatef(0, 0, z_move)

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        draw_Cube(vertices)

        pygame.display.flip()

if __name__ == '__main__':
    main()
    pygame.quit()
    quit()
