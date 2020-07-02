'''
    5____________6
    /|          /|
   / |         / |
 1/__________2/  |
 |   |       |   |
 |   |       |   |
 |   4_______|___7
 |  /        |  /
 | /         | /
 0___________3/
'''

class Geometry:
    def __init__(self, size=3):
        self.size = size
        self.init_geomentry()

    def init_geomentry(self, size=1):
        if self.size % 2 == 1:
            # trying to autogen the centers
            # self.center_pieces = [[[[0,0,0] for i in range(8)] for i in range(self.size)] for i in range(6)]
            # Do the centers in this block
            self.center_pieces = [
                # Front 0 Green
                #[[-1, -1, self.size],
                # [-1, 1, self.size],
                # [1, 1, self.size],
                # [1, -1, self.size],
                # [-1, -1, self.size-2],
                # [-1, 1, self.size-2],
                # [1, 1, self.size-2],
                # [1, -1, self.size-2]],
                [[[[i, j, self.size],
                   [i, j+2, self.size],
                   [i+2, j+2, self.size],
                   [i+2, j, self.size],
                   [i, j, self.size-2],
                   [i, j+2, self.size-2],
                   [i+2, j+2, self.size-2],
                   [i+2, j, self.size-2]
                  ] for i in range(-self.size+2, self.size-2, 2)
                ] for j in range(-self.size+2, self.size-2, 2)],

                # Left 1 Orange
                [[[[-self.size, i, j+2],
                   [-self.size, i+2, j+2],
                   [2-self.size, i+2, j+2],
                   [2-self.size, i, j+2],
                   [-self.size, i, j],
                   [-self.size, i+2, j],
                   [2-self.size, i+2, j],
                   [2-self.size, i, j]
                  ] for i in range(-self.size+2, self.size-2, 2)
                 ] for j in range(-self.size+2, self.size-2, 2)],

                 # Back 2 Blue
                 [[[[i, j, 2-self.size],
                    [i, j+2, 2-self.size],
                    [i+2, j+2, 2-self.size],
                    [i+2, j, 2-self.size],
                    [i, j, -self.size],
                    [i, j+2, -self.size],
                    [i+2, j+2, -self.size],
                    [i+2, j, -self.size]
                   ] for i in range(-self.size+2, self.size-2, 2)
                  ] for j in range(-self.size+2, self.size-2, 2)],

                 # Right 3 Red
                 [[[[self.size-2, i, j+2],
                    [self.size-2, i+2, j+2],
                    [self.size, i+2, j+2],
                    [self.size, i, j+2],
                    [self.size-2, i, j],
                    [self.size-2, i+2, j],
                    [self.size, i+2, j],
                    [self.size, i, j]
                   ] for i in range(-self.size+2, self.size-2, 2)
                  ] for j in range(-self.size+2, self.size-2, 2)],

                 # Up 4 White
                 [[[[i, self.size-2, j+2],
                    [i, self.size, j+2],
                    [i+2, self.size, j+2],
                    [i+2, self.size-2, j+2],
                    [i, self.size-2, j],
                    [i, self.size, j],
                    [i+2, self.size, j],
                    [i+2, self.size-2, j]
                   ] for i in range(-self.size+2, self.size-2, 2)
                  ] for j in range(-self.size+2, self.size-2, 2)],

                 # Down 5 Yellow
                 [[[[i, -self.size, j+2],
                    [i, 2-self.size, j+2],
                    [i+2, 2-self.size, j+2],
                    [i+2, -self.size, j+2],
                    [i, -self.size, j],
                    [i, 2-self.size, j],
                    [i+2, 2-self.size, j],
                    [i+2, -self.size, j]
                   ] for i in range(-self.size+2, self.size-2, 2)
                  ] for j in range(-self.size+2, self.size-2, 2)]
            ]

        else:
            self.center_pieces = [[[0,0,0] for i in range(8)] for i in range(6)]

        # in cube.py in the function on line 386(371) is the only place this variable is used
        self.axes = ((0, 1), (2, 3), (4, 5))
        # in cube.py in the function on line 386(3721) is the only place this variable is used
        self.axis_colors = ((1, 0, 0), (0, 1, 0), (0, 0, 1)) # Red, Green, Blue
        # in cube.py in the function on line 386(371) is the only place this variable is used
        self.axis_verts = (
            (-5.5, 0, 0),
            (5.5, 0, 0),
            (0, -5.5, 0),
            (0, 5.5, 0),
            (0, 0, -5.5),
            (0, 0, 5.5)
        )

        # Have to add this yet, need something to generate it for different sizes
        if self.size < 3:
            self.edge_pieces = [[[[0,0,0] for i in range(8)] for j in range(4)] for k in range(3)]
            self.edge_pieces = [[[[[0,0,0] for i in range(8)] for l in range(self.size)] for j in range(4)] for k in range(3)]
        else:
            #for i in range(-self.size, self.size, 2):
            self.edge_pieces = [
                # X
                # 0
                [
                 #[[-1, -self.size, self.size],
                 # [-1, 2-self.size, self.size],
                 # [1, 2-self.size, self.size],
                 # [1, -self.size, self.size],
                 # [-1, -self.size, -2+self.size],
                 # [-1, 2-self.size, -2+self.size],
                 # [1, 2-self.size, -2+self.size],
                 # [1, -self.size, -2+self.size]],
                 #[self.x_zero(i) for i in range(-self.size+2, self.size-2, 2)],
                 [[[i, -self.size, self.size],
                   [i, 2-self.size, self.size],
                   [i+2, 2-self.size, self.size],
                   [i+2, -self.size, self.size],
                   [i, -self.size, self.size-2],
                   [i, 2-self.size, self.size-2],
                   [i+2, 2-self.size, self.size-2],
                   [i+2, -self.size, self.size-2]
                 ] for i in range(-self.size+2, self.size-2, 2)],

                 # 1
                 [[[i, self.size-2, self.size],
                   [i, self.size, self.size],
                   [i+2, self.size, self.size],
                   [i+2, self.size-2, self.size],
                   [i, self.size-2, self.size-2],
                   [i, self.size, self.size-2],
                   [i+2, self.size, self.size-2],
                   [i+2, self.size-2, self.size-2]
                 ] for i in range(-self.size+2, self.size-2, 2)],

                 # 2
                 [[[i, -2+self.size, 2-self.size],
                   [i, self.size, 2-self.size],
                   [i+2, self.size, 2-self.size],
                   [i+2, -2+self.size, 2-self.size],
                   [i, -2+self.size, -self.size],
                   [i, self.size, -self.size],
                   [i+2, self.size, -self.size],
                   [i+2, -2+self.size, -self.size]
                 ] for i in range(-self.size+2, self.size-2, 2)],

                 # 3
                 [[[i, -self.size, 2-self.size],
                   [i, 2-self.size, 2-self.size],
                   [i+2, 2-self.size, 2-self.size],
                   [i+2, -self.size, 2-self.size],
                   [i, -self.size, -self.size],
                   [i, 2-self.size, -self.size],
                   [i+2, 2-self.size, -self.size],
                   [i+2, -self.size, -self.size]
                 ] for i in range(-self.size+2, self.size-2, 2)],
                 ],

                # Y
                # 0
                [[[[-self.size, i, self.size],
                   [-self.size, i+2, self.size],
                   [2-self.size, i+2, self.size],
                   [2-self.size, i, self.size],
                   [-self.size, i, -2+self.size],
                   [-self.size, i+2, -2+self.size],
                   [2-self.size, i+2, -2+self.size],
                   [2-self.size, i, -2+self.size]
                 ] for i in range(-self.size+2, self.size-2, 2)],

                 # 1
                 [[[-self.size, i, 2-self.size],
                   [-self.size, i+2, 2-self.size],
                   [2-self.size, i+2, 2-self.size],
                   [2-self.size, i, 2-self.size],
                   [-self.size, i, -self.size],
                   [-self.size, i+2, -self.size],
                   [2-self.size, i+2, -self.size],
                   [2-self.size, i, -self.size]
                 ] for i in range(-self.size+2, self.size-2, 2)],

                 # 2
                 [[[-2+self.size, i, 2-self.size],
                   [-2+self.size, i+2, 2-self.size],
                   [self.size, i+2, 2-self.size],
                   [self.size, i, 2-self.size],
                   [-2+self.size, i, -self.size],
                   [-2+self.size, i+2, -self.size],
                   [self.size, i+2, -self.size],
                   [self.size, i, -self.size]
                 ] for i in range(-self.size+2, self.size-2, 2)],

                 # 3
                 [[[-2+self.size, i, self.size],
                   [-2+self.size, i+2, self.size],
                   [self.size, i+2, self.size],
                   [self.size, i, self.size],
                   [-2+self.size, i, -2+self.size],
                   [-2+self.size, i+2, -2+self.size],
                   [self.size, i+2, -2+self.size],
                   [self.size, i, -2+self.size]
                 ] for i in range(-self.size+2, self.size-2, 2)]],

                # Z
                # 0
                [[[[-self.size, -self.size, i+2],
                   [-self.size, 2-self.size, i+2],
                   [2-self.size, 2-self.size, i+2],
                   [2-self.size, -self.size, i+2],
                   [-self.size, -self.size, i],
                   [-self.size, 2-self.size, i],
                   [2-self.size, 2-self.size, i],
                   [2-self.size, -self.size, i]
                 ] for i in range(-self.size+2, self.size-2, 2)],

                 # 1
                 [[[-self.size, -2+self.size, i+2],
                   [-self.size, self.size, i+2],
                   [2-self.size, self.size, i+2],
                   [2-self.size, -2+self.size, i+2],
                   [-self.size, -2+self.size, i],
                   [-self.size, self.size, i],
                   [2-self.size, self.size, i],
                   [2-self.size, -2+self.size, i]
                 ] for i in range(-self.size+2, self.size-2, 2)],

                 # 2
                 [[[-2+self.size, -2+self.size, i+2],
                   [-2+self.size, self.size, i+2],
                   [self.size, self.size, i+2],
                   [self.size, -2+self.size, i+2],
                   [-2+self.size, -2+self.size, i],
                   [-2+self.size, self.size, i],
                   [self.size, self.size, i],
                   [self.size, -2+self.size, i]
                 ] for i in range(-self.size+2, self.size-2, 2)],

                 # 3
                 [[[-2+self.size, -self.size, i+2],
                   [-2+self.size, 2-self.size, i+2],
                   [self.size, 2-self.size, i+2],
                   [self.size, -self.size, i+2],
                   [-2+self.size, -self.size, i],
                   [-2+self.size, 2-self.size, i],
                   [self.size, 2-self.size, i],
                   [self.size, -self.size, i]
                 ] for i in range(-self.size+2, self.size-2, 2)]],
            ]

        # Have to add this yet, need something to generate it for different sizes
        self.corner_pieces = [
            # Front
            # 0
            [[-self.size, -self.size, self.size],
             [-self.size, 2-self.size, self.size],
             [2-self.size, 2-self.size, self.size],
             [2-self.size, -self.size, self.size],
             [-self.size, -self.size, self.size-2],
             [-self.size, 2-self.size, self.size-2],
             [2-self.size, 2-self.size, self.size-2],
             [2-self.size, -self.size, self.size-2]],

            # 1
            [[-self.size, self.size-2, self.size],
             [-self.size, self.size, self.size],
             [2-self.size, self.size, self.size],
             [2-self.size, self.size-2, self.size],
             [-self.size, self.size-2, self.size-2],
             [-self.size, self.size, self.size-2],
             [2-self.size, self.size, self.size-2],
             [2-self.size, self.size-2, self.size-2]],

            # 2
            [[self.size-2, self.size-2, self.size],
             [self.size-2, self.size, self.size],
             [self.size, self.size, self.size],
             [self.size, self.size-2, self.size],
             [self.size-2, self.size-2, self.size-2],
             [self.size-2, self.size, self.size-2],
             [self.size, self.size, self.size-2],
             [self.size, self.size-2, self.size-2]],

            # 3
            [[self.size-2, -self.size, self.size],
             [self.size-2, 2-self.size, self.size],
             [self.size, 2-self.size, self.size],
             [self.size, -self.size, self.size],
             [self.size-2, -self.size, self.size-2],
             [self.size-2, 2-self.size, self.size-2],
             [self.size, 2-self.size, self.size-2],
             [self.size, -self.size, self.size-2]],

            # Back
            # 0
            [[-self.size, -self.size, 2-self.size],
             [-self.size, 2-self.size, 2-self.size],
             [2-self.size, 2-self.size, 2-self.size],
             [2-self.size, -self.size, 2-self.size],
             [-self.size, -self.size, -self.size],
             [-self.size, 2-self.size, -self.size],
             [2-self.size, 2-self.size, -self.size],
             [2-self.size, -self.size, -self.size]],

            # 1
            [[-self.size, self.size-2, 2-self.size],
             [-self.size, self.size, 2-self.size],
             [2-self.size, self.size, 2-self.size],
             [2-self.size, self.size-2, 2-self.size],
             [-self.size, self.size-2, -self.size],
             [-self.size, self.size, -self.size],
             [2-self.size, self.size, -self.size],
             [2-self.size, self.size-2, -self.size]],

            # 2
            [[self.size-2, self.size-2, 2-self.size],
             [self.size-2, self.size, 2-self.size],
             [self.size, self.size, 2-self.size],
             [self.size, self.size-2, 2-self.size],
             [self.size-2, self.size-2, -self.size],
             [self.size-2, self.size, -self.size],
             [self.size, self.size, -self.size],
             [self.size, self.size-2, -self.size]],

            # 3
            [[self.size-2, -self.size, 2-self.size],
             [self.size-2, 2-self.size, 2-self.size],
             [self.size, 2-self.size, 2-self.size],
             [self.size, -self.size, 2-self.size],
             [self.size-2, -self.size, -self.size],
             [self.size-2, 2-self.size, -self.size],
             [self.size, 2-self.size, -self.size],
             [self.size, -self.size, -self.size]],
        ]


        # need to figure out what this is for and how to use it
        # mostly how to auto generate them for different sizes
        # [axis, index]
        self.front_edges = [
            [0, 0], # x
            [0, 1],
            [1, 0], # y
            [1, 3],
        ]
        self.left_edges = [
            [1, 0], # y
            [1, 1],
            [2, 0], # z
            [2, 1],
        ]
        self.back_edges = [
            [0, 2], # x
            [0, 3],
            [1, 1], # y
            [1, 2],
        ]
        self.right_edges = [
            [1, 2], # y
            [1, 3],
            [2, 2], # z
            [2, 3],
        ]
        self.up_edges = [
            [0, 1], # x
            [0, 2],
            [2, 1], # z
            [2, 2],
        ]
        self.down_edges = [
            [0, 0], # x
            [0, 3],
            [2, 0], # z
            [2, 3],
        ]
        self.edges = [self.front_edges, self.left_edges, self.back_edges,
                      self.right_edges, self.up_edges, self.down_edges]


        '''
               5____________6
               /           /|
              /           / |
            1/__________2/  |
            |           |   |
            |           |   |
            |           |   7
            |           |  /
            |           | /
            0___________3/
        '''
        # left-right right is positive
        # up-down up is positive
        # front-back front is positive
        """self.cube_verts = (
            (-3.0, -3.0, 3.0), # 0
            (-3.0, 3.0, 3.0),  # 1
            (3.0, 3.0, 3.0),   # 2
            (3.0, -3.0, 3.0),  # 3
            (-3.0, -3.0, -3.0), # 4
            (-3.0, 3.0, -3.0),  # 5
            (3.0, 3.0, -3.0),  # 6
            (3.0, -3.0, -3.0)  # 7
        )"""
        self.cube_verts = (
            (-self.size, -self.size, self.size),
            (-self.size, self.size, self.size),
            (self.size, self.size, self.size),
            (self.size, -self.size, self.size),
            (-self.size, -self.size, -self.size),
            (-self.size, self.size, -self.size),
            (self.size, self.size, -self.size),
            (self.size, -self.size, -self.size)
        )

        # Need to make this autogenerate as well I belive
        # autogenerating is not urgent as this is only used
        # in cube.py render_lines function which I don't know if it is even called
        self.cube_edges = (
            (0, 1),
            (0, 3),
            (0, 4),
            (2, 1),
            (2, 3),
            (2, 6),
            (5, 1),
            (5, 4),
            (5, 6),
            (7, 3),
            (7, 4),
            (7, 6),
        )

        # I don't think this needs to be changed
        self.cube_surfaces = (
            [0, 1, 2, 3], # front 0
            [4, 5, 1, 0], # left 1
            [7, 6, 5, 4], # back 2
            [3, 2, 6, 7], # right 3
            [1, 5, 6, 2], # up 4
            [4, 0, 3, 7], # down 5
        )

        # don't know what this is for
        self.pulse_color = [0, 0, 0]
        self.pulse_val = 0.04

        # probably need to do some autogenerating
        # Black inner sides of edge pieces
        self.edge_black_pat = [
            [0, 1, 2, 3, 4, 5],
            [0, 1, 2, 3, 4, 5],
            [0, 1, 2, 3, 4, 5],
        ]
        self.corner_color_pat = [
            [0, 1, 5], # 0
            [0, 1, 4], # 1
            [0, 3, 4],
            [0, 3, 5],
            [2, 1, 5],
            [2, 1, 4],
            [2, 3, 4],
            [2, 3, 5],
        ]
        self.corner_black_pat = [
            [2, 3, 4], # 0
            [2, 3, 5], # 1
            [2, 1, 5],
            [2, 1, 4],
            [0, 3, 4],
            [0, 3, 5],
            [0, 1, 5],
            [0, 1, 4],
        ]

        # What's this?
        self.tex_coords = [
            (0, 0),
            (1, 0),
            (1, 1),
            (0, 1),
        ]

    def add_padding(self, value): pass

    def center_piece(self, value):
        return
        front = [
            [[[i, j, self.size],
              [i, j+2, self.size],
              [i+2, j+2, self.size],
              [i+2, j, self.size],
              [i, j, self.size-2],
              [i, j+2, self.size-2],
              [i+2, j+2, self.size-2],
              [i+2, j, self.size-2]
             ] for i in range(-self.size+2, self.size-2, 2)
            ] for j in range(-self.size+2, self.size-2, 2)
        ]
