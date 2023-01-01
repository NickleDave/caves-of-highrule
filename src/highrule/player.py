import pygame

from . import (
    folder,
    settings,
    weapon
)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites, create_weapon, destroy_weapon):
        super().__init__(groups)
        self.image = pygame.image.load(settings.GRAPHICS_ROOT / 'test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)

        self.load_player_assets()
        self.status = 'down'
        self.frame_index = 0
        self.animation_speed = 0.15

        # movement
        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None

        self.obstacle_sprites = obstacle_sprites

        # weapon
        self.weapon_index = 0
        self.weapon = list(weapon.WEAPON_DATA.keys())[self.weapon_index]
        self.create_weapon = create_weapon
        self.destroy_weapon = destroy_weapon

    def load_player_assets(self):
        character_path = settings.GRAPHICS_ROOT / 'player'
        self.animations = {}
        for movement_type in [
            'down',
            'down_attack',
            'down_idle',
            'left',
            'left_attack',
            'left_idle',
            'right',
            'right_attack',
            'right_idle',
            'up',
            'up_attack',
            'up_idle',
            ]:
            self.animations[movement_type] = folder.img_folder_to_surfaces(character_path / movement_type)

    def input(self):
        if self.attacking:
            # don't accept input during attack
            return

        keys = pygame.key.get_pressed()

        # ---- movement --------------------
        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.status = 'up'
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.status = 'down'
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.status = 'right'
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = 'left'
        else:
            self.direction.x = 0

        # ---- attack --------------------
        if keys[pygame.K_SPACE]:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            self.create_weapon()

        # ---- magic --------------------
        if keys[pygame.K_LCTRL]:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()

    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            if not self.status.endswith('_idle') and not self.status.endswith('_attack'):
                self.status = f'{self.status}_idle'

        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not self.status.endswith('_attack'):
                if self.status.endswith('_idle'):
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status = f'{self.status}_attack'
        else:
            if self.status.endswith('_attack'):
                self.status = self.status.replace('_attack', '')

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        if direction == 'horizontal':
            for obstacle_sprite in self.obstacle_sprites:
                if obstacle_sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:  # moving right
                        self.hitbox.right = obstacle_sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = obstacle_sprite.hitbox.right

        if direction == 'vertical':
            for obstacle_sprite in self.obstacle_sprites:
                if obstacle_sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:  # moving down
                        self.hitbox.bottom = obstacle_sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = obstacle_sprite.hitbox.bottom

    def cooldown(self):
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
                self.destroy_weapon()

    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def update(self):
        self.input()
        self.cooldown()
        self.get_status()
        self.animate()
        self.move(self.speed)
