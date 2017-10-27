import time
import os
import socket
import sys
import time
import pygame,sys
import pygame.camera
import pygame.display
from pygame.locals import *

pygame.init()
white = (255,255,255)
black = (0,0,0)



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

pygame.draw.line(screen, 
                 white, 
                 (0, pygame.display.Info().current_h/2), 
                 (pygame.display.Info().current_w, pygame.display.Info().current_h/2))

pygame.draw.line(screen,
                 white,
                 (pygame.display.Info().current_w/2, 0),
                 (pygame.display.Info().current_w/2, pygame.display.Info().current_h))


pygame.display.update()




def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def message_display(screen, text, cx, cy, color):
    largeText = pygame.font.Font('freesansbold.ttf',50)
    TextSurf, TextRect = text_objects(text, largeText, color)
    TextRect.center = (cx, cy)
    return screen.blit(TextSurf, TextRect)

TCP_IP = '127.0.0.1'
TCP_PORT = 12345
BUFFER_SIZE = 8192

prevText = []

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

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                pygame.display.quit()
                sock.close()
                sys.exit()

    if not isConnected:
        continue

    f = open('stats-'+str(time.time()), 'w')

    countEmptyData=0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                pygame.display.quit()
                sock.close()
                f.flush()
                f.close()
                sys.exit()

        print >>sys.stderr, '\nwaiting to receive message'
        data = sock.recv(BUFFER_SIZE)
        print >>sys.stderr, 'received %s bytes' % (len(data))
        print >>sys.stderr, data

        if len(data) == 0:
            countEmptyData = countEmptyData + 1

        if countEmptyData == 3:
            isConnected=False
            sock.close()
            f.flush()
            f.close()
            break;

        if data and len(data) > 4:
            countEmptyData = 0
            dataArray = data.split(",@\x00")
            print dataArray
            curList = []
            curUnits = []
            for item in dataArray:
                dataItem = item[4:]
                ds = dataItem.split(",")
                print ds 
                if (len(ds) == 5):
                    curList.append(ds[0]);
                    curUnits.append(ds[3]);
                    if (ds[4] == "3"):
                        f.write(curList[0] + "," + curList[1] + "," + curList[2] + "," + curList[3] + "," + str(time.time()) + "\n")
                        f.flush()

                        cw = pygame.display.Info().current_w/2
                        ch = pygame.display.Info().current_h/2

                        if len(prevText) > 0:
                            message_display(screen, prevText[0], 0+cw/2, 0+ch/2, black)
                            message_display(screen, prevText[1], cw+cw/2, 0+ch/2, black)
                            message_display(screen, prevText[2], 0+cw/2, ch+ch/2, black)
                            message_display(screen, prevText[3], cw+cw/2, ch+ch/2, black)
                            prevText = []

                        updatedRects = []

                        updatedRects.append(message_display(screen, curList[0] + " " + curUnits[0], 0+cw/2, 0+ch/2, white))
                        updatedRects.append(message_display(screen, curList[1] + " " + curUnits[1], cw+cw/2, 0+ch/2, white))
                        updatedRects.append(message_display(screen, curList[2] + " " + curUnits[2], 0+cw/2, ch+ch/2, white))
                        updatedRects.append(message_display(screen, curList[3] + " " + curUnits[3], cw+cw/2, ch+ch/2, white))

                        pygame.display.update(updatedRects)

                        prevText.append(curList[0] + " " + curUnits[0])
                        prevText.append(curList[1] + " " + curUnits[1])
                        prevText.append(curList[2] + " " + curUnits[2])
                        prevText.append(curList[3] + " " + curUnits[3])

                        curList = []


