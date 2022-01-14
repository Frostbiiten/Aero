class vector2:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

    # Add operator overload
    def __add__(self, other):
        return vector2(self.x + other.x, self.y + other.y)

    # Subtract operator overload
    def __sub__(self, other):
        return vector2(self.x - other.x, self.y - other.y)

    # Divide operator overload
    def __truediv__(self, other):
        if isinstance(other, self.__class__):
            return vector2(self.x / other.x, self.y / other.y)
        else:
            return vector2(self.x / other, self.y / other)

    # Multiply operator overload
    def __mul__(self, other):
        if isinstance(other, self.__class__):
            return vector2(self.x * other.x, self.y * other.y)
        else:
            return vector2(self.x * other, self.y * other)

    # String cast overload
    def __str__(self):
        return "({0}, {1})".format(self.x, self.y)

# Linearly interpolated between a and b at time t (0-1)
def lerp(a, b, t):
    return a + (b - a) * t
