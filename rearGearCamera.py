import time
import os
import pygame,sys
import pygame.camera
import pygame.display
from pygame.locals import *
import socket
import sys

def init():

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

    #1824 x 984
    cam = pygame.camera.Camera("/dev/video0", (640,320))
    cam.start()

    cameraActive = True
    while cameraActive:
        image = cam.get_image()
        screen.blit(image,(0,0))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                cam.stop()
                pygame.display.quit()
                cameraActive = False
                #sys.exit()

        time.sleep(0.01)

TCP_IP = '127.0.0.1'
TCP_PORT = 12345
BUFFER_SIZE = 1024

isConnected=False
while not isConnected:
    isConnected=False
    try:
        print >>sys.stderr, '\n Trying to connect to IP: %s, Port: %s' %(TCP_IP,TCP_PORT)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((TCP_IP, TCP_PORT))
        isConnected=True
    except:
        print >>sys.stderr, '\n Unable to connect!'
        isConnected=False
        time.sleep(0.5)

while True:
    print >>sys.stderr, '\nwaiting to receive message'
    data = sock.recv(BUFFER_SIZE)
    print >>sys.stderr, 'received %s bytes' % (len(data))
    print >>sys.stderr, data
    
    if data and len(data) > 4:
        data = data[4:]
        ds = data.split(",")
        print ds
        if (ds[0] == "1" or ds[0] == "On"):
            init()
