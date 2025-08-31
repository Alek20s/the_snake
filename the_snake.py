# -*- coding: utf-8 -*-

from random import randint

import pygame as pg

# Константы
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
DIRECTIONS = (UP, DOWN, LEFT, RIGHT)
INITIAL_POSITION = (0, 0)

# Цвета
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
WHITE_COLOR = (255, 255, 255)

# Скорость змейки
SPEED = 3

TRANSITIONS = {
    (pg.K_UP, LEFT): UP,
    (pg.K_UP, RIGHT): UP,
    (pg.K_DOWN, LEFT): DOWN,
    (pg.K_DOWN, RIGHT): DOWN,
    (pg.K_LEFT, UP): LEFT,
    (pg.K_LEFT, DOWN): LEFT,
    (pg.K_RIGHT, UP): RIGHT,
    (pg.K_RIGHT, DOWN): RIGHT,
}

# Включение экрана
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption('Змейка')
clock = pg.time.Clock()


class GameObject:
    """Основной класс для всех классов игры."""

    def __init__(self, body_color=WHITE_COLOR):
        """Обозначить позицию и цвет."""
        self.position = (0, 0)
        self.body_color = body_color

    def draw(self):
        """Нарисовать объект."""
        raise NotImplementedError


class Apple(GameObject):
    """Яблоко на экране."""

    def __init__(self):
        """Обозначение случайной позиции."""
        super().__init__(APPLE_COLOR)

    def randomize_position(self, occupied_positions):
        """Случайное положение яблока вне змейки."""
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
            )
            if self.position not in occupied_positions:
                break

    def draw(self):
        """Draw the apple on the board."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Контроль змейки игроком."""

    def __init__(self):
        """Вывести змейку на середину экрана."""
        super().__init__(SNAKE_COLOR)
        self.reset()
        self.direction = RIGHT
        self.next_direction = None

    def get_head_position(self):
        """Возвратить позицию головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """Обновление направлений."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Шаг вперёд змейки."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_head = (
            (head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT
        )

        self.positions.insert(0, new_head)
        if not self.grow:
            self.positions.pop()
        else:
            self.grow = False

    def reset(self):
        """Обновление позиции змейки в первоначальное положение."""
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.grow = False

    def draw(self):
        """Нарисовать змейку на экране."""
        for pos in self.positions:
            rect = pg.Rect(pos, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)


def handle_keys(snake):
    """Ручное управление змейкой клавиатурой с использованием TRANSITIONS."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            new_dir = TRANSITIONS.get((event.key, snake.direction))
            if new_dir:
                snake.next_direction = new_dir


def main():
    """Главный цикл игры."""
    pg.init()
    snake = Snake()
    apple = Apple()
    apple.randomize_position(snake.positions)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        # Проверка столкновения с самим собой
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()

        # Проверка, ест ли змея яблоко
        if snake.get_head_position() == apple.position:
            snake.grow = True
            apple.randomize_position(snake.positions)

        # Показать всё на дисплее
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
