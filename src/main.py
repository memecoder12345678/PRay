import argparse
import importlib
import os
from multiprocessing import cpu_count

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
    parser.add_argument(
        "-p",
        "--process",
        type=int,
        default=0,
        help="Number of processes to use (default: number of CPUs)",
    )
    args = parser.parse_args()
    samples = args.samples
    process = args.process
    if process < 0:
        print("Error: process must be at least 0")
        return
    elif process == 0:
        process = cpu_count()
    else:
        process = min(process, cpu_count())
    if samples < 1:
        print("Error: samples must be at least 1")
        return
    mod = importlib.import_module(args.scene)
    scene = Scene(mod.CAMERA, mod.OBJECTS, mod.LIGHTS, mod.WIDTH, mod.HEIGHT)
    engine = RenderEngine(samples_per_pixel=samples)
    os.chdir(os.path.dirname(os.path.abspath(mod.__file__)))
    with open(mod.RENDERED_IMG, "w") as img_file:
        engine.render_multiprocess(scene, process, img_file)


if __name__ == "__main__":
    main()
