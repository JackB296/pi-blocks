import pygame as pg

pg.init()

WIDTH, HEIGHT = 1000, 800
BLUE = (0, 0, 255)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("PI Blocks")
clock = pg.time.Clock()

font = pg.font.SysFont('monospace', 15)
collision_font = pg.font.SysFont('monospace', 30)

class Block:
    def __init__(self, mass, x, wall_y, velocity):
        # MASS IN KG
        self.mass = mass
        self.size = mass/2 if mass/2 > 30 and mass < 100 else 100 if mass > 100 else 30
        self.color = (255, 255, 255)
        self.pos = pg.math.Vector2(x, wall_y - self.size)
        self.velocity = velocity
    
    def draw(self, screen):
        # Draw the Rect
        pg.draw.rect(screen, self.color, (self.pos.x, self.pos.y, self.size, self.size))

        # Draw mass above our cube
        mass_surface = font.render((str(self.mass) + " kg"), False, (255, 255, 255))
        screen.blit(mass_surface, (self.pos - (0, 15)))

    def move(self):
        self.pos.x += self.velocity

    def bounce(self, other):
        v1_initial = self.velocity
        v2_initial = other.velocity

        self.velocity = (((self.mass - other.mass)/(self.mass + other.mass)) * v1_initial) + (((2 * other.mass)/(self.mass + other.mass)) * v2_initial)
        other.velocity = (((other.mass - self.mass)/(self.mass + other.mass)) * v2_initial) + (((2 * self.mass)/(self.mass + other.mass)) * v1_initial)

    def collide(self, other):
        return not (self.pos.x + self.size < other.pos.x or self.pos.x > other.pos.x + self.size)

class Sim:
    def __init__(self):
        self.collisions = 0
        self.time_steps = 100_000 # Euler integration
        self.wall_x = 200
        self.wall_y = HEIGHT/4*3
        self.blocks = []
        self.map_surface = pg.Surface((WIDTH, HEIGHT))
        self.collision_surface = collision_font.render(("# Collisions: " + str(self.collisions)), False, (255, 255, 255))
        self.digits = 6
        self.initialize()

    def main(self):
        running = True
        while running:
            screen.fill((0, 0, 0))

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

            for _ in range(self.time_steps):
                self.update()
            self.draw()

            clock.tick(60)
            
            pg.display.flip()

    def initialize(self):
        # Our first smaller block
        self.blocks.append(Block(100, self.wall_x + 100, self.wall_y, 0))
        # Our second bigger block make mass 100^number of digits to generate and divide velocity by time steps
        self.blocks.append(Block(100**self.digits, WIDTH-200, self.wall_y, -3/self.time_steps))
        #Draw our background and collision
        self.draw_map()
    
    
    def update(self):
        # If block 1 is colliding with anything
        collide = self.blocks[0].collide(self.blocks[1])
        if collide:
            self.update_collisions()
            self.blocks[0].bounce(self.blocks[1])
        if self.blocks[0].pos.x <= self.wall_x:
            self.update_collisions()
            self.blocks[0].velocity = -self.blocks[0].velocity
        for block in self.blocks:
            block.move()
        
    def draw(self):
        screen.blit(self.map_surface, (0, 0))
        self.draw_blocks()
        screen.blit(self.collision_surface, (WIDTH/2, 10))

    def update_collisions(self):
        self.collisions += 1
        self.collision_surface = collision_font.render(("# Collisions: " + str(self.collisions)), False, (255, 255, 255))

    def draw_map(self):
        self.map_surface.fill((0, 0, 0))
        # Start at top of screen near left side and move to near center, This is our wall
        pg.draw.line(self.map_surface, WHITE, (self.wall_x, 0), (self.wall_x, self.wall_y), 1)
        # Start at last line pos and move to right side of screen, This is our ground
        pg.draw.line(self.map_surface, WHITE, (self.wall_x, self.wall_y), (WIDTH, self.wall_y), 1)

    def draw_blocks(self):
        for block in self.blocks:
            block.draw(screen)

    

sim = Sim()
sim.main()