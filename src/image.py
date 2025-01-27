class Image:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.pixels = [[None for _ in range(width)] for _ in range(height)]

    def set_pixel(self, x, y, color):
        self.pixels[y][x] = color

    def write_ppm(self, filename):
        Image.write_ppm_header(
            filename, self.width, self.height
        )
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
