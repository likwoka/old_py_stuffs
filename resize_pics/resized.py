"""
Syntax:
    resized.py config_file

Desc:
    This program watches a folder for new and modified images. 
    Once they are found, it create a resized copy for each of 
    them and put it in the destination folder.
    
    If this program is run without given a configuration file
    as argument, it will go into interactive mode to generate
    a configuration file with answers from the user.

    Running it with -h or --help will show this screen.

Example:
    resized.py
    resized.py config_file
    resized.py --help

Requirement:
    Python 2.5+
"""

USAGE = __doc__
VERSION = "0.1"

# How long (in sec) to sleep before each scanning of folders. 
SLEEP_INTERVAL = 10

# A case-insensitive list of file extensions that we would resize.
VALID_EXTS = [".jpg", ".jpeg", ".gif"]

# The configuration file template.
CONTENT = """watch_folder = r"%(watch_folder)s"
output_folder = r"%(output_folder)s" 
# "w" or "h", size in pixel, enlarge?, shrink?
landscape_rule = ("%(landscape_side)s", %(landscape_size)s, %(landscape_enlarge)s, %(landscape_shrink)s) 
portrait_rule = ("%(portrait_side)s", %(portrait_size)s, %(portrait_enlarge)s, %(portrait_shrink)s)
square_rule = ("w", %(square_size)s, %(square_enlarge)s, %(square_shrink)s) 
"""

import os, time, shutil, sys, tempfile, traceback
from PIL import Image


def find_available_name(path):
    """Given a path, return a path that does not exist.
    Ex: /folder/file%s.txt --> /folder/file-1.txt
    
    path -- a string of the path, with a 
            %s for the pattern substutition.
    """
    pattern = "" 
    cnt = 0
    while 1:
        final_path = os.path.join(path % pattern)
        if os.path.exists(final_path):
            cnt += 1
            pattern = "-%s" % cnt
        else:
            return final_path


def generate_configfile():
    """The interactive configuration file generation 'wizard'.
    This function prompts the user for options and generate the
    configuration file.  Return the path to the configuration file.
    """
    print >> sys.stdout, "Since no configuration file is given, we will try to generate one now."
    
    while 1:
        cont = raw_input("Do you want to continue? [y | n] ")
        if cont.lower() not in ('y', 'n'):
            print >> sys.stdout, "%s is not a valid choice, please answer again!" % cont
        else:
            break

    if cont.lower() == 'n':
        sys.exit(0)
        
    watch_folder = raw_input("Please type in the full path of the folder to be watched: ")
    output_folder = raw_input("Please type in the full path of the output folder: ")
    
    while 1:
        landscape_side = raw_input("For landscape-oriented picture, do you want to resize according to height or width? [h | w] ")
        if landscape_side.lower() not in ('h', 'w'):
            print >> sys.stdout, "%s is not a valid choice, please answer again!" % landscape_side
        else:
            landscape_side = landscape_side.lower()
            break
    
    while 1:
        landscape_size = raw_input("What should the new size be (in pixel)? ")
        try:
            landscape_size = int(landscape_size)
            break
        except ValueError:
            print >> sys.stdout, "You can't express pixel in that!  Please answer again!"
    
    while 1:
        landscape_enlarge = raw_input("Should a smaller %s be enlarged to %s? [y | n] " % (landscape_side, landscape_size))
        if landscape_enlarge.lower() not in ('y', 'n'):
            print >> sys.stdout, "%s is not a valid choice, please answer again!" % landscape_enlarge
        else:
            landscape_enlarge = True if landscape_enlarge.lower() == 'y' else False
            break 
    
    while 1:
        landscape_shrink = raw_input("Should a larger %s be shrinked to %s? [y | n] " % (landscape_side, landscape_size))
        if landscape_shrink.lower() not in ('y', 'n'):
            print >> sys.stdout, "%s is not a valid choice, please answer again!" % landscape_shrink
        else:
            landscape_shrink = True if landscape_shrink.lower() == 'y' else False
            break  
    
    while 1:
        portrait_side = raw_input("For portrait-oriented picture, do you want to resize according to height or width? [h | w] ")
        if portrait_side.lower() not in ('h', 'w'):
            print >> sys.stdout, "%s is not a valid choice, please answer again!" % portrait_side
        else:
            portrait_side = portrait_side.lower()
            break  
    
    while 1:
        portrait_size = raw_input("What should the new size be (in pixel)? ")
        try:
            portrait_size = int(portrait_size)
            break
        except ValueError:
            print >> sys.stdout, "You can't express pixel in that!  Please answer again!"
    
    while 1:
        portrait_enlarge = raw_input("Should a smaller %s be enlarged to %s? [y | n] " % (portrait_side, portrait_size))
        if portrait_enlarge.lower() not in ('y', 'n'):
            print >> sys.stdout, "%s is not a valid choice, please answer again!" % portrait_enlarge
        else:
            portrait_enlarge = True if portrait_enlarge.lower() == 'y' else False
            break  
    
    while 1:
        portrait_shrink = raw_input("Should a larger %s be shrinked to %s? [y | n] " % (portrait_side, portrait_size))
        if portrait_shrink.lower() not in ('y', 'n'):
            print >> sys.stdout, "%s is not a valid choice, please answer again!" % portrait_shrink
        else:
            portrait_shrink = True if portrait_shrink.lower() == 'y' else False
            break      
    
    while 1:
        square_size = raw_input("For square sized picture now.  What should the new size be (in pixel)? ")
        try:
            square_size = int(square_size)
            break
        except ValueError:
            print >> sys.stdout, "You can't express pixel in that!  Please answer again!"
    
    while 1:
        square_enlarge = raw_input("Should a smaller size be enlarged to %s? [y | n] " % square_size)
        if square_enlarge.lower() not in ('y', 'n'):
            print >> sys.stdout, "%s is not a valid choice, please answer again!" % square_enlarge
        else:
            square_enlarge = True if square_enlarge.lower() == 'y' else False
            break  

    while 1:
        square_shrink = raw_input("Should a larger size be shrinked to %s? [y | n] " % square_size)
        if square_shrink.lower() not in ('y', 'n'):
            print >> sys.stdout, "%s is not a valid choice, please answer again!" % square_shrink
        else:
            square_shrink = True if square_shrink.lower() == 'y' else False
            break 

    temp_fd, temp_path = tempfile.mkstemp()
    f = os.fdopen(temp_fd, "w+b")
    f.write(CONTENT % (locals()))
    f.close()

    final_path = find_available_name(
            os.path.join(os.getcwd(), "resized%s.conf")
    )

    shutil.move(temp_path, final_path)
    
    time.sleep(1)
    print >> sys.stdout, "\nThe configuration has been generated in %s. " \
             "We will now run the program using that configuration file.\n" % final_path
    time.sleep(3)

    return final_path


