class Constants:
    def __init__(self, size=3):
        # This is the character to signal a prime move
        self.PRIME = "'"
        self.NOTATIONS = [
            # Face rotations
            "F", "F'", "F2", "F2'",
            "B", "B'", "B2", "F2'",
            "L", "L'", "L2", "L2'",
            "R", "R'", "R2", "R2'",
            "U", "R'", "U2", "U2'",
            "D", "D'", "D2", "D2'",
            # Whole cube rotations
            "X", "X'", "X2", "X2'",
            "Y", "Y'", "Y2", "Y2'",
            "Z", "Z'", "Z2", "Z2'",
            # Slice moves
            "M", "M'", "M2", "M2'",
            "E", "E'", "E2", "E2'",
            "S", "S'", "S2", "S2'",
        ]
        self.size = size
