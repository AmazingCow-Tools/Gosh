#!/usr/bin/python

#COWTODO: Add the license headers.

import os;
import os.path;
import sys;
import getopt;
import subprocess
from termcolor import colored;

################################################################################
## Constants / Globals                                                        ##
################################################################################
class Constants:
    #COWTODO: Paths are wrong. They should be hidden.
    PATH_DIR_RC    = "~/cowgoshrc"
    PATH_FILE_RC   = os.path.expanduser(os.path.join(PATH_DIR_RC, "goshrc.txt"));
    PATH_TEMP_FILE = os.path.join(PATH_DIR_RC, "temp_goshrc.txt");

    #COWTODO: Comment.
    OUTPUT_META_CHAR   = "#";
    BOOKMARK_SEPARATOR = ":";

class Globals:
    #COWTODO: Comment.
    bookmarks = {};
    opt_no_colors = False;


################################################################################
## Colored Class                                                              ##
################################################################################
class C:
    @staticmethod
    def red(msg):
        return C.__colored(msg, "red");
    
    @staticmethod
    def blue(msg):
        return C.__colored(msg, "blue");
    
    @staticmethod
    def magenta(msg):
        return C.__colored(msg, "magenta");

    @staticmethod 
    def __colored(msg, color):
        if(not Globals.opt_no_colors):
            return colored(msg, color);
        return msg;


################################################################################
## Read / Write Functions                                                     ##
################################################################################
def read_bookmarks():
    #COWTODO: Comment.
    for bookmark in open(Constants.PATH_FILE_RC):
        bookmark = bookmark.replace("\n", "");
        name, path = bookmark.split(Constants.BOOKMARK_SEPARATOR);
        
        name = name.replace(" ", "");
        path = path.replace(" ", "");

        Globals.bookmarks[name] = path;

def write_bookmarks():
    #COWTODO: Comment.
    #COWTODO: Check if has a better and nicer way to achieve this.
    os.system("touch {}".format(Constants.PATH_TEMP_FILE));
    for key in sorted(Globals.bookmarks.keys()):
        os.system("echo \"{} : {}\" >> {}".format(key, 
                                                  Globals.bookmarks[key],
                                                  Constants.PATH_TEMP_FILE));

    os.system("mv {} {}".format(Constants.PATH_TEMP_FILE,
                                Constants.PATH_FILE_RC));




################################################################################
## Helper Functions                                                           ##
################################################################################
def bookmark_exists(name):
    read_bookmarks(); 
    return name in Globals.bookmarks.keys();

def path_for_bookmark(name):
    read_bookmarks();
    return Globals.bookmarks[name];


################################################################################
## Print Functions                                                            ##
################################################################################
def print_fatal(msg):
    print "{} {}".format(C.red("[FATAL]"), msg);
    exit(1);

def print_invalid_output(msg):
    print "1#" + "{} {}".format(C.red("[ERROR]"), msg);
    exit(1);

def print_valid_output(msg):
    print "0#" + msg;
    exit(0);

def print_help():
    #COWTODO: Update the msg.
    print """Usage:
  gosh [-hv] [-ln] [-aru] ...
  gosh-go <bookmark>

  -h                   : Show this screen.
  -v                   : Show app version and copyright.
  -a <Bookmark> <Path> : Add a Bookmark with specified path.
  -r <Bookmark>        : Remove a Bookmark.
  -u <Bookmark> <Path> : Update a Bookmark to path.
  -l                   : Show all Bookmarks and Paths.
  -n                   : Print the output without colors.
"""
    exit(0);

def print_version():
    #COWTODO: Implement.
    print "version";
    exit(0);
    # "gosh - 0.1.2 - N2OMatt <n2omatt@amazingcow.com>"
    # "Copyright (c) 2015 - Amazing Cow"
    # "This is a free software (GPLv3) - Share/Hack it"
    # "Check opensource.amazingcow.com for more :)"
 
def get_terminal_width():
        return int(subprocess.check_output(['tput', 'cols']));


################################################################################
## Action Functions                                                           ##
################################################################################
def list_bookmarks():
    read_bookmarks();

    if(len(Globals.bookmarks) == 0):
        print "No bookmarks yet... :/";
        exit(0);

    #Get the greater bookmark's name length. It will be used to align 
    #all the bookmark's name.
    max_len = max(map(len, Globals.bookmarks.keys()));
    terminal_columns = get_terminal_width();


    for key in sorted(Globals.bookmarks.keys()):
        spaces = " " * (max_len - len(key)); #Put spaces to align the names.
        path   = Globals.bookmarks[key];
        
        #COWTODO: Make the output correct.
        path_max_len = max(terminal_columns - (len(key + spaces + " : ") + 3), 0);
        print_path = path[0:path_max_len];

        if(print_path != path):
            print_path += "...";

        print "{_key}{_spaces} : {_path}".format(_key=C.blue(key),
                                                 _spaces=spaces,
                                                 _path=C.magenta(print_path));    
    exit(0);

