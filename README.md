Gosh
====
Made with <3 by [Amazing Cow](http://www.amazingcow.com).

## Intro:
A very basic shell book marker util.  

Gosh is a program that makes the shell navigation a bit easier. 
It's not a way that We liked yet, but is good enough to be used.

The main drawback that We've found is as we cannot change the current 
working directory of parent process we must do some workaround stuff to get the program to work.

We currently do not understand ALL the complications that can occur by 
using the program, actually I don't see any but the "bad message" if we type a bookmark incorrectly.

## How it works:
The program has two "parts", the gosh itself and another "function" called 
gosh-go. All of them are placed into a single file, so "source" it is very simple.

* **gosh**: This a function that encompass the main functionality, this function 
will hide  all the inner functions, vars, constants, etc. from the outer scope.  
So it will not pollute the shell environment.

* **gosh-go**: This is a function that is more liked to be used as daily basis,
it will call the innerfunctions of ```gosh``` to retrieve the path associated 
with the bookmark and change the current directory to the retrieved path.

So if we want **add**, **remove**, **update**, **list**, ask **helper** or see the **version** 
we gonna use ```gosh```.  
If we want **change the current dir** to a bookmark's dir we gonna use ```gosh-go```.

This is far from ideal, but works for now. You're are very welcome to **hack and share** this program :)

Drawbacks:
-----
1. We must have two separate "programs" one ```gosh``` to manage the bookmarks, 
other to change the directories ```gosh-go```.
2. The ```gosh``` and ```gosh-go``` error message is currently very bad.

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

```gosh-go MonsterFramework```

or 

```gosh-go Client_Project1```

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
gosh-go AValidBookmark
```
    
## Status:
We're happy using gosh in a OSX 10.10, Xubuntu Linux 14.10 and CentOS (our web hosting).      
Up to date I don't have found any "bug" (but I'm sure that they are there, hidden, waiting
for just one more   
user install this to goes out and mess everything :D ).

## Installation:
Just source the file. This is usually more convenient to do in a ```.bashrc``` or ```.bashprofile``` file like:

``` bash
    #your .bashrc or .bashprofile.
    source /path/to/gosh.sh
```

## License:
This software is released under GPLv3.

## TODO:
Check the TODO file.

## Others:
Check our repos and take a look at our [open source site](http://opensource.amazingcow.com).
