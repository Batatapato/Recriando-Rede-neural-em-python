import pygame as pg



def blit_rotate_center(win, image, top_left, angle):
    rotated_image = pg.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(
        center=image.get_rect(topleft=top_left).center)

    win.blit(rotated_image, new_rect.topleft)