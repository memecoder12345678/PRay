from color import Color
from light import Light
from material import MirrorMaterial, Material
from point import Point
from geometry import Sphere
from vector import Vector

WIDTH = 960
HEIGHT = 540
RENDERED_IMG = "test_sphere.ppm"
CAMERA = Vector(0, -0.35, -1)
OBJECTS = [
    Sphere(
        Point(0, 10000.5, 1),
        10000.0,
        MirrorMaterial(
            color=Color.from_hex("#606060"), ambient=0.2, reflection=0.2, diffuse=0.1
        ),
    ),
    Sphere(
        Point(0.75, -0.1, 1),
        0.6,
        Material(
            Color.from_hex("#306998"),
            ambient=0.1,
            diffuse=0.7,
            specular=1.0,
            reflection=0.3,
        ),
    ),
    Sphere(
        Point(-0.75, -0.1, 2.25),
        0.6,
        Material(
            Color.from_hex("#FFD43B"),
            ambient=0.1,
            diffuse=0.7,
            specular=1.0,
            reflection=0.3,
        ),
    ),
]
LIGHTS = [
    Light(Point(2.0, -0.5, -10), Color.from_hex("#FFFFFF")),
    Light(Point(-2.0, -0.5, -5), Color.from_hex("#FFE5B4")),
    Light(Point(0, -10.5, 0), Color.from_hex("#E6E6E6")),
]
