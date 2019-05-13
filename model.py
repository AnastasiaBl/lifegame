import random


class Model():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.field_values = [[False] * width for x in range(height)]
        self.field_history = []

    def clear_history(self):
        self.field_history = [self.field_values]

    def step(self):
        field_values_new = [[False] * self.width for x in range(self.height)]

        for y in range(self.height):
            for x in range(self.width):
                neighbours_on = 0
                if x>0 and self.field_values[y][x-1]: neighbours_on += 1
                if y>0 and self.field_values[y-1][x]: neighbours_on += 1
                if x<self.width-1 and self.field_values[y][x+1]: neighbours_on += 1
                if y<self.height-1 and self.field_values[y+1][x]: neighbours_on += 1

                if x>0 and y>0 and self.field_values[y-1][x-1]: neighbours_on += 1
                if x<self.width-1 and y>0 and self.field_values[y-1][x+1]: neighbours_on += 1
                if x>0 and y<self.height-1 and self.field_values[y+1][x-1]: neighbours_on += 1
                if x<self.width-1 and y<self.height-1 and self.field_values[y+1][x+1]: neighbours_on += 1

                field_values_new[y][x] = self.field_values[y][x]
                if not self.field_values[y][x] and neighbours_on == 3:
                    field_values_new[y][x] = True
                elif self.field_values[y][x] and (neighbours_on < 2 or neighbours_on > 3):
                    field_values_new[y][x] = False

        self.field_values = field_values_new

        # Проверим не было ли уже такого состояния раньше
        if field_values_new in self.field_history:
            return True
        self.field_history.append(field_values_new)
        return False