def parse_configfile(path):
    """Parse the configuration file and return a dict of
    settings.

    path -- a string of path to the configuation file.
    """
    settings = {}
    execfile(path, settings)
    
    f = settings["watch_folder"]
    f = os.path.abspath(f)
    
    if not os.path.isdir(f):
        log_error("The watch_folder specified is not a folder!  "
                  "Please verify the configuration file and try again!",
                  timestamp=False)
        sys.exit(1)
    settings["watch_folder"] = f

    f = settings["output_folder"]
    f = os.path.abspath(f)
    
    if not os.path.exists(f):
        os.makedirs(f)
    else:
        if not os.path.isdir(f):
            log_error("The output_folder specified is not a folder! "
                      "Please verify the configuration file and try again.",
                      timestamp=False)
            sys.exit(1)
    settings["output_folder"] = f
    
    return settings

class Rule:
    """An image resize rule.  
    
    Ex: "Resize the width of this image to 450px if the 
    original widht is larger or smaller".  The 
    requirement of a rule would be expressd as the
    4 constructor arguments.  To apply the rule to 
    an image, call the resize() method to get the 
    new image size.
    """
    def __init__(self, side, resize_to, enlarge, shrink):
        """Constructor.
        
        side      -- a string of "h" or "w", meaning width or height.
        resize_to -- an int of pixel.
        enlarge   -- a boolean; should we enlarge the image to the
                     resize_to size?
        shrink    -- a boolean; should we shrink the image to the
                     resize_to size?
        """
        self.side           = side
        self.resize_to      = resize_to
        self.should_enlarge = enlarge
        self.should_shrink  = shrink

    def resize(self, x, y):
        """Resize the image and return the new size as
        a tuple of (width, height), where width and height
        are both integers.
        
        x -- an int of the current width.
        y -- an int of the current height.
        """
        # x is width, y is height
        if self.side == "w":
            diff = self.resize_to - x
            if (diff > 0 and self.should_enlarge) or \
               (diff < 0 and self.should_shrink):
                new_x, new_y = self.resize_to, int(float(y) * self.resize_to / x)
            else:
                new_x, new_y = x, y
        
        else:
            diff = self.resize_to - y
            if (diff > 0 and self.should_enlarge) or \
               (diff < 0 and self.should_shrink):
                new_x, new_y = int(float(x) * self.resize_to / y), self.resize_to
            else:
                new_x, new_y = x, y
        
        return new_x, new_y


