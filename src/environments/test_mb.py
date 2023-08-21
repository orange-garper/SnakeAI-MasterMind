import numpy as np
from pygame.math import Vector2

class SettableVector2(Vector2):
    def __init__(self, *args,**kwargs):
        super().__init__(*args, **kwargs)
    
    def __hash__(self) -> int:
        return hash((self.x, self.y))

a = [SettableVector2((1, 2))]
print(set(a))