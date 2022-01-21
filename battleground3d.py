from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader


if __name__ == "__main__":
    app = Ursina()


class Battleground():

    def __init__(self):

        Entity.default_shader = lit_with_shadows_shader

        self.sky = Sky()
        
        self.ground = Entity(
            model='plane',
            texture='grass',
            collider='mesh',
            scale=(100, 1, 50))
        
        self.player = FirstPersonController()

        self.wall = []

        for i in range(30):
            for j in range(3):
                self.wall.append(Entity(
                    model = 'cube',
                    texture = 'white_cube',
                    collider = 'box',
                    position= (i, 0.5+j, 5))
                )
        
        self.sun = DirectionalLight()
        self.sun.look_at(Vec3(1,-1,-1))
        self.disable()
    

    def enable(self):
        Entity.default_shader = lit_with_shadows_shader
        self.player.enable()


    def disable(self):
        Entity.default_shader = None
        self.player.disable()



if __name__ == "__main__":
    Entity.default_shader = lit_with_shadows_shader

    b = Battleground()
    b.enable()

    app.run()