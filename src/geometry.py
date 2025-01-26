import math
from vector import Vector
from point import Point


class Sphere:
    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material

    def intersects(self, ray):
        sphere_to_ray = ray.origin - self.center
        b = 2 * ray.direction.dot_product(sphere_to_ray)
        c = sphere_to_ray.dot_product(sphere_to_ray) - self.radius * self.radius
        discriminant = b * b - 4 * c
        if discriminant >= 0:
            dist = (-b - math.sqrt(discriminant)) / 2
            if dist > 0:
                return dist
        return None

    def normal(self, surface_point):
        return (surface_point - self.center).normalize()


class Rectangle:
    def __init__(self, center, width, height, normal, material):
        self.center = center
        self.width = width
        self.height = height
        self.normal_vector = normal.normalize()
        self.material = material
        self.u = Vector(1, 0, 0) if abs(self.normal_vector.y) == 1 else Vector(0, 1, 0)
        self.right = self.normal_vector.cross_product(self.u).normalize()
        self.up = self.right.cross_product(self.normal_vector)

    def intersects(self, ray):
        denom = ray.direction.dot_product(self.normal_vector)
        if abs(denom) < 0.0001:
            return None
        t = (self.center - ray.origin).dot_product(self.normal_vector) / denom
        if t < 0:
            return None
        hit_point = ray.origin + ray.direction * t
        local_point = hit_point - self.center
        right_proj = local_point.dot_product(self.right)
        up_proj = local_point.dot_product(self.up)
        if abs(right_proj) <= self.width / 2 and abs(up_proj) <= self.height / 2:
            return t
        return None

    def normal(self, surface_point):
        return self.normal_vector


class Box:
    def __init__(self, center, width, height, depth, material):
        self.center = center
        self.width = width
        self.height = height
        self.depth = depth
        self.material = material
        self.faces = [
            Rectangle(
                Point(center.x, center.y, center.z - depth / 2),
                width,
                height,
                Vector(0, 0, -1),
                material,
            ),
            Rectangle(
                Point(center.x, center.y, center.z + depth / 2),
                width,
                height,
                Vector(0, 0, 1),
                material,
            ),
            Rectangle(
                Point(center.x - width / 2, center.y, center.z),
                depth,
                height,
                Vector(-1, 0, 0),
                material,
            ),
            Rectangle(
                Point(center.x + width / 2, center.y, center.z),
                depth,
                height,
                Vector(1, 0, 0),
                material,
            ),
            Rectangle(
                Point(center.x, center.y + height / 2, center.z),
                width,
                depth,
                Vector(0, 1, 0),
                material,
            ),
            Rectangle(
                Point(center.x, center.y - height / 2, center.z),
                width,
                depth,
                Vector(0, -1, 0),
                material,
            ),
        ]

    def intersects(self, ray):
        nearest = None
        for face in self.faces:
            dist = face.intersects(ray)
            if dist is not None and (nearest is None or dist < nearest):
                nearest = dist
        return nearest

    def normal(self, surface_point):
        for face in self.faces:
            if (
                abs((surface_point - face.center).dot_product(face.normal_vector))
                < 0.0001
            ):
                return face.normal_vector
        return Vector(0, 1, 0)
