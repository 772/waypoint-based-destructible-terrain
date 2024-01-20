"""
Project name: waypoint_based_destructible_terrain
Author: Armin Schäfer
Requirements: ```pip install pygame```
"""

# Standard libraries.
import math
import random
from enum import Enum, auto

# Third party libraries.
import pygame

# Constants.
WINDOW_SIZE = (1000, 800)
SKY_COLOR = (215, 212, 255)
EARTH_COLOR = (200, 130, 110)
TUNNEL_COLOR = (100, 30, 10)
SPEED_WALKING = 3
SPEED_DIGGING = 1
SPEED_JUMPING = 8
BUTTON_X = 10
BUTTON_Y = 10
BUTTON_WDT = 270
BUTTON_HGT = 40
TUNNEL_HGT = 40
PLAYER_HGT = 20

# Variables that change over time.
pygame.init()
pygame.display.set_caption("waypoint based destructible terrain")
screen = pygame.display.set_mode(WINDOW_SIZE)
running = True
clock = pygame.time.Clock()
tunnels = []
players = []


class DirectionDigging(Enum):
    LEFT_UP = auto()
    LEFT = auto()
    LEFT_DOWN = auto()
    RIGHT_DOWN = auto()
    RIGHT = auto()
    RIGHT_UP = auto()


class Action(Enum):
    FALLING = auto()
    WALKING = auto()
    DIGGING = auto()


class Direction(Enum):
    LEFT = auto()
    RIGHT = auto()

class PlayerType(Enum):
    HUMAN = auto()
    AI = auto()

class Player:
    action: Action
    direction: Direction
    x: float
    y: float
    x_speed: float
    y_speed: float
    player_type: PlayerType

    def __init__(self, x, y, player_type):
        self.action = Action.FALLING
        self.direction = Direction.LEFT
        self.x = x
        self.y = y
        self.x_speed = 0
        self.y_speed = 0
        self.player_type = player_type

    def command_jump_left(self):
        self.direction = Direction.LEFT
        self.action = Action.FALLING
        self.x_speed = -SPEED_WALKING
        self.y_speed = -SPEED_JUMPING

    def command_jump_right(self):
        self.direction = Direction.RIGHT
        self.action = Action.FALLING
        self.x_speed = SPEED_WALKING
        self.y_speed = -SPEED_JUMPING

    def command_walk_left(self):
        self.direction = Direction.LEFT
        self.x_speed = -SPEED_WALKING

    def command_walk_right(self):
        self.direction = Direction.RIGHT
        self.x_speed = SPEED_WALKING

    def command_stop(self):
        self.x_speed = 0

    def is_there_solid_material(self, x, y) -> bool:
        return tuple(pygame.Surface.get_at(screen, (self.x + x, self.y + y))[:3]) in [
            EARTH_COLOR
        ]


class Tunnel:
    start_x: float
    start_y: float
    end_x: float
    end_y: float
    # direction: DirectionDigging

    def __init__(self, start_x, start_y, end_x, end_y):
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y


tunnels.append(Tunnel(200, 200, 400, 400))
tunnels.append(Tunnel(400, 200, 200, 400))

players.append(Player(100,100, PlayerType.HUMAN))
players.append(Player(200,100, PlayerType.AI))
players.append(Player(300,100, PlayerType.AI))
players.append(Player(400,100, PlayerType.AI))
debug_mode = False
smallfont = pygame.font.SysFont("Corbel", 35)
text = smallfont.render("Turn on debug mode", True, (0, 0, 0))

