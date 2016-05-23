#!/usr/bin/python
#coding=utf8
##----------------------------------------------------------------------------##
##               █      █                                                     ##
##               ████████                                                     ##
##             ██        ██                                                   ##
##            ███  █  █  ███        gosh-core.py                              ##
##            █ █        █ █        Gosh                                      ##
##             ████████████                                                   ##
##           █              █       Copyright (c) 2015, 2016                  ##
##          █     █    █     █      AmazingCow - www.AmazingCow.com           ##
##          █     █    █     █                                                ##
##           █              █       N2OMatt - n2omatt@amazingcow.com          ##
##             ████████████         www.amazingcow.com/n2omatt                ##
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
##        The email is: acknowledgment_opensource@AmazingCow.com              ##
##     3. Altered source versions must be plainly marked as such,             ##
##        and must not be misrepresented as being the original software.      ##
##     4. This notice may not be removed or altered from any source           ##
##        distribution.                                                       ##
##     5. Most important, you must have fun. ;)                               ##
##                                                                            ##
##      Visit opensource.amazingcow.com for more open-source projects.        ##
##                                                                            ##
##                                  Enjoy :)                                  ##
##----------------------------------------------------------------------------##

#COWTODO: Check if we can remove the absolute paths and instead use the ~ \
#         This will enable us to use the "same" paths on OSX and Linux.
#COWTODO: Change the termcolor to cowtermcolor.

## Imports ##
import os;
import os.path;
import sys;
import getopt;
import pdb;

#Termcolor isn't a standard module (but is really nice), so we must
#support system that doens't has it. On those systems the colored,
#will just return the plain string.
try:
    from termcolor import colored;
except Exception, e:
    def colored(msg, color): return msg;


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
    ACTION_HELP            = "gosh_opt_help";
    ACTION_VERSION         = "gosh_opt_version";
    ACTION_LIST            = "gosh_opt_list";
    ACTION_LIST_LONG       = "gosh_opt_list-long";
    ACTION_REMOVE          = "gosh_opt_remove";
    ACTION_ADD             = "gosh_opt_add";
    ACTION_UPDATE          = "gosh_opt_update";
    ACTION_PRINT           = "gosh_opt_print";
    ACTION_EXISTS_BOOKMARK = "gosh_opt_exists_bookmark";

class Globals:
    bookmarks     = {};    #Our bookmarks dictionary.
    opt_no_colors = False; #If user wants color or not.


################################################################################
## Colored Class                                                              ##
################################################################################
class C:
    @staticmethod
    def red(msg):
        return C._colored(msg, "red");

    @staticmethod
    def blue(msg):
        return C._colored(msg, "blue");

    @staticmethod
    def magenta(msg):
        return C._colored(msg, "magenta");

    @staticmethod
    def _colored(msg, color):
        if(not Globals.opt_no_colors):
            return colored(msg, color);
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
            path = path.lstrip().rstrip();

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

def bookmark_for_path(path):
    if(path is None):
        return None;

    read_bookmarks();
    full_path = canonize_path(path);

    for bookmark_name in Globals.bookmarks.keys():
        bookmark_path = canonize_path(Globals.bookmarks[bookmark_name]);
        if(bookmark_path == full_path):
            return bookmark_name;

    return None;

def ensure_valid_bookmark_name_or_die(name):
    #Check if name isn't empty...
    if(name is None or len(name) == 0):
        print_fatal("Missing arguments - name");

    #Check if this name is a valid name.
    if(((Constants.OUTPUT_META_CHAR   in name) or
        (Constants.BOOKMARK_SEPARATOR in name))):
        print_fatal("{} ('{}', '{}') chars.".format("Bookmark name cannot contains",
                                                    Constants.OUTPUT_META_CHAR,
                                                    Constants.BOOKMARK_SEPARATOR));

def ensure_valid_path_or_die(path):
    if(not os.path.isdir(path)):
        print_fatal("Path ({}) is invalid.".format(C.magenta(path)));


def ensure_bookmark_existance_or_die(name, bookmark_shall_exists):
    if(bookmark_exists(name) and bookmark_shall_exists == False):
        print_fatal("Bookmark ({}) already exists.".format(C.blue(name)));

    if(not bookmark_exists(name) and bookmark_shall_exists == True):
        print_fatal("Bookmark ({}) doesn't exists.".format(C.blue(name)));

def canonize_path(path):
    path = path.lstrip().rstrip();
    path = os.path.abspath(os.path.expanduser(path));

    return path;

def remove_enclosing_quotes(value):
    return value.strip("'");


################################################################################
## Print Functions                                                            ##
################################################################################
def print_fatal(msg):
    print "{} {}".format(C.red("[FATAL]"), msg);
    exit(1);

