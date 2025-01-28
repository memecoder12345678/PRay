import random
import shutil
import tempfile
from multiprocessing import Process, Value
from pathlib import Path

from color import Color
from image import Image
from point import Point
from ray import Ray


class RenderEngine:
    MAX_DEPTH = 5
    MIN_DISPLACE = 0.0001

    def __init__(self, samples_per_pixel=4):
        self.samples_per_pixel = samples_per_pixel

    def render_multiprocess(self, scene, processes_count, img_fileobj):
        def split_range(count, parts):
            d, r = divmod(count, parts)
            return [
                (i * d + min(i, r), (i + 1) * d + min(i + 1, r)) for i in range(parts)
            ]

        width = scene.width
        height = scene.height
        ranges = split_range(height, processes_count)
        temp_dir = tempfile.mkdtemp()
        temp_files_tmpl = "render_part_{}.temp"
        processes = []
        try:
            rows_done = Value("i", 0)
            for hmin, hmax in ranges:
                part_file = Path(temp_dir) / temp_files_tmpl.format(hmin)
                ppm_file = Path(temp_dir) / f"raw_output.ppm"
                processes.append(
                    Process(
                        target=self.render,
                        args=(scene, hmin, hmax, part_file, rows_done),
                    )
                )
            for p in processes:
                p.start()
            for p in processes:
                p.join()
            with open(ppm_file, "w") as f:
                Image.write_ppm_header(f, width=width, height=height)
            for hmin, _ in ranges:
                part_file = Path(temp_dir) / temp_files_tmpl.format(hmin)
                with open(ppm_file, "a") as f:
                    f.write(open(part_file, "r").read())
            Image.ppm2png(ppm_file, img_fileobj)
        finally:
            for p in processes:
                p.terminate()
            shutil.rmtree(temp_dir, ignore_errors=True)

    def render(self, scene, hmin, hmax, part_file, rows_done):
        width = scene.width
        height = scene.height
        aspect_ratio = width / height
        x0 = -1
        x1 = 1
        xstep = (x1 - x0) / (width - 1)
        y0 = -1 / aspect_ratio
        y1 = 1 / aspect_ratio
        ystep = (y1 - y0) / (height - 1)
        camera = scene.camera
        pixels = Image(width, hmax - hmin)
        for j in range(hmin, hmax):
            y = y0 + j * ystep
            for i in range(width):
                x = x0 + i * xstep
                pixel_color = Color(0, 0, 0)
                if self.samples_per_pixel == 1:
                    ray = Ray(camera, Point(x, y) - camera)
                    pixel_color = self.ray_trace(ray, scene)
                else:
                    for _ in range(self.samples_per_pixel):
                        jitter_x = x + random.uniform(-0.5, 0.5) * xstep
                        jitter_y = y + random.uniform(-0.5, 0.5) * ystep
                        ray = Ray(camera, Point(jitter_x, jitter_y) - camera)
                        pixel_color += self.ray_trace(ray, scene)
                pixel_color *= 1.0 / self.samples_per_pixel
                pixels.set_pixel(i, j - hmin, pixel_color)
            with rows_done.get_lock():
                rows_done.value += 1
                print(
                    f"\rProcess: [{('#' * int(float(rows_done.value) / float(height) * 50)).ljust(50, '.')}"
                    f"] {float(rows_done.value) / float(height) * 100:5.2f}%",
                    end="",
                )
                if (
                    float(f"{float(rows_done.value) / float(height) * 100:5.2f}")
                    == 100.00
                ):
                    print()
        with open(part_file, "w") as f:
            pixels.write_ppm_raw(f)

    def ray_trace(self, ray, scene, depth=0):
        color = Color(0, 0, 0)
        dist_hit, obj_hit = self.find_nearest(ray, scene)
        if obj_hit is None:
            return color
        hit_pos = ray.origin + ray.direction * dist_hit
        hit_normal = obj_hit.normal(hit_pos)
        color += self.color_at(obj_hit, hit_pos, hit_normal, scene)
        if depth < self.MAX_DEPTH:
            new_ray_pos = hit_pos + hit_normal * self.MIN_DISPLACE
            new_ray_dir = (
                ray.direction - 2 * ray.direction.dot_product(hit_normal) * hit_normal
            )
            new_ray = Ray(new_ray_pos, new_ray_dir)
            color += (
                self.ray_trace(new_ray, scene, depth + 1) * obj_hit.material.reflection
            )
        return color

    def find_nearest(self, ray, scene):
        dist_min = None
        obj_hit = None
        for obj in scene.objects:
            dist = obj.intersects(ray)
            if dist is not None and (obj_hit is None or dist < dist_min):
                dist_min = dist
                obj_hit = obj
        return (dist_min, obj_hit)

    def color_at(self, obj_hit, hit_pos, normal, scene):
        material = obj_hit.material
        obj_color = material.color_at(hit_pos)
        to_cam = scene.camera - hit_pos
        specular_k = 50
        color = Color.from_hex("#000000")
        for light in scene.lights:
            color += material.ambient * obj_color * light.color
            to_light = Ray(hit_pos, light.position - hit_pos)
            shadow_ray = Ray(
                hit_pos + normal * self.MIN_DISPLACE, light.position - hit_pos
            )
            dist_to_light, _ = self.find_nearest(shadow_ray, scene)
            if dist_to_light is not None and dist_to_light < to_light.length():
                continue
            color += (
                obj_color
                * material.diffuse
                * max(normal.dot_product(to_light.direction), 0)
            )
            half_vector = (to_light.direction + to_cam).normalize()
            color += (
                light.color
                * material.specular
                * max(normal.dot_product(half_vector), 0) ** specular_k
            )
        return color
