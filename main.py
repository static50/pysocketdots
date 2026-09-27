import pygame

def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((800, 600))
    running = True

    for event in pygame.event.get():
        if event.type == event.KEYDOWN:
            if event.key == pygame.K_w:

            elif event.key == pygame.K_s:

            elif event.key == pygame.K_a:

            elif event.key == pygame.K_d:







if __name__ == "__main__":
    main()