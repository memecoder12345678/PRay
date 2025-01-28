import zlib
import struct


class Image:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.pixels = [[None for _ in range(width)] for _ in range(height)]

    def set_pixel(self, x, y, color):
        self.pixels[y][x] = color

    def write_ppm(self, filename):
        Image.write_ppm_header(filename, self.width, self.height)
        self.write_ppm_raw(filename)

    @staticmethod
    def write_ppm_header(im_fileobj, width=None, height=None):
        im_fileobj.write(f"P3 {width} {height}\n255\n")

    def write_ppm_raw(self, filename):
        def to_byte(c):
            return round(max(min(c * 255, 255), 0))

        for row in self.pixels:
            for color in row:
                filename.write(
                    f"{to_byte(color.x)} {to_byte(color.y)} {to_byte(color.z)} "
                )
            filename.write("\n")

    @classmethod
    def ppm2png(cls, ppm_file, img_fileobj):
        try:
            with open(ppm_file, "r") as f:
                dimensions = f.readline().strip().split()
                width, height = int(dimensions[1]), int(dimensions[2])
                f.readline()
                pixels = []
                for line in f:
                    pixels.extend(map(int, line.strip().split()))
            png_header = b"\x89PNG\r\n\x1a\n"
            img_fileobj.write(png_header)
            ihdr_data = struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)
            img_fileobj.write(cls.create_png_chunk(b"IHDR", ihdr_data))
            pixel_data = bytearray()
            for y in range(height):
                pixel_data.append(0)
                for x in range(width):
                    i = (y * width + x) * 3
                    r, g, b = pixels[i : i + 3]
                    pixel_data.extend([r, g, b, 255])
            compressed_data = zlib.compress(pixel_data)
            img_fileobj.write(cls.create_png_chunk(b"IDAT", compressed_data))
            img_fileobj.write(cls.create_png_chunk(b"IEND", b""))
        except Exception as e:
            raise RuntimeError(f"Error converting PPM to PNG: {str(e)}")

    @staticmethod
    def create_png_chunk(chunk_type, data):
        length = len(data)
        chunk = struct.pack(">I", length) + chunk_type + data
        crc = zlib.crc32(chunk[4:])
        chunk += struct.pack(">I", crc)
        return chunk