while running:
    # Limit the game to 36 FPS.
    clock.tick(36)

    # Mouse events.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            if (
                BUTTON_X <= mouse[0] <= BUTTON_X + BUTTON_WDT
                and BUTTON_Y <= mouse[1] <= BUTTON_Y + BUTTON_HGT
            ):
                debug_mode = not debug_mode
                if debug_mode:
                    text = smallfont.render("Turn off debug mode", True, (0, 0, 0))
                else:
                    text = smallfont.render("Turn on debug mode", True, (0, 0, 0))

    # Apply movement to all players.
    for player in players:
        # Apply speed if there are no walls.
        if player.x_speed > 0:
            if player.is_there_solid_material(7, 0) and player.is_there_solid_material(
                7, -20
            ):
                player.x_speed = 0
            else:
                player.x += player.x_speed
        elif player.x_speed < 0:
            if player.is_there_solid_material(-7, 0) and player.is_there_solid_material(
                -7, -20
            ):
                player.x_speed = 0
            else:
                player.x += player.x_speed
        player.y += player.y_speed
        # The player should not leave the screen.
        if player.x < 10:
            player.x = 10
        elif player.x >= WINDOW_SIZE[0] - 10:
            player.x = WINDOW_SIZE[0] - 11
        if player.y < 0:
            player.y = 0
        elif player.y >= WINDOW_SIZE[1]:
            player.y = WINDOW_SIZE[1] - 1
        # Is the player falling?
        if player.action == Action.FALLING:
            # Gravitation.
            if player.y_speed < 10:
                player.y_speed += 1
            # Hit the ground?
            if player.y_speed > 0 and player.is_there_solid_material(0, 1):
                player.x_speed = 0
                player.y_speed = 0
                player.action = Action.WALKING
            # Hit the ceiling with the head?
            if player.y_speed < 0 and (
                player.is_there_solid_material(-5, -PLAYER_HGT)
                or player.is_there_solid_material(5, -PLAYER_HGT)
            ):
                player.x_speed = 0
                player.y_speed = 0

        if player.player_type == PlayerType.HUMAN:
            # Keyboard input for player 1.
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and player.action == Action.DIGGING:
                    player.x_speed = -SPEED_DIGGING
                if event.key == pygame.K_LEFT and player.action == Action.WALKING:
                    player.command_walk_left()
                if event.key == pygame.K_RIGHT and player.action == Action.DIGGING:
                    player.x_speed = SPEED_DIGGING
                if event.key == pygame.K_RIGHT and player.action == Action.WALKING:
                    player.command_walk_right()
                elif event.key == pygame.K_UP and player.action == Action.WALKING:
                    if player.direction == Direction.LEFT:
                        player.command_jump_left()
                    else:
                        player.command_jump_right()
            if event.type == pygame.KEYUP:
                if (
                    event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT
                ) and player.action == Action.WALKING:
                    player.command_stop()
            if player.action == Action.WALKING:
                a = False
                if player.x_speed != 0:
                    if not player.is_there_solid_material(0, 1):
                        player.y += 1
                        if not player.is_there_solid_material(0, 1):
                            player.y += 1
                            if not player.is_there_solid_material(0, 1):
                                player.y += 1
                                if not player.is_there_solid_material(0, 1):
                                    player.action = Action.FALLING
                        a = True
                    while (
                        player.is_there_solid_material(-5, -2)
                        or player.is_there_solid_material(5, -2)
                    ) and a == False:
                        player.y -= 1
        if player.player_type == PlayerType.AI:
            # Movement for AI players. This is only for testing the movements.
            if random.randint(0,100) == 0:
                player.command_walk_right()
            elif random.randint(0,100) == 0:
                player.command_walk_left()
            elif random.randint(0,50) == 0:
                player.command_stop()

    # Draw earth.
    pygame.draw.rect(screen, EARTH_COLOR, (0, 200, WINDOW_SIZE[0], 600))

    # Draw tunnels.
    for tunnel in tunnels:
        pygame.draw.line(
            screen,
            TUNNEL_COLOR,
            (tunnel.start_x, tunnel.start_y - TUNNEL_HGT / 2),
            (tunnel.end_x, tunnel.end_y - TUNNEL_HGT / 2),
            width=TUNNEL_HGT,
        )
        pygame.draw.circle(
            screen,
            TUNNEL_COLOR,
            (tunnel.end_x, tunnel.end_y - TUNNEL_HGT / 2),
            TUNNEL_HGT / 2,
        )
        if debug_mode:
            pygame.draw.circle(
                screen,
                (255, 255, 255),
                (tunnel.end_x, tunnel.end_y - TUNNEL_HGT / 2),
                3,
            )

    # Draw the sky.
    pygame.draw.rect(screen, SKY_COLOR, (0, 0, WINDOW_SIZE[0], 200))

    # Button for debug mode.
    pygame.draw.rect(screen, (0, 0, 0), (BUTTON_X, BUTTON_Y, BUTTON_WDT, BUTTON_HGT))
    pygame.draw.rect(
        screen,
        (255, 255, 255),
        (BUTTON_X + 1, BUTTON_Y + 1, BUTTON_WDT - 2, BUTTON_HGT - 2),
    )
    screen.blit(text, (BUTTON_X + 10, BUTTON_Y + 10))

    # Draw player.
    player_color = (255, 0, 0)
    for player in players:
        if player.action == Action.DIGGING:
            player_color = (255, 255, 0)
        pygame.draw.polygon(
            screen,
            player_color,
            (
                (player.x + 3, player.y),
                (player.x + 2, player.y - 18),
                (player.x - 2, player.y - 18),
                (player.x - 3, player.y),
                (player.x - 5, player.y - 20),
                (player.x + 5, player.y - 20),
            ),
            0,
        )

    # Update the display.
    pygame.display.update()

pygame.quit()
