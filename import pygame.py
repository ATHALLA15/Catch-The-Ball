
import pygame
import random
import os

# ---------- 1. INITIALIZATION ----------

pygame.init()
pygame.mixer.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge & Collect")

clock = pygame.time.Clock()


# ---------- 2. COLORS ----------

WHITE = (255, 255, 255)
YELLOW = (255, 210, 0)
RED = (220, 40, 40)
BACKGROUND = (25, 130, 60)


# ---------- 3. LOAD SPRITE SHEET ----------

SPRITE_PATH = (
    "C:/Users/ircha/OneDrive/Desktop/coding/"
    "coding week 4/kratos_sprite_jus_by_saxcreed_df1jcep.png"
)

SPRITESHEET = pygame.image.load(SPRITE_PATH).convert_alpha()

FRAME_W = 16
FRAME_H = 24

SCALE = 3

DISPLAY_W = FRAME_W * SCALE
DISPLAY_H = FRAME_H * SCALE


# Row for each direction
DIRECTION_ROWS = {
    "down": 0,
    "left": 1,
    "right": 2,
    "up": 3
}

FRAMES_PER_ROW = 4


def get_frame(direction, frame_index):
    """Get one frame from the sprite sheet."""

    row = DIRECTION_ROWS[direction]
    col = frame_index % FRAMES_PER_ROW

    rect = pygame.Rect(
        col * FRAME_W,
        row * FRAME_H,
        FRAME_W,
        FRAME_H
    )

    frame = SPRITESHEET.subsurface(rect).copy()

    frame = pygame.transform.scale(
        frame,
        (DISPLAY_W, DISPLAY_H)
    )

    return frame


# Create all animations
ANIMATIONS = {}

for direction in DIRECTION_ROWS:
    ANIMATIONS[direction] = []

    for frame_index in range(FRAMES_PER_ROW):
        frame = get_frame(direction, frame_index)
        ANIMATIONS[direction].append(frame)


# ---------- 4. LOAD MUSIC ----------

MUSIC_PATH = (
    "C:/Users/ircha/OneDrive/Desktop/coding/"
    "coding week 4/TownTheme.mp3"
)

if os.path.exists(MUSIC_PATH):
    pygame.mixer.music.load(MUSIC_PATH)
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)


# ---------- 5. PLAYER ----------

player_x = WIDTH // 2 - DISPLAY_W // 2
player_y = HEIGHT // 2 - DISPLAY_H // 2

player_speed = 4

facing = "down"

anim_frame = 0
anim_timer = 0

ANIM_SPEED = 8


# ---------- 6. FALLING OBJECTS ----------

OBJECT_SIZE = 26
fall_speed = 4


def make_object():
    """Create a random gem or spike."""

    kind = random.choice([
        "gem",
        "gem",
        "spike"
    ])

    x = random.randint(
        0,
        WIDTH - OBJECT_SIZE
    )

    return {
        "kind": kind,
        "x": x,
        "y": -OBJECT_SIZE
    }


falling_objects = [make_object()]

spawn_timer = 0
SPAWN_INTERVAL = 45


# ---------- 7. GAME VARIABLES ----------

score = 0
game_over = False
running = True


# ---------- 8. MAIN GAME LOOP ----------

