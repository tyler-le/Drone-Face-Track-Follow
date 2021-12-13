from djitellopy import tello
import time
import pygame

# Pygame window for keyboard press
pygame.init()
window = pygame.display.set_mode((400, 400))

tello = tello.Tello()
tello.connect()


def process_key(events):

    for event in events:
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_t:
                tello.takeoff()
            if event.key == pygame.K_l or event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                tello.land()
            if event.key == pygame.K_a:
                tello.move_left(30)
            if event.key == pygame.K_d:
                tello.move_right(30)
            if event.key == pygame.K_w:
                tello.move_up(30)
            if event.key == pygame.K_s:
                tello.move_down(30)
            if event.key == pygame.K_LEFT:
                tello.rotate_counter_clockwise(30)
            if event.key == pygame.K_RIGHT:
                tello.rotate_clockwise(30)
            if event.key == pygame.K_1:
                tello.flip_left()
            if event.key == pygame.K_2:
                tello.flip_right()
            if event.key == pygame.K_3:
                tello.flip_back()
            if event.key == pygame.K_4:
                tello.flip_forward()


while True:
    # Handle keyboard input to control drone
    events = pygame.event.get()
    process_key(events)
    time.sleep(0.05)

