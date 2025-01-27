from color import Color


class Material:
    def __init__(
        self,
        color=Color.from_hex("#FFFFFF"),
        ambient=0.05,
        diffuse=1.0,
        specular=1.0,
        reflection=0.5,
    ):
        self.color = color
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.reflection = reflection

    def color_at(self, _):
        return self.color


class ChequeredMaterial:
    def __init__(
        self,
        color1=Color.from_hex("#808080"),
        color2=Color.from_hex("#606060"),
        ambient=0.05,
        diffuse=1.0,
        specular=1.0,
        reflection=0.5,
    ):
        self.color1 = color1
        self.color2 = color2
        self.ambient = ambient
        self.diffuse = diffuse
        self.reflection = reflection
        self.specular = specular

    def color_at(self, position):
        if int((position.x + 5.0) * 3.0) % 2 == int(position.z * 3.0) % 2:
            return self.color1
        else:
            return self.color2


class MirrorMaterial:
    def __init__(
        self,
        color=Color.from_hex("#FFFFFF"),
        ambient=0.05,
        diffuse=0.05,
        specular=1.0,
        reflection=1.0,
    ):
        self.color = color
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.reflection = reflection
        if diffuse > 0.1:
            raise ValueError("Diffuse should be less than 0.1 for mirror material")

    def color_at(self, _):
        return self.color