def add_bookmark(name, path):    
    read_bookmarks(); #Load from file.

    #Check if we have this bookmark, since we are adding we cannot have it.
    if(bookmark_exists(name)):
        print_fatal("Bookmark ({}) already exists.".format(C.blue(name)));                                                    

    #Check if this name is a valid name.
    if(Constants.OUTPUT_META_CHAR in name):
        print_fatal("{} '{}' char.".format("Bookmark name cannot contain",
                                           Constants.OUTPUT_META_CHAR));

    #Check if path is valid path.
    abs_path = os.path.abspath(os.path.expanduser(path));
    if(not os.path.isdir(abs_path)):
        print_fatal("Path ({}) is invalid.".format(C.magenta(abs_path)));

    #Name and Path are valid... Add it and inform the user.
    Globals.bookmarks[name] = abs_path;
    msg = "Bookmark added:\n  ({}) - ({})".format(C.blue(name),
                                                  C.magenta(abs_path));
    print msg;

    write_bookmarks(); #Save to file
    exit(0);

def remove_bookmark(name):
    read_bookmarks(); #Load from file.

    #Check if we actually have a bookmark with this name.
    if(not bookmark_exists(name)):
        print_fatal("Bookmark ({}) doesn't exists.".format(C.blue(name)));   

    #Bookmark exists... Remove it and inform the user.
    del Globals.bookmarks[name];
    print "Bookmark removed:\n  ({})".format(C.blue(name));

    write_bookmarks(); #Save to file
    exit(0);

def update_bookmark(name, path):
    read_bookmarks(); #Load from file.

    #Check if we have this bookmark, since we are updating we must have it.
    if(not bookmark_exists(name)):
        print_fatal("Bookmark ({}) doesn't exists.".format(C.blue(name)));   

    #Check if this name is a valid name.
    if(Constants.OUTPUT_META_CHAR in name):
        print_fatal("{} '{}' char.".format("Bookmark name cannot contain",
                                           Constants.OUTPUT_META_CHAR));

    #Check if path is valid path.
    abs_path = os.path.abspath(os.path.expanduser(path));
    if(not os.path.isdir(abs_path)):
        print_fatal("Path ({}) is invalid.".format(C.magenta(abs_path)));

    #Bookmark exists and path is valid... Update it and inform the user.
    Globals.bookmarks[name] = abs_path;
    msg = "Bookmark updated:\n  ({}) - ({})".format(C.blue(name),
                                                    C.magenta(abs_path));
    print msg;

    write_bookmarks(); #Save to file
    exit(0);

################################################################################
## Script Initialization                                                      ##
################################################################################
def main():
    #COWTODO: This shoud be at Constants class.
    ACTION_HELP    = "help";
    ACTION_VERSION = "version";
    ACTION_LIST    = "list";
    ACTION_REMOVE  = "remove";
    ACTION_ADD     = "add";
    ACTION_UPDATE  = "update";


    #COWTODO: Comment and this is very ugly.
    args = sys.argv[1:]
    if(args[-1] == "no-colors"):
        Globals.opt_no_colors = True;
        args.pop();

    first_arg  = args[0];
    second_arg = args[1] if len(args) > 1 else "";
    third_arg  = args[2] if len(args) > 2 else "";

    #All the command line options are exclusive operations. i.e
    #they will run the requested command and exit after it.
    if(ACTION_HELP    == first_arg): print_help();
    if(ACTION_VERSION == first_arg): print_version();
    if(ACTION_LIST    == first_arg): list_bookmarks();
    if(ACTION_REMOVE  == first_arg): remove_bookmark(second_arg);
    if(ACTION_ADD     == first_arg): add_bookmark(second_arg, third_arg);
    if(ACTION_UPDATE  == first_arg): update_bookmark(second_arg, third_arg);


    #No command line options were found so it means that user is trying 
    #to go to a bookmark location. But since this program is not a stand 
    #alone program, it actually don't go to the requested location, it 
    #will just 'print' the bookmark's path. 
    #By 'printing' the location we enable the gosh shell script to 'capture'
    #the 'printed' location and actually change the directory.
    #
    #But we have caveat here, the gosh shell script must be able to recognize
    #the valid output i.e. the bookmark's path from the error output i.e. the 
    #stuff that must be show to user but isn't a path. 
    #To do this we decide to set the '#' character as a meta character that 
    #has the meaning of be a separator. This way we pass a return value followed
    #by the "#" and the message|path.
    #
    #So any valid path will be printed as:
    #   0#/some/path/here - Where: 0 is the return value for gosh shell script.
    #                              # is the separator (used in cut).
    #                              /some/path/here is a valid path.
    #And any invalid output will be printed as:
    #  1#ERROR MESSAGE - Where: 1 is the return value for gosh shell script.
    #                           # is the separator.
    #                           ERROR MESSAGE is the error message. :O 
    if(not bookmark_exists(first_arg)):
        print_invalid_output("Bookmark ({}) doesn't exists.".format(C.blue(first_arg)));
    
    #Print the path to gosh shell script change the directory.
    print_valid_output(path_for_bookmark(first_arg));


if __name__ == '__main__':
    main();
