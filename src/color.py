from vector import Vector


class Color(Vector):
    @classmethod
    def from_hex(cls, hexcolor="#FFFFFF"):
        hexcolor = hexcolor.upper()
        if hexcolor[0] != "#":
            raise ValueError("Hex color must start with #")
        elif len(hexcolor) != 7:
            raise ValueError("Hex color must be 7 characters long")
        elif not all([c in "0123456789ABCDEF" for c in hexcolor[1:]]):
            raise ValueError("Hex color must be in the format #RRGGBB (HEX)")
        r = int(hexcolor[1:3], 16) / 255.0
        g = int(hexcolor[3:5], 16) / 255.0
        b = int(hexcolor[5:7], 16) / 255.0
        return cls(r, g, b)