while running:

    # ---------- EVENTS ----------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            # Restart game
            if event.key == pygame.K_r and game_over:

                player_x = (
                    WIDTH // 2
                    - DISPLAY_W // 2
                )

                player_y = (
                    HEIGHT // 2
                    - DISPLAY_H // 2
                )

                falling_objects = [
                    make_object()
                ]

                score = 0
                game_over = False
                spawn_timer = 0


    # ---------- GAME UPDATE ----------

    if not game_over:

        keys = pygame.key.get_pressed()

        moving = False


        # ---------- PLAYER MOVEMENT ----------

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:

            player_x -= player_speed
            facing = "left"
            moving = True


        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:

            player_x += player_speed
            facing = "right"
            moving = True


        if keys[pygame.K_UP] or keys[pygame.K_w]:

            player_y -= player_speed
            facing = "up"
            moving = True


        if keys[pygame.K_DOWN] or keys[pygame.K_s]:

            player_y += player_speed
            facing = "down"
            moving = True


        # ---------- KEEP PLAYER ON SCREEN ----------

        player_x = max(
            0,
            min(
                WIDTH - DISPLAY_W,
                player_x
            )
        )

        player_y = max(
            0,
            min(
                HEIGHT - DISPLAY_H,
                player_y
            )
        )


        # ---------- PLAYER ANIMATION ----------

        if moving:

            anim_timer += 1

            if anim_timer >= ANIM_SPEED:

                anim_timer = 0

                anim_frame = (
                    anim_frame + 1
                ) % FRAMES_PER_ROW

        else:

            anim_frame = 0
            anim_timer = 0


        # ---------- SPAWN OBJECTS ----------

        spawn_timer += 1

        if spawn_timer >= SPAWN_INTERVAL:

            spawn_timer = 0

            falling_objects.append(
                make_object()
            )


        # ---------- MOVE OBJECTS ----------

        for obj in falling_objects:

            obj["y"] += fall_speed


        # ---------- COLLISION ----------

        player_rect = pygame.Rect(
            player_x,
            player_y,
            DISPLAY_W,
            DISPLAY_H
        )


        for obj in falling_objects[:]:

            object_rect = pygame.Rect(
                obj["x"],
                obj["y"],
                OBJECT_SIZE,
                OBJECT_SIZE
            )


            if player_rect.colliderect(object_rect):

                # Collect gem
                if obj["kind"] == "gem":

                    score += 1
                    falling_objects.remove(obj)


                # Hit spike
                elif obj["kind"] == "spike":

                    game_over = True


            # Remove object after leaving screen
            elif obj["y"] > HEIGHT:

                falling_objects.remove(obj)


    # ---------- DRAW BACKGROUND ----------

    screen.fill(BACKGROUND)


    # ---------- DRAW OBJECTS ----------

    for obj in falling_objects:

        if obj["kind"] == "gem":

            pygame.draw.circle(
                screen,
                YELLOW,
                (
                    int(
                        obj["x"]
                        + OBJECT_SIZE // 2
                    ),
                    int(
                        obj["y"]
                        + OBJECT_SIZE // 2
                    )
                ),
                OBJECT_SIZE // 2
            )

        else:

            # Spike
            points = [
                (
                    obj["x"]
                    + OBJECT_SIZE // 2,
                    obj["y"]
                ),
                (
                    obj["x"],
                    obj["y"]
                    + OBJECT_SIZE
                ),
                (
                    obj["x"]
                    + OBJECT_SIZE,
                    obj["y"]
                    + OBJECT_SIZE
                )
            ]

            pygame.draw.polygon(
                screen,
                RED,
                points
            )


    # ---------- DRAW PLAYER ----------

    player_image = ANIMATIONS[facing][anim_frame]

    screen.blit(
        player_image,
        (player_x, player_y)
    )


    # ---------- SCORE ----------

    font = pygame.font.Font(
        None,
        36
    )

    score_text = font.render(
        f"Score: {score}",
        True,
        WHITE
    )

    screen.blit(
        score_text,
        (20, 20)
    )


    # ---------- GAME OVER ----------

    if game_over:

        game_over_font = pygame.font.Font(
            None,
            72
        )

        game_over_text = game_over_font.render(
            "GAME OVER",
            True,
            WHITE
        )

        restart_text = font.render(
            "Press R to restart",
            True,
            WHITE
        )


        screen.blit(
            game_over_text,
            (
                WIDTH // 2
                - game_over_text.get_width() // 2,
                HEIGHT // 2 - 60
            )
        )


        screen.blit(
            restart_text,
            (
                WIDTH // 2
                - restart_text.get_width() // 2,
                HEIGHT // 2 + 20
            )
        )


    # ---------- UPDATE SCREEN ----------

    pygame.display.flip()

    clock.tick(60)


# ---------- QUIT ----------

pygame.quit()