def resize_image(image_path, output_folder,
        landscape_rule, portrait_rule, square_rule):
    """Resize an image and save it to the output folder.

    image_path     -- a string of input image path.
    output_folder  -- a string of output folder path.
    landscape_rule -- a Rule instance.
    portrait_rule  -- a Rule instance.
    square_rule    -- a Rule instance.
    """
    image = Image.open(image_path)
    (x, y) = image.size

    if x > y:   # landscape
        new_x, new_y = landscape_rule.resize(x, y)
    elif x < y: # portrait
        new_x, new_y = portrait_rule.resize(x, y)
    else:       # square
        new_x, new_y = square_rule.resize(x, y)

    filename = os.path.basename(image_path)
    new_path = os.path.join(output_folder, filename)
    try:
        image.resize((new_x, new_y), Image.ANTIALIAS).save(new_path, quality=90, optimize=1)
        log_info("Resized image %s." % filename)
    except IOError:
        log_error("Resizing image %s failed!" % filename)
        log_error(traceback.format_exc(), timestamp=False)


def log_info(msg, timestamp=True):
    """Log informational message.
    
    msg       -- a string of the message.
    timestamp -- a bool of display timestamp or not.
    """
    _log(msg, sys.stdout, timestamp)


def log_error(msg, timestamp=True):
    """Log error message.
    
    msg       -- a string of the message.
    timestamp -- a bool of display timestamp or not.
    """
    _log(msg, sys.stderr, timestamp)


def _log(msg, stream, timestamp):
    if timestamp:
        print >> stream, time.strftime("[%y%m%d %H:%M:%S]"),
    print >> stream, msg


def watch_directories (paths, func, delay=1.0):
    """(paths:[str], func:callable, delay:float)
    Continuously monitors the paths and their subdirectories
    for changes.  If any files or directories are modified,
    the callable 'func' is called with a list of the modified paths of both
    files and directories.  'func' can return a Boolean value
    for rescanning; if it returns True, the directory tree will be
    rescanned without calling func() for any found changes.
    (This is so func() can write changes into the tree and prevent itself
    from being immediately called again.)

    Authored by AMK (www.amk.ca).
    """

    # Basic principle: all_files is a dictionary mapping paths to
    # modification times.  We repeatedly crawl through the directory
    # tree rooted at 'path', doing a stat() on each file and comparing
    # the modification time.

    all_files = {}
    def f (unused, dirname, files):
        # Traversal function for directories
        for filename in files:
            path = os.path.join(dirname, filename)

            try:
                t = os.stat(path)
            except os.error:
                # If a file has been deleted between os.path.walk()
                # scanning the directory and now, we'll get an
                # os.error here.  Just ignore it -- we'll report
                # the deletion on the next pass through the main loop.
                continue

            mtime = remaining_files.get(path)
            if mtime is not None:
                # Record this file as having been seen
                del remaining_files[path]
                # File's mtime has been changed since we last looked at it.
                if t.st_mtime > mtime:
                    changed_list.append(path)
            else:
                # No recorded modification time, so it must be
                # a brand new file.
                changed_list.append(path)

            # Record current mtime of file.
            all_files[path] = t.st_mtime

    # Main loop
    rescan = False
    while True:
        changed_list = []
        remaining_files = all_files.copy()
        all_files = {}
        for path in paths:
            os.path.walk(path, f, None)
        removed_list = remaining_files.keys()
        if rescan:
            rescan = False
        elif changed_list or removed_list:
            rescan = func(changed_list, removed_list)

        time.sleep(delay)


if __name__ == '__main__':
    args = sys.argv
    num_of_args = len(args)
    
    if num_of_args == 1:
        configfile_path = generate_configfile()
    elif num_of_args > 1:
        if args[1] in ("-h", "--help"):
            print >> sys.stdout, USAGE
            sys.exit(0)
        else:
            configfile_path = args[1]
    else:
        print >> sys.stdout, "Too many arguments!"
        print >> sys.stdout, USAGE
        sys.exit(1)
    
    settings = parse_configfile(configfile_path)

    watch_folder   = settings["watch_folder"]
    output_folder  = settings["output_folder"]
    landscape_rule = Rule(*settings["landscape_rule"])
    portrait_rule  = Rule(*settings["portrait_rule"])
    square_rule    = Rule(*settings["square_rule"])

    def folder_has_changes(changed_files, removed_files):
        for f in changed_files:
            _, ext = os.path.splitext(f)
            if ext.lower() in VALID_EXTS:
                resize_image(f, output_folder,
                        landscape_rule, portrait_rule, square_rule)
        
        for f in removed_files:
            log_info("Removed %s." % os.path.basename(f))

    log_info("Start listening on %s.  [Ctrl-C] to shutdown." % watch_folder)
    watch_directories([watch_folder], folder_has_changes, SLEEP_INTERVAL)

