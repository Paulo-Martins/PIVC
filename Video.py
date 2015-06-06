# Import the parts we need from SimpleCV
from SimpleCV import Camera, VideoStream, Display

# This import is just to create the video (if you want to do something meanwhile)
from multiprocessing import Process

# To give the correct name to the output file
import time

# Imports to treat command line arguments
import sys
import getopt

def main(cameraNumber, camWidth, camHeight, outputFile):
    BUFFER_NAME = 'buffer.avi'

    # create the video stream for saving the video file
    vs = VideoStream(fps=24, filename=BUFFER_NAME, framefill=True)
    
    # create a display with size (width, height)
    disp = Display((camWidth, camHeight))
    
    # Initialize Camera
    cam = Camera(cameraNumber, prop_set={"width": camWidth, "height": camHeight})
    
    # while the user does not press 'esc'
    while disp.isNotDone():
        # KISS: just get the image... don't get fancy
        img = cam.getImage()
        
        # write the frame to videostream
        vs.writeFrame(img)
        
        # show the image on the display
        img.save(disp)
    
    # Finished the acquisition of images now Transform into a film
    makefilmProcess = Process(self.saveFilmToDisk, args=(BUFFER_NAME, outputFile))
    makefilmProcess.start()


    def saveFilmToDisk(self, bufferName, outname):
        # construct the encoding arguments
        params = " -i {0} -c:v mpeg4 -b:v 700k -r 24 {1}".format(bufferName, outname)
        
        # run avconv to compress the video since ffmpeg is deprecated (going to be).
        call('avconv'+params, shell=True)


if __name__ == '__main__':
    camNR = 1
    width = 640
    height = 480
    outname = 'output_{0}.mp4'.format(time.ctime().replace(" ", "_"))
    
#    try:
#        opts, args = getopt.getopt(argv,"hx:y:o:c:",["width=","height=", "output="])
#    except getopt.GetoptError:
#        print HELP_MSG
#        sys.exit(2)

    # Get the specified command line arguments
#    for opt, arg in opts:
#        if opt == '-h':
#            print HELP_MSG
#            sys.exit()
#        elif opt in ("-x", "--width"):
#            width = arg
#        elif opt in ("-y", "--height"):
#            height = arg
#        elif opt in ("-c"):
#            camNR = arg
#        elif opt in ("-o", "--output"):
#            outname = arg

# Finally let's start
main(camNR, width, height, outname)