def print_help():
    print """Usage:
  gosh                        (Same as gosh -l)
  gosh <name>                 (To change the directory)
  gosh -h | -v                (Show help | version)
  gosh -l | -L                (Show list of bookmarks)
  gosh -p <name>              (Show path for bookmark)
  gosh -e <path>              (Show bookmark for path)
  gosh -a | -u <name> <path>  (Add | Update bookmark)
  gosh -r <name>              (Remove the bookmark)

Options:
  *-h --help     : Show this screen.
  *-v --version  : Show app version and copyright.

  *-e --exists <path>  : Print the Bookmark for path.
  *-p --print  <name>  : Print the path of Bookmark.

  *-l --list       : Show all Bookmarks (no Paths).
  *-L --list-long  : Show all Bookmarks and Paths.

  *-a --add    <name> <path>  : Add a Bookmark with specified path.
  *-r --remove <name>         : Remove a Bookmark.
  *-u --update <name> <path>  : Update a Bookmark to path.

  -n --no-colors : Print the output without colors.

Notes:
  If <path> is blank the current dir is assumed.

  Options marked with * are exclusive, i.e. the gosh will run that
  and exit after the operation.
"""
    exit(0);

def print_version():
    print "\n".join([
        "gosh - 0.6.3 - N2OMatt <n2omatt@amazingcow.com>",
        "Copyright (c) 2015, 2016 - Amazing Cow",
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
    #Must be valid name.
    ensure_valid_bookmark_name_or_die(name);

    #Load from file.
    read_bookmarks();

    #Check if we have this bookmark, since we are adding we cannot have it.
    ensure_bookmark_existance_or_die(name, bookmark_shall_exists=False);

    #Check if path is valid path.
    abs_path = canonize_path(path);
    ensure_valid_path_or_die(abs_path);

    print abs_path;
    #Name and Path are valid... Add it and inform the user.
    Globals.bookmarks[name] = abs_path;
    msg = "Bookmark added:\n  ({}) - ({})".format(C.blue(name),
                                                  C.magenta(abs_path));
    print msg;

    write_bookmarks(); #Save to file
    exit(0);

def remove_bookmark(name):
    #Must be valid name.
    ensure_valid_bookmark_name_or_die(name);

    #Load from file.
    read_bookmarks();

    #Check if we actually have a bookmark with this name.
    ensure_bookmark_existance_or_die(name, bookmark_shall_exists=True);

    #Bookmark exists... Remove it and inform the user.
    del Globals.bookmarks[name];
    print "Bookmark removed:\n  ({})".format(C.blue(name));

    write_bookmarks(); #Save to file
    exit(0);

def update_bookmark(name, path):
    #Must be valid name.
    ensure_valid_bookmark_name_or_die(name);

    #Load from file.
    read_bookmarks();

    #Check if we have this bookmark, since we are updating we must have it.
    ensure_bookmark_existance_or_die(name, bookmark_shall_exists=True);

    #Check if path is valid path.
    abs_path = canonize_path(path);
    ensure_valid_path_or_die(abs_path);

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
    #The other options will use the length of the list as a way to check
    #if the arguments are ok.
    args = sys.argv[1:]
    if(args[-1] == "no-colors"):
        Globals.opt_no_colors = True;
        args.pop();

    #gosh.sh is using getopt(1) and it passes the arguments inside a pair
    #of single quotes - This method will remove them.
    first_arg  = remove_enclosing_quotes(args[0]);
    second_arg = remove_enclosing_quotes(args[1]) if len(args) > 1 else "";
    third_arg  = remove_enclosing_quotes(args[2]) if len(args) > 2 else "";

    #All the command line options are exclusive operations. i.e
    #they will run the requested command and exit after it.
    #Help / Version.
    if(Constants.ACTION_HELP    == first_arg): print_help();
    if(Constants.ACTION_VERSION == first_arg): print_version();

    #List.
    if(Constants.ACTION_LIST      == first_arg): list_bookmarks();
    if(Constants.ACTION_LIST_LONG == first_arg): list_bookmarks(long=True);

    #Remove / Add / Update.
    if(Constants.ACTION_REMOVE  == first_arg): remove_bookmark(second_arg);
    if(Constants.ACTION_ADD     == first_arg): add_bookmark   (second_arg, third_arg);
    if(Constants.ACTION_UPDATE  == first_arg): update_bookmark(second_arg, third_arg);

    #Exists Bookmark
    if(Constants.ACTION_EXISTS_BOOKMARK == first_arg):
        bookmark_name = bookmark_for_path(second_arg);
        if(bookmark_name is None):
            print "No bookmark";
            exit(1);
        else:
            print "Bookmark: ({})".format(C.blue(bookmark_name));
            exit(0);

    #Print.
    if(Constants.ACTION_PRINT == first_arg):
        if(len(second_arg) == 0):
            print_fatal("Missing args - name.");

        if(not bookmark_exists(second_arg)):
            msg = "Bookmark ({}) doesn't exists.".format(C.blue(second_arg));
            print msg;
            exit(1);


        #Bookmark exists, check if path is valid.
        bookmark_path = path_for_bookmark(second_arg);
        if(not os.path.isdir(bookmark_path)):
            msg = "Bookmark ({}) {} ({})".format(C.blue(second_arg),
                                                 "exists but it's path is invalid.",
                                                 C.magenta(bookmark_path));
            print msg;
            exit(1);

        #Bookmark and path are valid.
        #Print the path to gosh shell script change the directory.
        print bookmark_path;
        exit(0);


if(__name__ == "__main__"):
    #If any error occurs in main, means that user is trying to use
    #the gosh-core instead of gosh. Since gosh always pass the parameters
    #even user didn't. So inform the user that the correct is use gosh.
    try:
        main();
    except Exception, e:
        print_fatal("You should use gosh not gosh-core. (Exception: ({}))".format(e));
