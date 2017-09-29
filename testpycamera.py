import time
import os
import pygame,sys
import pygame.camera
import pygame.display
from pygame.locals import *

pygame.init()
pygame.camera.init()

pygame.display.init()
info = pygame.display.Info()
print(info)

disp_no = os.getenv("DISPLAY")
if disp_no:
    print ("I'm running under X display = {0}".format(disp_no))


# Check which frame buffer drivers are available
# Start with fbcon since directfb hangs with composite output

drivers = ['svgalib', 'fbcon', 'directfb', 'svgalib']
found = False
for driver in drivers:
# Make sure that SDL_VIDEODRIVER is set
    if not os.getenv('SDL_VIDEODRIVER'):
        os.putenv('SDL_VIDEODRIVER', driver)
    try:
        pygame.display.init()
    except pygame.error:
        print ('Driver: {0} failed.'.format(driver))
        continue
    found = True
    print ("Using driver: {0}".format(driver))
    break
    
if not found:
    raise Exception('No suitable video driver found!')

size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
print ("Framebuffer size: %d x %d" % (size[0], size[1]))

screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

# Clear the screen to start
#screen.fill((255, 0, 0))

# Render the screen
#pygame.display.update()

#time.sleep(10)

#screen = pygame.display.set_mode([320,240], pygame.FULLSCREEN)

cam = pygame.camera.Camera("/dev/video0", (320,240))
cam.start()

while 1:
    image = cam.get_image()
    screen.blit(image,(0,0))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            sys.exit()

    time.sleep(0.05)
