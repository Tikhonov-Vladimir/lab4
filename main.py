from random import randint
from math import sqrt


class Field:
    def __init__(self, width, height):
        self.characters = []
        self.width = width
        self.height = height

    def add_character(self, character):
        self.characters.append(character)

    def remove_character(self, character):
        self.characters.remove(character)


class Character:
    def __init__(self, name, speed, health, strength, attack_strength, attack_distance, reload, _field):
        self.name = name
        self.capacity = 3
        self._field = _field

        _field.add_character(self)

        if speed == 'slow':
            self.speed = 100
        elif speed == 'normal':
            self.speed = 150
        elif speed == 'fast':
            self.speed = 200
        else:
            raise ValueError('Unknown speed')

        if attack_distance == 'low':
            self.attack_distance = 100
        elif attack_distance == 'normal':
            self.attack_distance = 150
        elif attack_distance == 'long':
            self.attack_distance = 200
        else:
            raise ValueError('Unknown distance')

        if reload == 'slow':
            self.reload = 50
        elif reload == 'normal':
            self.reload = 500
        elif reload == 'fast':
            self.reload = 1000
        else:
            raise ValueError('Unknown reload')

        self.health = health * strength
        self.strength = strength
        self.attack_strength = attack_strength * strength
        self.x = randint(0, field.width)
        self.y = randint(0, field.height)

    def move(self, x, y):
        if self.x + x * self.speed <= self._field.width:
            if self.x + x * self.speed < 0:
                self.x = 0
            else:
                self.x += x * self.speed
        else:
            self.x = self._field.width

        if self.y + y * self.speed <= self._field.height:
            if self.y + y * self.speed < 0:
                self.y = 0
            else:
                self.y += y * self.speed
        else:
            self.y = self._field.height

    def take_damage(self, damage):
        self.health -= damage
        print(self.name, 'takes', damage, 'damage')
        if self.health <= 0:
            self._field.remove_character(self)
            self._field = None
            print(self.name, 'dies((9')

    def attack(self):
        if self.capacity < 1:
            return
        min_char = None
        _min = float('inf')
        for ch in self._field.characters:
            if ch == self:
                continue
            dist = sqrt((self.x - ch.x) ** 2 + (self.y - ch.y) ** 2)

            if _min > dist and self.attack_distance >= dist:
                _min = dist
                min_char = ch

        if min_char:
            self.capacity -= 1
            print(self.name, 'attacking', min_char.name, 'with', self.attack_strength, 'points')
            min_char.take_damage(self.attack_strength)

    def update(self):
        if self.capacity == 3:
            return
        elif self.capacity > 3:
            self.capacity = 3
            return
        self.capacity += self.reload / 1000


class Shelly(Character):
    def __init__(self, strength, _field):
        super().__init__('Shelly', 'normal', 3800, strength, 300, 'long', 'normal', _field)


class Piper(Character):
    def __init__(self, strength, _field):
        super().__init__('Piper', 'normal', 2400, strength, 1520, 'long', 'slow', _field)


class Bull(Character):
    def __init__(self, strength, _field):
        super().__init__('Bull', 'fast', 5000, strength, 400, 'normal', 'normal', _field)


if __name__ == '__main__':
    field = Field(1000, 1000)

    player1: Character = Shelly(1, field)
    player2: Character = Piper(1, field)
    player3: Character = Bull(1, field)

    while len(field.characters) > 1:
        for c in field.characters:
            c.update()
            c.move(randint(-1, 1), randint(-1, 1))
            c.attack()

    print('The winner is ', field.characters[0].name, '!')
