from random import randrange
from pygame.locals import *
import pygame as pg


pg.init()

DIMENSIONS = 600
WINDOW = pg.display.set_mode([DIMENSIONS] * 2)
pg.display.set_caption("Snake")
fpsClock = pg.time.Clock()

TILESIZE = 25
RANGE = (TILESIZE//2, DIMENSIONS - TILESIZE//2, TILESIZE)
get_random_pos = lambda: [randrange(*RANGE), randrange(*RANGE)]



def draw(body, food):
    WINDOW.fill("black")

    pg.draw.rect(WINDOW, "red", food)
    length = len(body)
    [pg.draw.rect(WINDOW, (0, 255//(length-i), 0), part) for i, part in enumerate(body)]
    
    pg.display.update()


# makes sure food doesn't spawn on top of the snake's head
def validate_food_spawn(snake):
    pos = get_random_pos()
    while snake.center == pos:
        pos = get_random_pos()
    return pos


def main():
    snake = pg.Rect(0, 0, TILESIZE - 2, TILESIZE - 2)
    snake.center = get_random_pos()
    snake_dir = (0, 0)
    length = 1
    body = [snake.copy()]
    time, time_step = 0, 110

    food = snake.copy()
    food.center = validate_food_spawn(snake)

    key_dict = {K_UP: 1, K_DOWN: 1, K_RIGHT: 1, K_LEFT: 1}


    while True:

        for event in pg.event.get():
            if event.type == QUIT:
                quit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    quit()
                if event.key == K_UP and key_dict[event.key]:
                    key_dict = {K_UP: 1, K_DOWN: 0, K_RIGHT: 1, K_LEFT: 1}
                    snake_dir = (0, -TILESIZE)
                if event.key == K_DOWN and key_dict[event.key]:
                    key_dict = {K_UP: 0, K_DOWN: 1, K_RIGHT: 1, K_LEFT: 1}
                    snake_dir = (0, TILESIZE)
                if event.key == K_RIGHT and key_dict[event.key]:
                    key_dict = {K_UP: 1, K_DOWN: 1, K_RIGHT: 1, K_LEFT: 0}
                    snake_dir = (TILESIZE, 0)
                if event.key == K_LEFT and key_dict[event.key]:
                    key_dict = {K_UP: 1, K_DOWN: 1, K_RIGHT: 0, K_LEFT: 1}
                    snake_dir = (-TILESIZE, 0)

        time_now = pg.time.get_ticks()
        if time_now - time > time_step:
            time = time_now
            snake.move_ip(snake_dir)
            body.append(snake.copy())
            body = body[-length:]

        # check for border and body collision
        self_eating = pg.Rect.collidelist(snake, body[:-1]) != -1
        if (snake.left < 0) or (snake.right > DIMENSIONS) or (snake.top < 0) or (snake.bottom > DIMENSIONS) or self_eating:
            snake.center, food.center = get_random_pos(), validate_food_spawn(snake)
            length, snake_dir = 1, (0, 0)
            body = [snake.copy()]

        # respawn food when eaten
        if food.center == snake.center:
            food.center = validate_food_spawn(snake)
            length += 1

        draw(body, food)
        fpsClock.tick(60)



if __name__ == "__main__":
    main()