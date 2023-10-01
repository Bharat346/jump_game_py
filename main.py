import pygame as pg

pg.init()
clock = pg.time.Clock()
backx = 0
backy = 0
score = 0
backvelo = 6
obsx = 600
obsy = 370
s_w = 800
s_h = 600
x_change = 0
x = 200
y = 410
jump = False
j_h = 15
j_count = 0
game_over = False  # Flag to indicate game over
restart_button_rect = pg.Rect(150, 300, 200, 100)  # Rect for "Play Again" button
screen = pg.display.set_mode((s_w, s_h))
pg.display.set_caption("Jumping game")
o_img = bg_img = pg.image.load("bg_img_jump.jpg")
obs1 = pg.image.load("obs1.png")
obs2 = pg.image.load("obs2.png")
obs3 = pg.image.load("obs3.png")
obs4 = pg.image.load("obs4.png")
new_size = (800, 600)
resized_image = pg.transform.scale(o_img, new_size)

# Create Rect objects for the player character and each obstacle
player_rect = pg.Rect(x - 25, y - 25, 50, 50)
obs1_rect = pg.Rect(obsx, obsy, obs1.get_width() - 20, obs1.get_height() - 20)
obs2_rect = pg.Rect(obsx + 600, obsy + 10, obs2.get_width() - 20, obs2.get_height() - 20)
obs3_rect = pg.Rect(obsx + 1600, obsy, obs3.get_width() - 20, obs3.get_height() - 20)
obs4_rect = pg.Rect(obsx + 2200, obsy - 70, obs4.get_width() - 50, obs4.get_height() - 50)

# message function
def message(size, mess, x_pos, y_pos):
    font = pg.font.SysFont(None, size)
    ren = font.render(mess, True, (230, 230, 1))
    screen.blit(ren, (x_pos, y_pos))
    pg.display.update()

running = True
restart_clicked = False  # Flag to track if "Play Again" button has been clicked

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                x_change = -10
            elif event.key == pg.K_RIGHT:
                x_change = 10
        if event.type == pg.KEYUP:
            if event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
                x_change = 0
        if event.type == pg.MOUSEBUTTONDOWN and game_over:
            # Check if the mouse click is within the "Play Again" button area
            if restart_button_rect.collidepoint(event.pos):
                game_over = False
                restart_clicked = True
                score = 0
                x = 200
                y = 410
                obsx = 600

    keys = pg.key.get_pressed()

    if keys[pg.K_SPACE] and not jump and not game_over:  
        jump = True

    # Handle jumping logic
    if jump:
        if j_h >= -15:
            neg = 1
            if j_h < 0:
                neg = -1
            y -= (j_h ** 2) * 0.5 * 0.5 * neg
            j_h -= 1

        else:
            jump = False
            j_h = 15

    x = x + x_change
    if x < 25:
        x = 25
    elif x > s_w - 25:
        x = s_w - 25

    if not game_over:
        backx -= backvelo
        obsx -= backvelo

        if backx <= -800:
            backx = 0
        if obsx < -2600:
            obsx = 800

        player_rect.x = x - 25
        player_rect.y = y - 25
        obs1_rect.x = obsx
        obs2_rect.x = obsx + 600
        obs3_rect.x = obsx + 1600
        obs4_rect.x = obsx + 2200
        message(100, f"Score: {score}", 150, 200)
        score += 1

        if player_rect.colliderect(obs1_rect) or player_rect.colliderect(obs2_rect) or player_rect.colliderect(
                obs3_rect) or player_rect.colliderect(obs4_rect):
            game_over = True

    clock.tick(60)
    screen.fill((255, 255, 255))
    screen.blit(resized_image, (backx, backy))
    screen.blit(resized_image, (backx + 800, backy))
    screen.blit(obs1, (obsx, obsy))
    screen.blit(obs2, (obsx + 600, obsy + 10))
    screen.blit(obs3, (obsx + 1600, obsy))
    screen.blit(obs4, (obsx + 2200, obsy - 70))
    pg.draw.circle(screen, (250, 140, 0), center=(x, y), radius=25.0)

    if game_over:
        pg.draw.rect(screen, (20, 200, 20), [150, 300, 200, 100])
        message(50, "Play Again", 160, 325)
        message(100, "GAME OVER", 150, 100)
        message(100, f"Score: {score}", 150, 200)
    elif restart_clicked:
        # Clear the "Play Again" button area
        pg.draw.rect(screen, (255, 255, 255), [150, 300, 200, 100])
        restart_clicked = False

    pg.display.flip()

# The game loop has ended
pg.quit()
