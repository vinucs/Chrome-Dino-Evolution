class Sprite():
    def __init__(self, x, y, max_dist):
        self.posx = x
        self.posy = y
        self.max_dist = max_dist

    def getPosition(self):
        return (self.posx, self.posy)

    def move(self, x, y):
        self.posx += x
        self.posy += y

    def setHitBox(self, hb_x, hb_y):
        self.hitbox_lenght = hb_x
        self.hitbox_height = hb_y
        self.hitbox = (self.posx, self.posy, self.hitbox_lenght + self.posx, self.posy + self.hitbox_height)

    def updateHitBox(self):
        self.hitbox = (self.posx, self.posy, self.hitbox_lenght + self.posx, self.posy + self.hitbox_height)


class Dinosaur(Sprite):
    def __init__(self, x, y, max_dist, max_acel, max_down):
        super().__init__(x, y, max_dist)
        self.grounded = True
        self.aceleration = 0
        self.max_aceleration = max_acel
        self.max_down_acel = max_down
        self.going_down = False

    def setDinoHitBox(self, hb_wx, hb_wy, hb_cx, hb_cy):
        self.hitbox_lt_walk = hb_wx
        self.hitbox_ht_walk = hb_wy
        self.hitbox_lt_crouch = hb_cx
        self.hitbox_ht_crouch = hb_cy
        self.hitbox_walk = (self.posx, self.posy, self.hitbox_lt_walk + self.posx, self.posy + self.hitbox_ht_walk)
        self.hitbox_crouch = (self.posx, self.posy + 13, self.hitbox_lt_crouch + self.posx, self.posy + 13 + self.hitbox_ht_crouch)
        self.hitbox = self.hitbox_walk
        self.hitbox_lenght = self.hitbox_lt_walk
        self.hitbox_height = self.hitbox_ht_walk

    def updateDinoHitbox(self):
        self.hitbox_walk = (self.posx, self.posy, self.hitbox_lt_walk + self.posx, self.posy + self.hitbox_ht_walk)
        self.hitbox_crouch = (self.posx, self.posy + 13, self.hitbox_lt_crouch + self.posx, self.posy + 13 + self.hitbox_ht_crouch)
        if self.state == 'j' or self.state == 'w':
            self.hitbox = self.hitbox_walk
            self.hitbox_lenght = self.hitbox_lt_walk
            self.hitbox_height = self.hitbox_ht_walk
        elif self.state == 'c':
            self.hitbox = self.hitbox_crouch
            self.hitbox_lenght = self.hitbox_lt_crouch
            self.hitbox_height = self.hitbox_ht_crouch

    def setSprites(self, walk, crouch):
        self.walk_sprite = walk
        self.crouch_sprite = crouch
        self.state = 'w'
        self.next_sprite = 0

    def getSprite(self):
        if self.state == 'w':
            return self.walk_sprite[self.next_sprite]
        elif self.state == 'c':
            return self.crouch_sprite[self.next_sprite]
        elif self.state == 'j':
            return self.walk_sprite[0]

    def updateSprite(self):
        sprite = None
        if self.state == 'w':
            if self.next_sprite >= len(self.walk_sprite):
                self.next_sprite = 0
            sprite = self.walk_sprite[self.next_sprite]
            self.next_sprite += 1
            if self.next_sprite >= len(self.walk_sprite):
                self.next_sprite = 0
        elif self.state == 'c':
            if self.next_sprite >= len(self.crouch_sprite):
                self.next_sprite = 0
            sprite = self.crouch_sprite[self.next_sprite]
            self.next_sprite += 1
            if self.next_sprite >= len(self.crouch_sprite):
                self.next_sprite = 0
        elif self.state == 'j':
            sprite = self.walk_sprite[0]
            self.next_sprite = 0
        return sprite

    def changeState(self, new_state):
        self.state = new_state
        self.next_sprite = 0

    def isJumping(self):
        if self.grounded == True:
            self.grounded = False
            self.aceleration = self.max_aceleration
            self.state = 'j'
            self.updateDinoHitbox()

    def isGrounded(self, y):
        self.grounded = True
        self.going_down = False
        self.aceleration = 0
        self.posy = y
        self.state = 'w'
        self.next_sprite = 0
        self.updateDinoHitbox()

    def isCrouch(self):
        if self.state == 'j' and self.going_down == False:
            self.aceleration = self.max_down_acel
            self.going_down = True
        if self.state == 'w':
            self.state = 'c'
            self.next_sprite = 0
            self.updateDinoHitbox()

    def isWalking(self):
        if self.state == 'c':
            self.state = 'w'
            self.next_sprite = 0
            self.updateDinoHitbox()


class Cactus(Sprite):
    def setSprites(self, sprites):
        self.sprites = sprites

    def getSprite(self):
        return self.sprites

class Bird(Sprite):
    def setSprites(self, sprites, sprite_time):
        self.sprites = sprites
        self.next_sprite = 0
        self.sprite_time = sprite_time

    def getSprite(self):
        return self.sprites[self.next_sprite]

    def updateSprite(self):
        if self.next_sprite == 0:
            self.next_sprite = 1
        else:
            self.next_sprite = 0


class Ground(Sprite):
    def setSprites(self, sprite):
        self.sprite = sprite

    def getSprite(self):
        return self.sprite

class Cloud(Sprite):
    def setSprites(self, sprite):
        self.sprite = sprite

    def getSprite(self):
        return self.sprite




