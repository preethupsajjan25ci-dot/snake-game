import pygame
import random
import math

pygame.init()

# ================= WINDOW =================
WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Nokia Snake")

# ================= COLORS =================
BACKGROUND = (12, 18, 16)
GAME_AREA = (8, 35, 25)
BORDER = (80, 255, 140)
GRID_COLOR = (18, 60, 42)

SNAKE_COLOR = (45, 210, 95)
SNAKE_HEAD = (100, 255, 155)
GLOW_COLOR = (25, 110, 60)

FOOD_COLOR = (255, 55, 55)
FOOD_DARK = (190, 25, 25)
LEAF_COLOR = (70, 190, 90)

TEXT_COLOR = (240, 255, 245)
GAME_OVER_COLOR = (255, 70, 70)
PAUSE_COLOR = (255, 220, 80)
NEW_BEST_COLOR = (80, 255, 150)

EYE_COLOR = (255, 255, 255)

# ================= FONTS =================
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 70)
title_font = pygame.font.Font(None, 90)

# ================= GAME AREA =================
game_rect = pygame.Rect(40, 80, 720, 480)

CELL_SIZE = 20


# ================= FOOD =================
def create_food(snake):
    while True:
        food = [
            random.randrange(
                game_rect.left,
                game_rect.right,
                CELL_SIZE
            ),
            random.randrange(
                game_rect.top,
                game_rect.bottom,
                CELL_SIZE
            )
        ]

        if food not in snake:
            return food


# ================= RESET GAME =================
def reset_game():
    snake = [
        [200, 200],
        [180, 200],
        [160, 200]
    ]

    direction = [CELL_SIZE, 0]

    food = create_food(snake)

    score = 0

    return snake, direction, food, score


# ================= PARTICLES =================
particles = []


def create_particles(x, y):
    for _ in range(30):
        particles.append({
            "x": x,
            "y": y,
            "dx": random.uniform(-4, 4),
            "dy": random.uniform(-4, 4),
            "life": random.randint(20, 40)
        })


def update_particles():
    for particle in particles[:]:

        particle["x"] += particle["dx"]
        particle["y"] += particle["dy"]

        particle["life"] -= 1

        if particle["life"] <= 0:
            particles.remove(particle)


