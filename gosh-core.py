#!/usr/bin/python
#coding=utf8
##----------------------------------------------------------------------------##
##               █      █                                                     ##
##               ████████                                                     ##
##             ██        ██                                                   ##
##            ███  █  █  ███                                                  ##
##            █ █        █ █        gosh-core.py                              ##
##             ████████████         Gosh                                      ##
##           █              █       Copyright (c) 2015 AmazingCow             ##
##          █     █    █     █      www.AmazingCow.com                        ##
##          █     █    █     █                                                ##
##           █              █       N2OMatt - n2omatt@amazingcow.com          ##
##             ████████████         www.amazingcow.com/n2omatt                ##
##                                                                            ##
##                                                                            ##
##                  This software is licensed as GPLv3                        ##
##                 CHECK THE COPYING FILE TO MORE DETAILS                     ##
##                                                                            ##
##    Permission is granted to anyone to use this software for any purpose,   ##
##   including commercial applications, and to alter it and redistribute it   ##
##               freely, subject to the following restrictions:               ##
##                                                                            ##
##     0. You **CANNOT** change the type of the license.                      ##
##     1. The origin of this software must not be misrepresented;             ##
##        you must not claim that you wrote the original software.            ##
##     2. If you use this software in a product, an acknowledgment in the     ##
##        product IS HIGHLY APPRECIATED, both in source and binary forms.     ##
##        (See opensource.AmazingCow.com/acknowledgment.html for details).    ##
##        If you will not acknowledge, just send us a email. We'll be         ##
##        *VERY* happy to see our work being used by other people. :)         ##
##        The email is: acknowledgmentopensource@AmazingCow.com               ##
##     3. Altered source versions must be plainly marked as such,             ##
##        and must notbe misrepresented as being the original software.       ##
##     4. This notice may not be removed or altered from any source           ##
##        distribution.                                                       ##
##     5. Most important, you must have fun. ;)                               ##
##                                                                            ##
##      Visit opensource.amazingcow.com for more open-source projects.        ##
##                                                                            ##
##                                  Enjoy :)                                  ##
##----------------------------------------------------------------------------##

## Imports ##
import os;
import os.path;
import sys;
import getopt;
import termcolor;

################################################################################
## Constants / Globals                                                        ##
################################################################################
class Constants:
    #Where the bookmarks will be stored. 
    PATH_DIR_RC  = "~/.cowgoshrc"
    PATH_FILE_RC = os.path.expanduser(os.path.join(PATH_DIR_RC, "goshrc.txt"));

    #Some chars that are important to gosh.
    #This char is used to pass the values back to gosh shell script.
    OUTPUT_META_CHAR   = "#";
    BOOKMARK_SEPARATOR = ":";

    #Kind of getopt flags but fixed in positions. 
    ACTION_HELP      = "help";
    ACTION_VERSION   = "version";
    ACTION_LIST      = "list";
    ACTION_LIST_LONG = "list-long";
    ACTION_REMOVE    = "remove";
    ACTION_ADD       = "add";
    ACTION_UPDATE    = "update";


class Globals:
    bookmarks     = {};    #Our bookmarks dictionary.
    opt_no_colors = False; #If user wants color or not.


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
            return termcolor.colored(msg, color);
        return msg;


################################################################################
## Read / Write Functions                                                     ##
################################################################################
def check_rc_files():
    #This will ensure that the RC path and file exists.
    if(not os.path.isdir(Constants.PATH_DIR_RC)):
        checked_system("mkdir -p {}".format(Constants.PATH_DIR_RC));
    if(not os.path.isfile(Constants.PATH_FILE_RC)):
        checked_system("touch {}".format(Constants.PATH_FILE_RC));

def read_bookmarks():
    #Check if rc file exists...
    check_rc_files();

    #Open the filename and read all bookmarks that are in format of:
    #   BookmarkName : BookmarkSeparator (Note that the ':' is the separator)
    try:
        bookmarks_file = open(Constants.PATH_FILE_RC);
        
        for bookmark in bookmarks_file.readlines():
            bookmark = bookmark.replace("\n", "");
            name, path = bookmark.split(Constants.BOOKMARK_SEPARATOR);
    
            #Trim all white spaces.        
            name = name.replace(" ", "");
            path = path.replace(" ", "");

            Globals.bookmarks[name] = path;
    
    except Exception, e:
        #Failed to unpack, this is because the bookmarks aren't in form of
        #   Name SEPARATOR Path. 
        #So state it to user, so he could correct manually.
        help_msg = "{} {} {} {}".format("Check if all values are in form of",
                                        C.blue("BookmarkName"),
                                        C.magenta(Constants.BOOKMARK_SEPARATOR),
                                        C.blue("BookmarkPath"));

        msg = "{} ({})\n{}".format("Bookmarks file is corrupted.",
                                    C.blue(Constants.PATH_FILE_RC),
                                    help_msg);
        print_fatal(msg);

    finally:
        bookmarks_file.close();

