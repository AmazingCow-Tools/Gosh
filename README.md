# Gosh

**Made with <3 by [Amazing Cow](http://www.amazingcow.com).**



<!-- ####################################################################### -->
<!-- ####################################################################### -->

## Description:

```gosh``` - A basic shell book marker util.  

```gosh``` is a program that makes the shell navigation a bit easier by 
enabling you to assign meaningful names to paths and navigate around using 
those meaningful names instead of the raw paths.


```gosh``` will try to auto complete what is being typed.


<br>

As usual, you are **very welcomed** to **share** and **hack** it.



<!-- ####################################################################### -->
<!-- ####################################################################### -->

## Usage:

``` 
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

```

### Examples:

* Go some location of bookmark:
    
``` bash
    # You can do this from anywhere. Now imagine that MyBookmark refers 
    # to a very deeply path like :
    #  /home/you/Documents/Projects/Games/OpenSource/TicTacToe/Linux/Images
     
    $ gosh MyBookmark 

    # Is the same of doing a:
    #   cd /home/you/Documents/Projects/Games/OpenSource/TicTacToe/Linux/Images
    # The nicer thing is that gosh remembers the fullpath for a bookmark
    # so it will always cd correctly :)
```

* Add a bookmark.

``` bash
    $ gosh    -a AnAwesomeGame                   # Using short opt (Path is assumed to be "./").
    $ gosh --add PlaceThatIGoOften ~/SomeDirHere # Using long opt  (gosh understands the relative path names).
```
    
* Remove a bookmark.

``` bash
    $ gosh       -r IDontLikeThisBookmark # Short opt.
    $ gosh --remove UnusedBookmarkName    # Long opt.
```

* Update a bookmark.

``` bash
    $ gosh      -u MyAwesomeGame ~/NewPath      # Short opt, relative paths.
    $ gosh -update MyAwesomeGame2 /home/me/game # Long opt, absolute paths are ok too.
```
    
* List all the bookmarks.
    
``` bash
    $ gosh    -l # Short opt, Will list only the bookmark names.
    $ gosh -list # Ditto but with long opt.

    $ gosh -L         # Short opt, Will list the bookmarks and paths.
    $ gosh -list-long # Long opt, Will list the bookmarks and paths.
```


<!-- ####################################################################### -->
<!-- ####################################################################### -->

## Install:

Use the Makefile.

``` bash
    make install
```

Or to uninstall

``` bash
    make uninstall
```

### Notes:

* The install / uninstall targets accepts the file that gosh will be sourced, 
the default is ```~/.bashrc```.   
To specify other file use ```BASH_PROFILE=/path/to/profile```   
(**Notice for OSX users:** In OSX the profile is ```~/.bash_profile``` so, you 
need to change it accordingly)

* A bash-completion script is also provided if your system supports.   
  By default it will get the installation running the command:   
```pkg-config --variable=completionsdir bash-completion```   
   You can change the installation location passing another path as:   
``` BASH_COMPLETION_DIR=/path/to/completion/dir ``` 


* The install / uninstall targets make backups of the sourced file.   
  They are located in ```~/.bash_profile_gosh_backup```




<!-- ####################################################################### -->
<!-- ####################################################################### -->

## Dependencies:

There is no dependency for ```gosh```.



<!-- ####################################################################### -->
<!-- ####################################################################### -->

## Environment and Files: 

### Files:

* ```~/.cowgoshrc``` - Directory containing ```gosh``` info.
* ```~/.cowgoshrc/goshrc.txt``` - ```gosh``` bookmark list.

* ```/path/for/bash/completion/gosh``` - The ```gosh``` auto completion helper   
  Note that this is only installed on supported systems.


### Environments:

* ```gosh``` exposes the gosh function.



<!-- ####################################################################### -->
<!-- ####################################################################### -->

## License:

This software is released under GPLv3.



<!-- ####################################################################### -->
<!-- ####################################################################### -->

## TODO:

Check the TODO file for general things.

This projects uses the COWTODO tags.   
So install [cowtodo](http://www.github.com/AmazingCow-Tools/COWTODO/) and run:

``` bash
$ cd path/for/the/project
$ cowtodo 
```

That's gonna give you all things to do :D.



<!-- ####################################################################### -->
<!-- ####################################################################### -->

## BUGS:

We strive to make all our code the most bug-free as possible - But we know 
that few of them can pass without we notice ;).

Please if you find any bug report to [bugs_opensource@amazingcow.com]() 
with the name of this project and/or create an issue here in Github.



<!-- ####################################################################### -->
<!-- ####################################################################### -->

## Source Files:

* AUTHORS.txt
* CHANGELOG.txt
* COPYING.txt
* gosh_bash-completion.sh
* gosh-core.py*
* gosh.sh*
* Makefile
* OLDREADME.md
* README.md
* TODO.txt 



<!-- ####################################################################### -->
<!-- ####################################################################### -->

## Others:
Check our repos and take a look at our [open source site](http://opensource.amazingcow.com).
