import time
import os
import socket
import sys
import time
import subprocess as sub
import pygame,sys
import pygame.camera
import pygame.display
from pygame.locals import *

pygame.init()
pygame.display.init()
size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
white = (255,255,255)

def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()

def message_display(text,screen):
    largeText = pygame.font.Font('freesansbold.ttf',40)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((pygame.display.Info().current_w/2),(pygame.display.Info().current_h/2))
    screen.blit(TextSurf, TextRect)

    pygame.display.update()

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

    if not isConnected:
        continue

    countEmptyData=0

    while True:
        if sock == None:
            isConnected=False
            break

        print >>sys.stderr, '\nwaiting to receive message'
        data = sock.recv(BUFFER_SIZE)
        print >>sys.stderr, 'received %s bytes' % (len(data))
        print >>sys.stderr, data

        if len(data) == 0:
            countEmptyData = countEmptyData + 1

        if countEmptyData == 3:
            isConnected=False
            sock.close()
            break;
   

        if data and len(data) > 4:
            countEmptyData = 0
            dataArray = data.split(",@\x00")
            print dataArray
            for item in dataArray:
                dataItem = item[4:]
                ds = dataItem.split(",")
                print ds
                if len(ds) == 5: 

                    if (ds[4] == "1" and ds[0] == "On"):
                        screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
                        message_display("Taking FRONT pic!", screen)
                        bashCommand = "fswebcam -r 640x480 image-" + str(time.time()) + ".jpg -S 20"
                        os.system(bashCommand)
                        sock.shutdown(socket.SHUT_RDWR)
                        sock.close()
                        sock = None
                        pygame.display.quit()
                        break

                    if (ds[4] == "2" and ds[0] == "On"):
                        screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
                        message_display("Taking FRONT video!", screen)
                        bashCommand = "timeout 60 avconv -f video4linux2 -r 30 -s 640x480 -i /dev/video0 test" + str(time.time()) + ".avi"
                        os.system(bashCommand)
                        sock.shutdown(socket.SHUT_RDWR)
                        sock.close()
                        sock = None
                        pygame.display.quit()
                        break

                    if (ds[4] == "0" and ds[0] == "On"):
                        screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
                        message_display("Taking BACK pic!", screen)
                        while True:
                            bashCommand="sudo rmmod uvcvideo; sudo modprobe uvcvideo; fswebcam -d /dev/video1 -r 1280x720 image-r-" + str(time.time()) + " -S 20; sudo rmmod uvcvideo; sudo modprobe uvcvideo;"
                            p = sub.Popen(bashCommand, stdout=sub.PIPE, stderr=sub.PIPE, shell=True);
                            output, errors = p.communicate()
                            print "Output='" + output + "'"
                            print "Errors='" + errors + "'"

                            if errors == None or errors == "" or not errors or "Writing" in errors:
                                break

                            time.sleep(2)

                        sock.shutdown(socket.SHUT_RDWR)
                        sock.close()
                        sock = None
                        pygame.display.quit()
                        break

                    if (ds[4] == "3" and ds[0] == "On"):
                        message_display("Taking BACK video!", screen)
                        screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
                        while True:
                            bashCommand = "sudo rmmod uvcvideo; sudo modprobe uvcvideo; sudo timeout 60 avconv -f video4linux2 -r 30 -s 640x480 -i /dev/video1 test-r" + str(time.time()) + ".avi; sudo rmmod uvcvideo; sudo modprobe uvcvideo;"
                            p = sub.Popen(bashCommand, stdout=sub.PIPE, stderr=sub.PIPE, shell=True);
                            output, errors = p.communicate()
                            print "Output='" + output + "'"
                            print "Errors='" + errors + "'"

                            if errors == None or errors == "" or not errors or "frame=" in errors:
                                break
                        
                        sock.shutdown(socket.SHUT_RDWR)
                        sock.close()
                        sock = None
                        pygame.display.quit()
                        break
