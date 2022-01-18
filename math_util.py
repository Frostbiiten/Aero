from math import sqrt

# Utility class for dealing with and manipulating vectors
class Vector2:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

    # Add operator overload
    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    # Subtract operator overload
    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    # Divide operator overload
    def __truediv__(self, other):
        if isinstance(other, self.__class__):
            return Vector2(self.x / other.x, self.y / other.y)
        else:
            return Vector2(self.x / other, self.y / other)

    # Multiply operator overload
    def __mul__(self, other):
        if isinstance(other, self.__class__):
            return Vector2(self.x * other.x, self.y * other.y)
        else:
            return Vector2(self.x * other, self.y * other)

    # String cast overload
    def __str__(self):
        return "({0}, {1})".format(self.x, self.y)

# Linearly interpolate between a and b at time t (0-1)
def lerp(a, b, t):
    return a + (b - a) * t

# Gets the squared magnitude of a vector, this is computationally faster
def sqr_magnitude(vector):
    return vector.x ** 2 + vector.y ** 2

# Gets the magnitude of a vector
def magnitude(vector):
    return sqrt(sqr_magnitude(vector))

# Returns the unit vector of the given vector; makes the magnitude 1
def normalize(vector):
    return vector / magnitude(vector)