def draw_particles():

    for particle in particles:

        radius = max(1, particle["life"] // 7)

        pygame.draw.circle(
            screen,
            (120, 255, 160),
            (
                int(particle["x"]),
                int(particle["y"])
            ),
            radius
        )


# ================= INITIAL GAME STATE =================
snake, direction, food, score = reset_game()

high_score = 0

clock = pygame.time.Clock()

running = True

game_started = False
game_over = False
paused = False

animation_time = 0

score_effect = 0
crash_flash = 0


# ================= MAIN LOOP =================
while running:

    # ================= EVENTS =================
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            # ================= START SCREEN =================
            if not game_started:

                if event.key == pygame.K_RETURN:

                    snake, direction, food, score = reset_game()

                    particles.clear()

                    game_started = True
                    game_over = False
                    paused = False

            # ================= GAME OVER =================
            elif game_over:

                if event.key == pygame.K_r:

                    snake, direction, food, score = reset_game()

                    particles.clear()

                    game_over = False
                    paused = False
                    crash_flash = 0

                elif event.key == pygame.K_q:

                    running = False

            # ================= ACTIVE GAME =================
            else:

                # Pause
                if event.key == pygame.K_p:

                    paused = not paused

                # Movement
                if not paused:

                    # UP
                    if event.key == pygame.K_UP:

                        if direction != [0, CELL_SIZE]:

                            direction = [
                                0,
                                -CELL_SIZE
                            ]

                    # DOWN
                    elif event.key == pygame.K_DOWN:

                        if direction != [0, -CELL_SIZE]:

                            direction = [
                                0,
                                CELL_SIZE
                            ]

                    # LEFT
                    elif event.key == pygame.K_LEFT:

                        if direction != [CELL_SIZE, 0]:

                            direction = [
                                -CELL_SIZE,
                                0
                            ]

                    # RIGHT
                    elif event.key == pygame.K_RIGHT:

                        if direction != [-CELL_SIZE, 0]:

                            direction = [
                                CELL_SIZE,
                                0
                            ]

    # ================= GAME UPDATE =================
    if game_started and not game_over and not paused:

        new_head = [
            snake[0][0] + direction[0],
            snake[0][1] + direction[1]
        ]

        snake.insert(0, new_head)

        # ================= WALL COLLISION =================
        if (
            snake[0][0] < game_rect.left
            or snake[0][0] >= game_rect.right
            or snake[0][1] < game_rect.top
            or snake[0][1] >= game_rect.bottom
        ):

            game_over = True
            crash_flash = 12

        # ================= SELF COLLISION =================
        if snake[0] in snake[1:]:

            game_over = True
            crash_flash = 12

        # ================= FOOD =================
        if not game_over and snake[0] == food:

            score += 1

            # High score
            if score > high_score:

                high_score = score

            # Particle explosion
            create_particles(
                food[0] + CELL_SIZE // 2,
                food[1] + CELL_SIZE // 2
            )

            score_effect = 15

            # New food
            food = create_food(snake)

        else:

            if not game_over:

                snake.pop()

    # ================= ANIMATION =================
    animation_time += 1

    update_particles()

    if score_effect > 0:

        score_effect -= 1

    if crash_flash > 0:

        crash_flash -= 1

    # ================= START SCREEN =================
    if not game_started:

        screen.fill(BACKGROUND)

        # Title
        title = title_font.render(
            "NOKIA SNAKE",
            True,
            BORDER
        )

        screen.blit(
            title,
            (
                WIDTH // 2 - title.get_width() // 2,
                160
            )
        )

        # Subtitle
        subtitle = font.render(
            "THE CLASSIC RETURNS",
            True,
            TEXT_COLOR
        )

        screen.blit(
            subtitle,
            (
                WIDTH // 2 - subtitle.get_width() // 2,
                270
            )
        )

        # Start
        start_text = font.render(
            "PRESS ENTER TO START",
            True,
            NEW_BEST_COLOR
        )

        screen.blit(
            start_text,
            (
                WIDTH // 2 - start_text.get_width() // 2,
                350
            )
        )

        # Controls
        controls = font.render(
            "ARROW KEYS TO MOVE",
            True,
            TEXT_COLOR
        )

        screen.blit(
            controls,
            (
                WIDTH // 2 - controls.get_width() // 2,
                400
            )
        )

    # ================= GAME SCREEN =================
    else:

        screen.fill(BACKGROUND)

        # ================= SCORE =================
        score_size = 36

        if score_effect > 0:

            score_size = 42

        score_font = pygame.font.Font(
            None,
            score_size
        )

        score_text = score_font.render(
            f"Score: {score}",
            True,
            TEXT_COLOR
        )

        screen.blit(
            score_text,
            (40, 30)
        )

        # ================= HIGH SCORE =================
        best_text = font.render(
            f"Best: {high_score}",
            True,
            TEXT_COLOR
        )

        screen.blit(
            best_text,
            (600, 30)
        )

        # ================= GAME AREA =================
        pygame.draw.rect(
            screen,
            GAME_AREA,
            game_rect
        )

        # ================= GRID =================
        for x in range(
            game_rect.left,
            game_rect.right,
            CELL_SIZE
        ):

            pygame.draw.line(
                screen,
                GRID_COLOR,
                (x, game_rect.top),
                (x, game_rect.bottom)
            )

        for y in range(
            game_rect.top,
            game_rect.bottom,
            CELL_SIZE
        ):

            pygame.draw.line(
                screen,
                GRID_COLOR,
                (game_rect.left, y),
                (game_rect.right, y)
            )

        # ================= BORDER =================
        pygame.draw.rect(
            screen,
            BORDER,
            game_rect,
            4
        )

        # ================= FOOD =================
        if not game_over:

            pulse = math.sin(
                animation_time * 0.12
            ) * 2

            radius = int(
                9 + pulse
            )

            center = (
                food[0] + 10,
                food[1] + 11
            )

            # Glow
            pygame.draw.circle(
                screen,
                (100, 30, 30),
                center,
                radius + 5
            )

            # Dark outer apple
            pygame.draw.circle(
                screen,
                FOOD_DARK,
                center,
                radius + 2
            )

            # Apple
            pygame.draw.circle(
                screen,
                FOOD_COLOR,
                center,
                radius
            )

            # Leaf
            pygame.draw.ellipse(
                screen,
                LEAF_COLOR,
                (
                    food[0] + 10,
                    food[1] - 3,
                    10,
                    6
                )
            )

        # ================= SNAKE =================
        for i, segment in enumerate(snake):

            x = segment[0]
            y = segment[1]

            # Glow
            glow_rect = pygame.Rect(
                x - 3,
                y - 3,
                CELL_SIZE + 6,
                CELL_SIZE + 6
            )

            pygame.draw.rect(
                screen,
                GLOW_COLOR,
                glow_rect,
                border_radius=8
            )

            # Head
            if i == 0:

                pygame.draw.rect(
                    screen,
                    SNAKE_HEAD,
                    (
                        x,
                        y,
                        CELL_SIZE,
                        CELL_SIZE
                    ),
                    border_radius=7
                )

                # Eyes based on direction
                if direction == [CELL_SIZE, 0]:

                    eyes = [
                        (x + 14, y + 5),
                        (x + 14, y + 15)
                    ]

                elif direction == [-CELL_SIZE, 0]:

                    eyes = [
                        (x + 6, y + 5),
                        (x + 6, y + 15)
                    ]

                elif direction == [0, -CELL_SIZE]:

                    eyes = [
                        (x + 5, y + 6),
                        (x + 15, y + 6)
                    ]

                else:

                    eyes = [
                        (x + 5, y + 14),
                        (x + 15, y + 14)
                    ]

                for eye in eyes:

                    pygame.draw.circle(
                        screen,
                        EYE_COLOR,
                        eye,
                        3
                    )

                    pygame.draw.circle(
                        screen,
                        (0, 0, 0),
                        eye,
                        1
                    )

            # Body
            else:

                pygame.draw.rect(
                    screen,
                    SNAKE_COLOR,
                    (
                        x,
                        y,
                        CELL_SIZE,
                        CELL_SIZE
                    ),
                    border_radius=6
                )

        # ================= PARTICLES =================
        draw_particles()

        # ================= PAUSE =================
        if paused and not game_over:

            overlay = pygame.Surface(
                (WIDTH, HEIGHT)
            )

            overlay.set_alpha(160)

            overlay.fill(
                (0, 0, 0)
            )

            screen.blit(
                overlay,
                (0, 0)
            )

            pause_text = big_font.render(
                "PAUSED",
                True,
                PAUSE_COLOR
            )

            continue_text = font.render(
                "Press P to Continue",
                True,
                TEXT_COLOR
            )

            screen.blit(
                pause_text,
                (
                    WIDTH // 2
                    - pause_text.get_width() // 2,
                    220
                )
            )

            screen.blit(
                continue_text,
                (
                    WIDTH // 2
                    - continue_text.get_width() // 2,
                    310
                )
            )

        # ================= GAME OVER =================
        if game_over:

            overlay = pygame.Surface(
                (WIDTH, HEIGHT)
            )

            overlay.set_alpha(190)

            overlay.fill(
                (0, 0, 0)
            )

            screen.blit(
                overlay,
                (0, 0)
            )

            game_over_text = big_font.render(
                "GAME OVER",
                True,
                GAME_OVER_COLOR
            )

            final_score = font.render(
                f"Score: {score}",
                True,
                TEXT_COLOR
            )

            best_score = font.render(
                f"Best: {high_score}",
                True,
                TEXT_COLOR
            )

            retry_text = font.render(
                "Press R to Retry",
                True,
                TEXT_COLOR
            )

            quit_text = font.render(
                "Press Q to Quit",
                True,
                TEXT_COLOR
            )

            screen.blit(
                game_over_text,
                (
                    WIDTH // 2
                    - game_over_text.get_width() // 2,
                    170
                )
            )

            screen.blit(
                final_score,
                (
                    WIDTH // 2
                    - final_score.get_width() // 2,
                    270
                )
            )

            screen.blit(
                best_score,
                (
                    WIDTH // 2
                    - best_score.get_width() // 2,
                    310
                )
            )

            screen.blit(
                retry_text,
                (
                    WIDTH // 2
                    - retry_text.get_width() // 2,
                    370
                )
            )

            screen.blit(
                quit_text,
                (
                    WIDTH // 2
                    - quit_text.get_width() // 2,
                    410
                )
            )

            # New high score
            if score == high_score and score > 0:

                new_best = font.render(
                    "NEW HIGH SCORE!",
                    True,
                    NEW_BEST_COLOR
                )

                screen.blit(
                    new_best,
                    (
                        WIDTH // 2
                        - new_best.get_width() // 2,
                        450
                    )
                )

    # ================= CRASH FLASH =================
    if crash_flash > 0:

        flash = pygame.Surface(
            (WIDTH, HEIGHT)
        )

        flash.set_alpha(
            crash_flash * 10
        )

        flash.fill(
            (255, 50, 50)
        )

        screen.blit(
            flash,
            (0, 0)
        )

    # ================= DISPLAY =================
    pygame.display.update()

    # ================= SPEED =================
    speed = 6 + score // 5

    clock.tick(speed)


# ================= QUIT =================
pygame.quit()