def write_bookmarks():
    #Save the bookmarks in disk. Sort them before just as convenience for
    #who wants to mess with them in an editor.
    bookmarks_str = "";
    for key in sorted(Globals.bookmarks.keys()):
        bookmarks_str += "{} : {}\n".format(key,Globals.bookmarks[key]);

    #Check if rc file exists...
    check_rc_files();

    #Write and close.
    try:
        bookmarks_file = open(Constants.PATH_FILE_RC, "w");
        bookmarks_file.write(bookmarks_str);

    except Exception, e:
        print_fatal("Error while writing file. {}".format(str(e)));
    
    finally:        
        bookmarks_file.close();



################################################################################
## Helper Functions                                                           ##
################################################################################
def checked_system(cmd, expected_val = 0):
    if(os.system(cmd) != expected_val):
        print_fatal("Error while executing command ({}).".format(C.red(cmd)));

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
    print """Usage:
  gosh <Name>
  gosh [-hv] [-n] [-lL] [-au <Name> <Path>] [-r <Name>]

Options:
 *-h               : Show this screen.
 *-v               : Show app version and copyright.
 *-a <Name> <Path> : Add a Bookmark with specified path.
 *-r <Name>        : Remove a Bookmark.
 *-u <Name> <Path> : Update a Bookmark to path.
 *-l               : Show all Bookmarks (no Paths).
 *-L               : Show all Bookmarks and Paths.
  -n               : Print the output without colors.

Notes:
  If <Path> is blank the current dir is assumed.
  
  Options marked with * are exclusive, i.e. the gosh will run that
  and exit successfully after the operation.
"""
    exit(0);

def print_version():
    print "\n".join([
        "gosh - 0.2.0 - N2OMatt <n2omatt@amazingcow.com>",
        "Copyright (c) 2015 - Amazing Cow",
        "This is a free software (GPLv3) - Share/Hack it",
        "Check opensource.amazingcow.com for more :)"]);
    exit(0);
 

################################################################################
## Action Functions                                                           ##
################################################################################
def list_bookmarks(long = False):
    read_bookmarks();

    if(len(Globals.bookmarks) == 0):
        print "No bookmarks yet... :/";
        exit(0);

    #Get the greater bookmark's name length. It will 
    #be used to align all the bookmark's name.
    max_len = max(map(len, Globals.bookmarks.keys()));
    for key in sorted(Globals.bookmarks.keys()):
        spaces = " " * (max_len - len(key)); #Put spaces to align the names.
        path   = Globals.bookmarks[key];

        if(long):
            print "{_key}{_spaces} : {_path}".format(_key=C.blue(key),
                                                     _spaces=spaces,
                                                     _path=C.magenta(path));
        else:
            print C.blue(key);
            
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
    #gosh will pass as last parameter with user want color or not.
    #So we grab this information and remove them from list because
    #The other options will use the lenght of the list as a way to check
    #if the arguments are ok.
    args = sys.argv[1:]
    if(args[-1] == "no-colors"):
        Globals.opt_no_colors = True;
        args.pop();

    first_arg  = args[0];
    second_arg = args[1] if len(args) > 1 else "";
    third_arg  = args[2] if len(args) > 2 else "";

    #All the command line options are exclusive operations. i.e
    #they will run the requested command and exit after it.
    if(Constants.ACTION_HELP      == first_arg): print_help();
    if(Constants.ACTION_VERSION   == first_arg): print_version();
    if(Constants.ACTION_LIST      == first_arg): list_bookmarks();
    if(Constants.ACTION_LIST_LONG == first_arg): list_bookmarks(long=True);
    if(Constants.ACTION_REMOVE    == first_arg): remove_bookmark(second_arg);
    if(Constants.ACTION_ADD       == first_arg): add_bookmark(second_arg, third_arg);
    if(Constants.ACTION_UPDATE    == first_arg): update_bookmark(second_arg, third_arg);


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
    #by the "#" and the message | path.
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
        msg = "Bookmark ({}) doesn't exists.".format(C.blue(first_arg));
        print_invalid_output(msg);

    #Bookmark exists, check if path is valid.
    bookmark_path = path_for_bookmark(first_arg);
    if(not os.path.isdir(bookmark_path)):
        msg = "Bookmark ({}) {} ({})".format(C.blue(first_arg),
                                             "exists but it's path is invalid.",
                                             C.magenta(bookmark_path));
        print_invalid_output(msg);        

    #Bookmark and path are valid.
    #Print the path to gosh shell script change the directory.
    print_valid_output(bookmark_path);


if(__name__ == "__main__"):
    #If any error occurs in main, means that user is trying to use 
    #the gosh-core instead of gosh. Since gosh always pass the parameters 
    #even user didn't. So inform the user that the correct is use gosh.
    try:
        main();
    except Exception, e:        
        print_fatal("You should use gosh not gosh-core.");
