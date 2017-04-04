"""
Resize all pictures (with picExt) in a tree of directories, or
resize all pictures in a directory, or
just resize 1 picture.

Default size is to resize to (784, 536) which generally
corresponds to a .2.jpg.

@author Alex Li
@version 0.1
@date 2003-03-04
"""

# python imports
import os, sys, getopt

# PIL imports
from PIL import Image


class Resizer:
    """
    Sample Usage:
    Resizer().resize("/folde/contains/photos/")
    """

    OUT_EXT = ".2.jpg"
    IN_EXT = ".3.jpg"    

    def _isPhoto(self, filename):
        """Returns boolean to see if the file here should be resize.

        Use IN_EXT to determine.
        """
        return filename[0-len(self.IN_EXT):].lower() == self.IN_EXT.lower()

    def _fullpath(self, filename):
        """Returns the full path of a file (dirname plus basename).

        filename -- just the filename, without path info (no dirname)
        """
        return os.path.abspath(os.path.join(self._folder, filename))  

    def resize(self, file, isRecursive=0, resizeTo=None):
        """Resizes photos.  This is the main method."""
        self._folder = file
        self._resizeTo = resizeTo

        if isRecursive:
            os.path.walk(self._folder, self._resizePhotos, None)
        elif os.path.isdir(self._folder):
            self._resizePhotos(None, self._folder, os.listdir(self._folder))
        else: #must be a file
            self._resizeAPhoto(self._folder)
        
    def _resizePhotos(self, dummy, folder, files):
        "Resize the pictures in the given list of files."
        self._folder = folder
        [self._resizeAPhoto(self._fullpath(file)) for file in files
         if self._isPhoto(file)]    

    def _resizeAPhoto(self, infile):
        """Resizes the picture."""
        try:
            outfile = infile[:len(infile)-len(self.IN_EXT)] + self.OUT_EXT
            im = Image.open(infile)
            (x, y) = im.size

            if self._resizeTo:
                finalSize = self._resizeTo
            elif x > y: #landscape
                finalSize = (784, y * (784.0 / x)) #x is the longer side
            else: finalSize = (x * (784.0 / y), 784) #portrait, y longer side
            
            im.resize(finalSize, Image.BICUBIC).save(outfile, "JPEG")
            print "resized photo <%s>" % infile
        except IOError:
            print "cannot resize <%s>" % infile


def run(argv):
    """The main control."""
    (folder, isRecursive, resizeTo) = getOpts(argv)
    Resizer().resize(folder, isRecursive, resizeTo)

def getOpts(argv):
    """Gets command line options and arguments."""
    isRecursive = 0
    resizeTo = ()
    try:
        opts, args = getopt.getopt(argv,
                                   "hrs:",
                                   ["help", "recursive", "size"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
        
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        if o in ("-r", "--recursive"):
            isRecursive = 1
        if o in ("-s", "--size="):
            resizeTo = (int(a.split(",")[0].strip()),
                        int(a.split(",")[1].strip()))

    if len(args) < 1:
        usage()
        sys.exit(2)
    else:
        folder = args[0]       
    return (folder, isRecursive, resizeTo)

def usage():
    """Print usage message."""
    print """
Usage: resize [OPTION] file
Resize pictures with extension ".3.jpg" to a new set of pictures
with extension ".2.jpg"

    -h, --help              display this message
    -r, --recursive         use file as the root folder and recursively
                            resize pictures
    -s, --size width,height use the size stated here as the size to resize to.
                            Default is 784,536
"""    


#Add this to album???
#3 -- ?, ?
#2 -- 784, 536
#Find out what is nearest, bilinear, bicubic
if __name__ == "__main__":
    run(sys.argv[1:])

