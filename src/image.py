class Image:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.pixels = [[0 for _ in range(width)] for _ in range(height)]

    def set_pixel(self, x, y, color):
        self.pixels[y][x] = color

    def write_ppm(self, filename):
        def to_byte(c):
            return round(max(min(c * 255, 255), 0))

        filename.write(f"P3 {self.width} {self.height}\n255\n")
        for row in self.pixels:
            for color in row:
                filename.write(
                    f"{to_byte(color.x)} {to_byte(color.y)} {to_byte(color.z)} "
                )
            filename.write("\n")
