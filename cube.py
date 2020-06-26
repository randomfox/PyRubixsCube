""" cube
Original PyCube written by Michael King

Based and modified from original version found at:
http://stackoverflow.com/questions/30745703/rotating-a-cube-using-quaternions-in-pyopengl
"""
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import math
import numpy as np
from queue import Queue

from enums import FaceRotation
from geometry import Geometry
from helpers import LittleHelpers
from mathf import Mathf
from quat import *
from tween import *

class State(Enum):
    IDLE = 0
    TWEENING = 1

class Cube:
    def __init__(self, settings, face_rotation_ease_type, sticker_texture_id, size=3):
        default_color = (0, 0, 0)
        self.padding = settings.cube_padding
        self.draw_cubies = settings.cube_draw_cubies
        self.draw_sphere = settings.cube_draw_sphere
        self.draw_lines = settings.cube_draw_lines
        self.line_width = settings.cube_line_width
        self.inner_color = LittleHelpers.convert_hex_color_to_floats(settings.cube_inner_color, default_color)
        self.sphere_color = LittleHelpers.convert_hex_color_to_floats(settings.cube_sphere_color, default_color)
        self.angular_drag = settings.cube_angular_drag
        self.scale_drag = settings.cube_scale_drag
        self.min_scale = settings.cube_min_scale/size
        self.max_scale = settings.cube_max_scale

        self.size = size

        self.rot_x = 0
        self.rot_y = 0
        self.accum = (1, 0, 0, 0)

        self.scale = 1/(self.size/3)
        self.scale_speed = 0
        self.sphere_radius = 3
        self.sphere_slices = 16
        self.sphere_stacks = 16

        self.face_rotation_tween_time = settings.cube_face_rotation_tween_time
        self.face_rotation_ease_type = face_rotation_ease_type
        self.texture_mapping_enabled = settings.texture_mapping_enabled
        self.sticker_texture_id = sticker_texture_id

        self.geometry = Geometry(self.size)
        self.face_colors = (
            (0, 154/255, 74/255), # Front: Green
            (1, 86/255, 35/255), # Left: Orange
            (0, 75/255, 171/255), # Back: Blue
            (190/255, 15/255, 56/255), # Right: Red
            (1, 1, 1), # Up: White
            (1, 210/255, 44/255), # Down: Yellow
        )
        self.reset()

        rx = settings.cube_initial_rotation_x * Mathf.DEG_TO_RAD
        ry = settings.cube_initial_rotation_y * Mathf.DEG_TO_RAD
        self.apply_rotation(rx, ry, settings.rotate_y_before_x_initially)

        # auto-rotation
        repeat = True
        repetion_count = -1

        if settings.cube_auto_rot_x_enabled:
            begin = settings.cube_auto_rot_x_begin
            end = settings.cube_auto_rot_x_end
            jump_start = settings.cube_auto_rot_x_jump_start
            ease = Tween.get_ease_type_by_name(settings.cube_auto_rot_x_ease_type)
            self.auto_rot_x = Tween()
            self.auto_rot_x.tween(begin, end, time, ease, repeat, repetition_count, jump_start)
        else:
            self.auto_rot_x = False

        if settings.cube_auto_rot_y_enabled:
            begin = settings.cube_auto_rot_y_begin
            end = settings.cube_auto_rot_y_end
            time = settings.cube_auto_rot_y_time
            jump_start = settings.cube_auto_rot_y_jump_start
            ease = Tween.get_ease_type_by_name(settings.cube_auto_rot_y_ease_type)
            self.auto_rot_y = Tween()
            self.auto_rot_y.tween(begin, end, time, ease, repeat, repetition_count, jump_start)
        else:
            self.auto_rot_y = False

    def reset(self):
        self.geometry = Geometry(self.size)
        self.geometry.add_padding(self.padding)
        self.queued_face_rotations = Queue(0)
        self.tween = Tween()
        self.state = State.IDLE
        self.current_face_rotation = None

    def apply_rotation(self, x, y, rotate_y_before_x=False):
        qx = normalize(axisangle_to_q((1, 0, 0), x))
        qy = normalize(axisangle_to_q((0, 1, 0), y))
        if rotate_y_before_x:
            self.accum = q_mult(self.accum, qy)
            self.accum = q_mult(self.accum, qx)
        else:
            self.accum = q_mult(self.accum, qx)
            self.accum = q_mult(self.accum, qy)

    def update(self, elapsed_time):
        self.rot_x -= abs(self.rot_x) * self.angular_drag * elapsed_time * np.sign(self.rot_x)
        self.rot_y -= abs(self.rot_y) * self.angular_drag * elapsed_time * np.sign(self.rot_y)

        qx = normalize(axisangle_to_q((1, 0, 0), self.rot_x))
        qy = normalize(axisangle_to_q((0, 1, 0), self.rot_y))

        self.accum = q_mult(self.accum, qx)
        self.accum = q_mult(self.accum, qy)

        self.scale_speed -= abs(self.scale_speed) * self.scale_drag * elapsed_time * np.sign(self.scale_speed)
        self.scale += self.scale_speed
        if self.scale < self.min_scale:
            self.scale = self.min_scale
            self.scale_speed = 0
        if self.scale > self.max_scale:
            self.scale = self.max_scale
            self.scale_speed = 0

        self.update_queue()
        self.update_tween(elapsed_time)
        self.update_face_tweening()
        if self.auto_rot_x: self.auto_rot_x.update(elapsed_time)
        if self.auto_rot_y: self.auto_rot_y.update(elapsed_time)

    def render(self):
        # glPushMatrix()
        glLoadMatrixf(q_to_mat4(self.accum))
        glScalef(self.scale, self.scale, self.scale)

        if self.auto_rot_x:
            rot_x = self.auto_rot_x.get_current()
            glRotatef(rot_x, 1, 0, 0)
        if self.auto_rot_y:
            rot_y = self.auto_rot_y.get_current()
            glRotatef(rot_y, 0, 1, 0)

        if self.draw_sphere: self.render_sphere()
        if self.draw_cubies:
            if self.texture_mapping_enabled:
                self.render_cubies_with_textures()
            else:
                self.render_cubies()
        if self.draw_lines: self.render_lines()
        # glPopMatrix()

    def add_rotate_x(self, value): self.rot_x += value
    def add_rotate_y(self, value): self.rot_y += value
    def add_scale(self, value):
        self.scale_speed += value

    def reset_rotation(self):
        self.rot_x = 0
        self.rot_y = 0
        self.accum = (1, 0, 0, 0)

    def reset_scale(self): self.scale = 1

    def stop_rotation(self):
        self.rot_x = 0
        self.rot_y = 0

    def append_face_rotation(self, face_rotation):
        if type(face_rotation) == FaceRotation:
            self.queued_face_rotations.put(face_rotation)

    def scramble(self, face_rotations):
        theta = math.pi / 2
        for face in face_rotations:
            self.rotate_face(face, theta)

    def map_colors(self, front_color, back_color, left_color, right_color, up_color, down_color):
        self.face_colors = (front_color, left_color, back_color, right_color, up_color, down_color)

    def update_queue(self):
        if self.state == State.TWEENING or self.queued_face_rotations.empty(): return
        self.current_face_rotation = self.queued_face_rotations.get_nowait()
        self.state = State.TWEENING
        self.tween.tween(0, math.pi/2, self.face_rotation_tween_time, self.face_rotation_ease_type)

    def update_tween(self, elapsed_time):
        if self.state != State.TWEENING: return

        if self.tween.is_done():
            self.state = State.IDLE
            self.current_face_rotation = None
        else:
            self.tween.update(elapsed_time)

    def update_face_tweening(self):
        theta = self.tween.get_delta()
        self.rotate_face(self.current_face_rotation, theta)

    def rotate_face(self, face, theta):
        if (face == FaceRotation.FRONT_CW or
                face == FaceRotation.BACK_CCW or
                face == FaceRotation.LEFT_CCW or
                face == FaceRotation.RIGHT_CW or
                face == FaceRotation.UP_CW or
                face == FaceRotation.DOWN_CCW):
            theta *= -1
        if face == FaceRotation.FRONT_CW or face == FaceRotation.FRONT_CCW:
            self.rotate_front_face(theta)
        if face == FaceRotation.BACK_CW or face == FaceRotation.BACK_CCW:
            self.rotate_back_face(theta)
        if face == FaceRotation.LEFT_CW or face == FaceRotation.LEFT_CCW:
            self.rotate_left_face(theta)
        if face == FaceRotation.RIGHT_CW or face == FaceRotation.RIGHT_CCW:
            self.rotate_right_face(theta)
        if face == FaceRotation.UP_CW or face == FaceRotation.UP_CCW:
            self.rotate_up_face(theta)
        if face == FaceRotation.DOWN_CW or face == FaceRotation.DOWN_CCW:
            self.rotate_down_face(theta)

    def rotate_front_face(self, theta):
        for i in range(8):
            self.geometry.center_pieces[0][i] = z_rot(self.geometry.center_pieces[0][i], theta)
        for axis in self.geometry.edge_pieces:
            for piece in axis:
                flag = True
                for vertex in piece:
                    if vertex[2] < 0:
                        flag = False
                        break
                if flag:
                    for i in range(8):
                        piece[i] = z_rot(piece[i], theta)
        for piece in self.geometry.corner_pieces:
            flag = True
            for vertex in piece:
                if vertex[2] < 0:
                    flag = False
                    break
            if flag:
                for i in range(8):
                    piece[i] = z_rot(piece[i], theta)

    def rotate_back_face(self, theta):
        for i in range(8):
            self.geometry.center_pieces[2][i] = z_rot(self.geometry.center_pieces[2][i], theat)
        for axis in self.geometry.edge_pieces:
            for piece in axis:
                flag = True
                for vertex in piece:
                    if vertex[2] > 0:
                        flag = False
                        break
                if flag:
                    for i in range(8):
                        piece[i] = z_rot(piece[i], theta)
        for piece in self.geometry.corner_pieces:
            flag = True
            for vertex in piece:
                if vertex[0] > 0:
                    flag = False
                    break
            if flag:
                for i in range(8):
                    piece[i] = z_rot(piece[i], theat)

    def rotate_left_face(self, theta):
        for i in range(8):
            self.geometry.center_pieces[1][i] = x_rot(self.geometry.center_pieces[1][i], theta)
        for axis in self.geometry.edge_pieces:
            for piece in axis:
                flag = True
                for vertex in piece:
                    if vertex[0] > 0:
                        flag = False
                        break
                if flag:
                    for i in range(8):
                        piece[i] = x_rot(piece[i], theta)
        for piece in self.geometry.corner_pieces:
            flag = True
            for vertex in piece:
                if vertex[0] > 0:
                    flag = False
                    break
            if flag:
                for i in range(8):
                    piece[i] = x_rot(piece[i], theta)

    def rotate_right_face(self, theta):
        for i in range(8):
            self.geometry.center_pieces[3][i] = x_rot(self.geometry.center_pieces[3][i], theta)
        for axis in self.geometry.edge_pieces:
            for piece in axis:
                flag = True
                for vertex in piece:
                    if vertex[0] < 0:
                        flag = False
                        break
                if flag:
                    for i in range(8):
                        piece[i] = x_rot(piece[i], theta)
        for piece in self.geometry.corner_pieces:
            flag = True
            for vertex in piece:
                if vertex[0] < 0:
                    flag = False
            if flag:
                for i in range(8):
                    piece[i] = x_rot(piece[i], theta)

    def rotate_up_face(self, theta):
        for i in range(8):
            self.geometry.center_pieces[4][i] = y_rot(self.geometry.center_pieces[4][i], theta)
        for axis in self.geometry.edge_pieces:
            for piece in axis:
                flag = True
                for vertex in piece:
                    if vertex[1] < 0:
                        flag = False
                        break
                if flag:
                    for i in range(8):
                        piece[i] = y_rot(piece[i], theta)
        for piece in self.geometry.corner_pieces:
            flag = True
            for vertex in piece:
                if vertex[1] < 0:
                    flag = False
                    break
            if flag:
                for i in range(8):
                    piece[i] = y_rot(piece[i], theta)

    def rotate_down_face(self, theta):
        for i in range(8):
            self.geometry.center_pieces[5][i] = y_rot(self.geometry.center_pieces[5][i], theta)
        for axis in self.geometry.edge_pieces:
            for piece in axis:
                flag = True
                for vertex in piece:
                    if vertex[1] > 0:
                        flag = False
                        break
                if flag:
                    for i in range(8):
                        piece[i] = y_rot(piece[i], theta)
        for piece in self.geometry.corner_pieces:
            flag = True
            for vertex in piece:
                if vertex[1] > 0:
                    flag = False
                    break
            if flag:
                for i in range(8):
                    piece[i] = y_rot(piece[i], theta)

    def render_sphere(self):
        glColor3f(self.sphere_color[0], self.sphere_color[1], self.sphere_color[2])
        glutSolidSphere(self.sphere_radius, self.sphere_slices, self.sphere_stacks)

    def render_axes(self):
        glLineWidth(1)
        glBegin(GL_LINES)
        for color, axis in zip(self.geometry.axis_colors, self.geometry.axes):
            glColor3f(color[0], color[1], color[2])
            for point in axis:
                p = self.geometry.axis_verts[point]
                glVertex3f(p[0], p[1], p[2])
        glEnd()

    def render_lines(self):
        glLineWidth(self.line_width)
        glColor3f(0, 0, 0)
        glBegin(GL_LINES)
        for axis in self.geometry.edge_pieces:
            for piece in axis:
                for edge in self.geometry.cube_edges:
                    for vertex in edge:
                        v = piece[vertex]
                        glVertex3f(v[0], v[1], v[2])
        for piece in self.geometry.center_pieces:
            for edge in self.geometry.cube_edges:
                for vertex in edge:
                    v = piece[vertex]
                    glVertex3f(v[0], v[1], v[2])
        glEnd()

    def render_cubies(self):
        inner_color = self.inner_color

        glBegin(GL_QUADS)

        # render center pieces
        i = 0
        for color, surface in zip(self.face_colors, self.geometry.cube_surfaces):
            glColor3f(color[0], color[1], color[2])
            for vertex in surface:
                v = self.geometry.center_pieces[i][vertex]
                glVertex3f(v[0], v[1], v[2])
            j = 0
            for piece in self.geometry.center_pieces:
                glColor3f(inner_color[0], inner_color[1], inner_color[2])
                for vertex in surface:
                    v = self.geometry.center_pieces[j][vertex]
                    glVertex3f(v[0], v[1], v[2])
                j += 1
            i += 1

        # render edge pieces
        for color, surface, face in zip(self.face_colors, self.geometry.cube_surfaces, self.geometry.edges):
            glColor3f(color[0], color[1], color[2])
            for piece in face:
                for vertex in surface:
                    p = self.geometry.edge_pieces[piece[0]][piece[1]][vertex]
                    glVertex3f(p[0], p[1], p[2])
        glColor3f(inner_color[0], inner_color[1], inner_color[2])
        for i in range(len(self.geometry.edge_black_pat)):
            for face in self.geometry.edge_black_pat[i]:
                for piece in self.geometry.edge_pieces[i]:
                    for vertex in self.geometry.cube_surfaces[face]:
                        v = piece[vertex]
                        glVertex3f(v[0], v[1], v[2])

        # render corner pieces
        for i in range(len(self.geometry.corner_black_pat)):
            for face in self.geometry.corner_color_pat[i]:
                color = self.face_colors[face]
                glColor3f(color[0], color[1], color[2])
                for vertex in self.geometry.cube_surfaces[face]:
                    v = self.geometry.corner_pieces[i][vertex]
                    glVertex3f(v[0], v[1], v[2])
        glColor3f(inner_color[0], inner_color[1], inner_color[2])
        for i in range(len(self.geometry.corner_black_pat)):
            for face in self.geometry.corner_black_pat[i]:
                for vertex in self.geometry.cube_surfaces[face]:
                    v = self.geometry.corner_pieces[i][vertex]
                    glVertex3f(v[0], v[1], v[2])
        glEnd()

    def render_cubies_with_textures(self):
        tex_coords = self.geometry.tex_coords
        inner_color = self.inner_color

        # render outer faces with an applied texture
        glBindTexture(GL_TEXTURE_2D, self.sticker_texture_id)
        glBegin(GL_QUADS)

        # render center pieces
        i = 0
        for color, surface in zip(self.face_colors, self.geometry.cube_surfaces):
            glColor3f(color[0], color[1], color[2])
            ti = 0
            for vertex in surface:
                v = self.geometry.center_pieces[i][vertex]
                glVertex3f(v[0], v[1], v[2])
                glTexCoord2f(tex_coords[ti][0], tex_coords[ti][1])
                ti += 1
            i += 1

        # render edge pieces
        for color, surface, face in zip(self.face_colors, self.geometry.cube_surfaces, self.geometry.edges):
            glColor3f(color[0], color[1], color[2])
            for piece in face:
                ti = 0
                for vertex in surface:
                    p = self.geometry.edge_pieces[piece[0]][piece[1]][vertex]
                    glVertex3f(p[0], p[1], p[2])
                    glTexCoord2f(tex_coords[ti][0], tex_coords[ti][1])
                    ti += 1

        # render corner pieces
        for i in range(len(self.geometry.corner_color_pat)):
            for face in self.geometry.corner_color_pat[i]:
                color = self.face_colors[face]
                glColor3f(color[0], color[1], color[2])
                ti = 0
                for vertex in self.geometry.cube_surfaces[face]:
                    v = self.geometry.corner_pieces[i][vertex]
                    glVertex3f(v[0], v[1], v[2])
                    glTexCoord2f(tex_coords[ti][0], tex_coords[ti][1])
                    ti += 1
        glEnd()

        # render inner faces without texture using only the inner color
        glBindTexture(GL_TEXTURE_2D, 0)
        glBegin(GL_QUADS)

        # render center pieces
        i = 0
        for color, surface in zip(self.face_colors, self.geometry.cube_surfaces):
            j = 0
            for piece in self.geometry.center_pieces:
                glColor3f(inner_color[0], inner_color[1], inner_color[2])
                for vertex in surface:
                    v = self.geometry.center_pieces[j][vertex]
                    glVertex3f(v[0], v[1], v[2])
                j += 1
            i += 1

        # render edge pieces
        glColor3f(inner_color[0], inner_color[1], inner_color[2])
        for i in range(len(self.geometry.edge_black_pat)):
            for face in self.geometry.edge_black_pat[i]:
                for piece in self.geometry.edge_pieces[i]:
                    for vertex in self.geometry.cube_surfaces[face]:
                        v = piece[vertex]
                        glVertex3f(v[0], v[1], v[2])

        # render corner pieces
        glColor3f(inner_color[0], inner_color[1], inner_color[2])
        for i in range(len(self.geometry.corner_black_pat)):
            for face in self.geometry.corner_black_pat[i]:
                for vertex in self.geometry.cube_surfaces[face]:
                    v = self.geometry.corner_pieces[i][vertex]
                    glVertex3f(v[0], v[1], v[2])
        glEnd()
