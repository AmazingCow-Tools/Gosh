Gosh
====
Made with <3 by [Amazing Cow](http://www.amazingcow.com).

## Intro:

A very basic shell book marker util.  

Gosh is a program that makes the shell navigation a bit easier. 
It's not a way that we liked yet, but is good enough to be used.

The main drawback that we've found is as we cannot change the current 
working directory of parent process we must do some workaround stuff to get 
the program to work. To the end user this is almost transparent but the 
code solution isn't clean or elegant enough.   

See the **Drawbacks** section to see what works and what not.

Gosh was rewritten in the version 0.1x -> 0.2.x and now, we think, that the
way that stuff is organized is much better.

## How it works:

The program has two "parts", the ```gosh-core``` and the ```gosh``` function. 

The ```gosh-core``` is a python script located in ```/usr/local/bin``` that 
handles everything about the application, except changing directory.   

In Unix (and Linux and OSX and all :O) we cannot change the properties of the 
parent process and since when we start a program a fork of current shell is created
we're unable to change the current directory of the parent shell.   
This is not a problem to all operations of ```gosh``` like **add**, **remove**, **update** 
and **list** the bookmarks.   
But is a **BIG** problem in the main feature of ```gosh``` that is change the
current directory.  

To achieve this we create another file named ```gosh``` that is located inside 
of ```/usr/local/bin```.   
This file has only one function named ```gosh```.   
The file ```/usr/local/bin/gosh``` is sourced inside a ```~/.bash_profile```, so 
the function named ```gosh``` will take precedence in the name lookup.   
This is did that way to pollute the less possible the "programs namespace".   
The result is that when we're in a terminal and type ```gosh``` the function will 
be executed not the file located at ```/usr/local/bin```.

The ```gosh``` file and by extension the ```gosh``` function inside this file 
has only one job - Parse the command line options and forward them to ```gosh-core```.   
The ```gosh-core``` expects the options in a very strict way, so even is possible 
to use ```gosh-core``` directly (but not for changing the directory) is very unpleasant 
thing to do.

All operations (**add**, **remove**, **update**, **list**) are handled only by 
```gosh-core```, i.e. after finish the operation it'll will quit and ```gosh```
will do nothing more.  
But when user wants to change the directory the flow is a bit different. First ```gosh```
parse the command line parameters and forward to ```gosh-core``` the by it's time check 
if a bookmark exists and if the path is valid. After ```gosh-core``` complete its job
it must "pass back" the information to ```gosh```. 
This is done by printing the info, but since we're in sub shell the user don't get this 
output.   
So after ```gosh-core``` print the information, ```gosh``` parse it and check if the info
is a valid path or a error message and print it again (But now we're in the shell that
originated the flow, so all output is visible to user). 

Drawbacks:
-----
1. We must have too separated files. ```gosh-core``` and the ```gosh```.
2. We must source the ```gosh``` file to make it "part" of the current shell. 
Without this the changing directory stuff won't work.
3. We have a file and a function with same name - ```/usr/local/bin/gosh``` and inside
it the function ```gosh```. This works pretty well in the systems that we tried. (OSX 10.10,
Ubuntu 15.04, Ubuntu 14.04 and CentOS) with the bash version that 
came with those systems, but we're not 100% sure that is correct or will work at all times.
4. This is a hack, works but isn't pretty - Has to be another prettier way.
5. **GOSH WON'T WORK INSIDE SHELL SCRIPTS.**
6. **The user must have** ```/usr/local/bin/gosh``` **sourced.**

Motivation:
-----
We work in several small projects along of the day and usually one big project. 
Furthermore our directory tree is very deep.   
An example: 


```
~/Documents/Projects/AmazingCow/OpenSource/MonsterFramework
~/Documents/Projects/AmazingCow/OpenSource/AmazingBuild/PSDTools/PSDCutter
~/Documents/Projects/AmazingCow/Proprietary/InHouse/XYZ/ABC
~/Documents/Projects/AmazingCow/Proprietary/Client/Client1/A123
```

... And so on.

And is pain in butt to ```cd ..``` or ```cd ~/Documents/Projects/AmazingCow/...```
just to change the working project.  
I'd like to bookmark the directories and just type: 

```gosh MonsterFramework```

or 

```gosh Client_Project1```

This is the main motivation for create this stuff.

## Examples:
* Add a bookmark.
        
```
gosh -a AnAwesomeGame .
gosh -a PlaceThatIGoOften ~/SomeDirHere
```
    
* Remove a bookmark.

```
gosh -r MyAwesomeGame 
```

* Update a bookmark.

```
gosh -u MyAwesomeGame ~/NewPath
```
    
* List all the bookmarks.
    
```
gosh -l 
```
    
* Go some bookmark:
    
```
gosh AValidBookmark
```
    
## Status:
We're happy using gosh in a OSX 10.10, UbuntuMate 15.04, Ubuntu 14.04, Xubuntu
Linux 14.10 and CentOS (our web hosting).      
Up to date we don't have found any "bug" (but I'm sure that they are there, hidden, waiting
for just one more user install this to goes out and mess everything :D ).

## Installation:
Use the Makefile:

```
    make install 
```

To uninstall ```gosh``` using the makefile you can use:

```
    make uninstall
```

The install/uninstall targets accepts the file that gosh will be sourced, the default is```~/.bash_profile```.   
To specify other file use ```BASH_PROFILE=your_bash_profile_here```

A bash-completion script is also provided if your system supports.  

By default it will get the installation running the command:   
```pkg-config --variable=completionsdir bash-completion```   

You can change the installation location passing another path as:   
```BASH_COMPLETION_DIR=your_location_here```

#####Note 
The makefile will create backups before doing the operations.

## License:
This software is released under GPLv3.

## TODO:
Check the TODO file.

## Others:
Check our repos and take a look at our [open source site](http://opensource.amazingcow.com).
