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
        default=32,
        help="Number of samples per pixel for anti-aliasing (default: 32)",
    )
    parser.add_argument(
        "-p",
        "--process",
        type=int,
        default=0,
        help="Number of processes to use (default: number of CPUs)",
    )
    parser.add_argument(
        "-r",
        "--raw",
        action="store_true",
        help="Output raw PPM instead of PNG",
    )
    args = parser.parse_args()
    samples = args.samples
    process = args.process
    raw = args.raw
    if process < 0:
        raise ValueError("Error: process must be at least 0")
    elif process == 0:
        process = cpu_count()
    else:
        process = min(process, cpu_count())
    if samples < 1:
        raise ValueError("Error: samples must be at least 1")
    mod = importlib.import_module(args.scene)
    scene = Scene(mod.CAMERA, mod.OBJECTS, mod.LIGHTS, mod.WIDTH, mod.HEIGHT)
    engine = RenderEngine(samples_per_pixel=samples)
    os.chdir(os.path.dirname(os.path.abspath(mod.__file__)))
    if raw:
        with open(mod.RENDERED_IMG, "w") as img_file:
            engine.render_multiprocess(scene, process, img_file, raw)
    else:
        with open(mod.RENDERED_IMG, "wb") as img_file:
            engine.render_multiprocess(scene, process, img_file, raw)


if __name__ == "__main__":
    main()
