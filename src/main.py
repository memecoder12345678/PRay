import argparse
import importlib
import os
from engine import RenderEngine
from scene import Scene


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("scene", help="Path to scene file (without .py extension)")
    parser.add_argument(
        "-s",
        "--samples",
        type=int,
        default=4,
        help="Number of samples per pixel for anti-aliasing (default: 4)",
    )
    args = parser.parse_args()
    samples = args.samples
    if samples < 1:
        print("Error: samples must be at least 1")
        return
    mod = importlib.import_module(args.scene)
    scene = Scene(mod.CAMERA, mod.OBJECTS, mod.LIGHTS, mod.WIDTH, mod.HEIGHT)
    engine = RenderEngine(samples_per_pixel=samples)
    image = engine.render(scene)
    os.chdir(os.path.dirname(os.path.abspath(mod.__file__)))
    with open(mod.RENDERED_IMG, "w") as img_file:
        image.write_ppm(img_file)


if __name__ == "__main__":
    main()
