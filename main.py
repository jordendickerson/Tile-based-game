#Tile Based Shooter
#Jorden Dickerson 2022

#Artwork by Kenney

from settings import *
from sprites import *
from tilemap import *
import pygame as pg
from os import path

#YOU MUST INSTALL PYGAME, PYTMX, AND PYTWEENING ON YOUR COMPUTER FOR THIS GAME TO RUN
#open the terminal on your system and type 'pip install [pygame/pytmx/pytweening]'

#TO MAKE MAPS USE TILED MAP EDITOR


#HUD functions
def draw_player_health(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x,y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    if pct > 0.6:
        color = GREEN
    elif pct > 0.3:
        color = YELLOW
    else:
        color = RED
    pg.draw.rect(surf, color, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)

class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.running = True

    def load_data(self):
        #load map
        self.map = TiledMap(path.join(maps_Folder, 'map.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        #load images
        self.player_img = pg.image.load(path.join(img_Folder, PLAYER_IMG)).convert_alpha()
        self.wall_img = pg.image.load(path.join(img_Folder, WALL_IMG)).convert()
        self.mob_img = pg.image.load(path.join(img_Folder, MOB_IMG)).convert_alpha()
        self.bullet_img = pg.image.load(path.join(img_Folder, BULLET_IMG)).convert()
        self.gun_flashes = []
        for img in MUZZLE_FLASHES:
            self.gun_flashes.append(pg.image.load(path.join(img_Folder, img)).convert_alpha())
        self.item_images = {}
        for item in ITEM_IMAGES:
            self.item_images[item] = pg.image.load(path.join(img_Folder, ITEM_IMAGES[item])).convert_alpha()
        # Sound Loading
        pg.mixer.music.load(path.join(audio_Folder, BG_MUSIC))
        #effects sounds
        self.effects_sounds = {}
        for type in EFFECTS_SOUNDS:
            self.effects_sounds[type] = pg.mixer.Sound(path.join(audio_Folder, EFFECTS_SOUNDS[type]))
        #weapons souds
        self.weapon_sounds = {}
        self.weapon_sounds['gun'] = []
        for snd in WEAPON_SOUNDS_GUN:
            s = pg.mixer.Sound(path.join(audio_Folder, snd))
            s.set_volume(0.5)
            self.weapon_sounds['gun'].append(s)
        #zombie sounds
        self.zombie_moan_sounds = []
        for snd in ZOMBIE_MOAN_SOUNDS:
            s = pg.mixer.Sound(path.join(audio_Folder, snd))
            s.set_volume(0.3)
            self.zombie_moan_sounds.append(s)
        self.zombie_hit_sounds = []
        for snd in ZOMBIE_HIT_SOUNDS:
            s = pg.mixer.Sound(path.join(audio_Folder, snd))
            s.set_volume(0.5)
            self.zombie_hit_sounds.append(s)
        #player hit sounds
        self.player_hit_sounds = []
        for snd in PLAYER_HIT_SOUNDS:
            s = pg.mixer.Sound(path.join(audio_Folder, snd))
            s.set_volume(0.6)
            self.player_hit_sounds.append(s)



    def new(self):
        self.load_data()
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.items = pg.sprite.Group()

        ###For making maps out of text files###
        # for row, tiles in enumerate(self.map.data):
        #     for col, tile in enumerate(tiles):
        #         if tile == '1':
        #             Wall(self, col, row)
        #         if tile == 'M':
        #             Mob(self, col, row)
        #         if tile == "P":
        #             self.player = Player(self, col, row)

        for tile_object in self.map.tmxdata.objects:
            obj_center = vec(tile_object.x + tile_object.width / 2,
                             tile_object.y + tile_object.height / 2)
            if tile_object.name == 'player':
                self.player = Player(self, obj_center.x, obj_center.y)
            if tile_object.name == 'zombie':
                Mob(self, tile_object.x, obj_center.y)
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name in ['health']:
                Item(self, obj_center, tile_object.name)
        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False
        self.effects_sounds['level_start'].play()
        self.run()

    def run(self):
        pg.mixer.music.play(loops=-1)
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def update(self):
        #Update loops
        self.all_sprites.update()
        self.camera.update(self.player)
        #player hits health pack
        hits = pg.sprite.spritecollide(self.player, self.items, False)
        for hit in hits:
            if hit.type == 'health' and self.player.health < PLAYER_HEALTH:
                hit.kill()
                self.player.add_health(HEALTH_PACK_AMOUNT)
                self.effects_sounds['health_up'].play()
        #mobs hit player
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        for hit in hits:
            if random.random() < 0.7:
                random.choice(self.player_hit_sounds).play()
            self.player.health -= MOB_DAMAGE
            hit.vel = vec(0,0)
            if self.player.health <= 0:
                self.playing = False
        if hits:
            self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)
        #bullet hits mobs
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for hit in hits:
            hit.health -= BULLET_DAMAGE
            hit.vel = vec(0,0)

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_h:
                    self.draw_debug = not self.draw_debug
    def draw_grid(self):
        for x in range(0,WIDTH,TILESIZE):
            pg.draw.line(self.screen, LIGHTGRAY, (x, 0), (x, HEIGHT))
        for y in range(0,HEIGHT,TILESIZE):
            pg.draw.line(self.screen, LIGHTGRAY, (0, y), (WIDTH, y))

    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        #Draw sprites

        #draw map
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        # self.draw_grid()
        for sprite in self.all_sprites:
            if isinstance(sprite, Mob):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.draw_debug:
                pg.draw.rect(self.screen, skyBlue, self.camera.apply_rect(sprite.hit_rect), 1)
        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(self.screen, skyBlue, self.camera.apply_rect(wall.rect), 1)

        # pg.draw.rect(self.screen, WHITE, self.player.hit_rect, 2)
        #HUD
        draw_player_health(self.screen, 10, 10, self.player.health / PLAYER_HEALTH)
        #after drawing, flip display
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        pass

    def show_go_screen(self):
        # game over/continue
        pass

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()