import math;
class Vector3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"Vector3D({self.x},{self.y},{self.z})"

    def norm(self):
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
    def __add__(self, someVector):
        return Vector3D(self.x + someVector.x, self.y + someVector.y, self.z + someVector.z)
    def __sub__(self, someVector):
        return Vector3D(self.x - someVector.x, self.y - someVector.y, self.z - someVector.z)
    def dot(self,someVector):
        return self.x * someVector.x + self.y * someVector.y + self.z * someVector.z
    def __mul__(self, scalar):
        return Vector3D(self.x * scalar, self.y * scalar, self.z * scalar)
    def cross(self, someVector):
         return Vector3D( self.y * someVector.z - self.z*  someVector.y, self.z * someVector.x - self.x * someVector.z, self.x * someVector.y - self.y * someVector.x)
    @staticmethod
    def are_orthogonal(vec1, vec2):
        return Vector3D(vec1.x,vec1.y,vec1.z).dot(vec2)


# Utworzenie obiektu klasy Samochod
