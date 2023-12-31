import pygame

from constants import Images
from templates import BaseSurface
from game import Cell
from utils import load_image


class Hero(Cell):
    IMAGE_NAME = Images.HERO

    class _ArrowVector(BaseSurface):  # Do not inherit from cell. Field.add_cells() will cause issues
        IMAGE_NAME = Images.ARROW_VECTOR

        def __init__(self, x, y, w, h, parent=None):
            super().__init__(x, y, w, h, parent=parent)

            self._angle = 0
            self._original_image = pygame.transform.scale(load_image(self.IMAGE_NAME), (w, h))
            self._image = self._original_image.copy()

        @property
        def image(self):
            return self._image.copy()

        @property
        def angle(self):
            return self._angle

        def rotate(self, angle):
            self._angle = (self._angle + angle) % 360  # Value will repeat after 359. This prevents angle to overflow.
            self._image = pygame.transform.rotate(self._original_image, self._angle)

        def draw(self):
            self.fill((255, 255, 255, 0))
            self.blit(self._image)

    def __init__(self, field, coordinates, *groups, arrowed=True):
        super().__init__(field, coordinates, *groups)
        self._arrowed = arrowed

        if self._arrowed:
            # will be moved in update (_get_arrow_vector_rect() relies on ArrowVector size)
            self._arrow_vector = self._ArrowVector(-1, -1, *self.get_size(), parent=field)

    def _get_arrow_vector_rect(self):
        return pygame.Rect(
            self.get_rect().x - (self._arrow_vector.image.get_rect().w - self._arrow_vector.get_width()) / 2,
            self.get_rect().y - self.get_rect().h / 2 - (self._arrow_vector.image.get_rect().h -
                                                         self._arrow_vector.get_height()) / 2,
            *self.get_rect().size
        )

    def update(self, *events) -> None:
        self.move(self.get_rect().x, self.get_rect().y)
        self._arrow_vector.move(*self._get_arrow_vector_rect().topleft)
        if self._arrowed:
            self._arrow_vector.rotate(1.5)

    def handle(self):
        super().handle()

        self._arrow_vector.handle()
        self._field.blit(self._arrow_vector)
