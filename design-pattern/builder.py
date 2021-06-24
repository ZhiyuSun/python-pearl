class Hero:
    def __init__(self, name):
        self.name = name
        self.blood = None
        self.attack = None
        self.job = None

    def __str__(self):
        info = ("Name {}".format(self.name), "blood: {}".format(self.blood),
                "attack: {}".format(self.attack), "job: {}".format(self.job))
        return '\n'.join(info)


class HeroBuilder:
    def __init__(self):
        self.hero = Hero("Monki")

    def configure_blood(self, amount):
        self.hero.blood = amount

    def configure_attack(self, amount):
        self.hero.attack = amount

    def configure_job(self, job):
        self.hero.job = job

class Game:
    def __init__(self):
        self.builder = None

    def construct_hero(self, blood, attack, job):
        self.builder = HeroBuilder()
        self.builder.configure_blood(blood)
        self.builder.configure_attack(attack),
        self.builder.configure_job(job)

    @property
    def hero(self):
        return self.builder.hero

game = Game()
game.construct_hero(5000, 200, "warrior")
hero = game.hero
print(hero)