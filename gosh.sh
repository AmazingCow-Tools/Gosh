#!/bin/bash
##----------------------------------------------------------------------------##
##               █      █                                                     ##
##               ████████                                                     ##
##             ██        ██                                                   ##
##            ███  █  █  ███                                                  ##
##            █ █        █ █                                                  ##
##             ████████████         gosh.sh - Gosh                            ##
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


gosh() (
    ############################################################################
    ## Constants                                                              ##
    ############################################################################
    PATH_DIR_RC=~/cowgoshrc
    PATH_FILE_RC="${PATH_DIR_RC}"/goshrc.txt
    PATH_TEMP_FILE="${PATH_DIR_RC}"/temp_goshrc.txt

    BOOKMARK_SEP=":"
    NO_COLORS=false

    ############################################################################
    ## Helper Functions                                                       ##
    ############################################################################
    show_help() {
        echo "Usage:"
        echo "  gosh [-hv] [-ln] [-aru] ..."
        echo "  gosh-go <bookmark>"
        echo ""
        echo "  -h                   : Show this screen."
        echo "  -v                   : Show app version and copyright."
        echo "  -a <Bookmark> <Path> : Add a Bookmark with specified path."
        echo "  -r <Bookmark>        : Remove a Bookmark."
        echo "  -u <Bookmark> <Path> : Update a Bookmark to path."
        echo "  -l                   : Show all Bookmarks and Paths."
        echo "  -n                   : Print the output without colors."
        echo ""
        echo "  gosh-go <bookmark> - Change dir to Bookmark's path."
    }
    show_version() {
        echo "gosh - 0.1.2 - N2OMatt <n2omatt@amazingcow.com>"
        echo "Copyright (c) 2015 - Amazing Cow"
        echo "This is a free software (GPLv3) - Share/Hack it"
        echo "Check opensource.amazingcow.com for more :)"
    }
    print_error()
    {
        echo "ERROR: ${1}";
    }

    #File/Dir Functions.
    check_dir_and_files() {
        #Check if the rc folder exists.
        if [ ! -e "${PATH_DIR_RC}" ]; then
            print_error "Directory ${PATH_DIR_RC} not found - creating one now."
            mkdir -p "${PATH_DIR_RC}"
        fi
        #Check if the file containing the data exists.
        if [ ! -e "${PATH_FILE_RC}" ]; then
            print_error "File ${PATH_FILE_RC} not found - creating one now."
            touch "${PATH_FILE_RC}"
        fi
    }
    sort_file() {
        cat "${PATH_FILE_RC}" | sort > "${PATH_TEMP_FILE}";\
        mv "${PATH_TEMP_FILE}" ${PATH_FILE_RC}
    }

    #Bookmark Functions.
    bookmark_exists() {
        #Check if already have a bookmark with the name.
        name=$1
        if [[ -z $name ]]; then
            return 1;
        fi

        if [[ -n $(grep "^\b${name}\b" $PATH_FILE_RC) ]]; then
            return 0
        fi
        return 1
    }
    path_for_bookmark() {
        name=$1
        v=$(grep "^\b${name}\b" $PATH_FILE_RC | cut -d"${BOOKMARK_SEP}" -f2);
        echo $v;
    }

    #Other Functions.
    expand_path() {
        echo $(cd $1; pwd)
    }
    fatal() {
        exit $1;
    }

    ############################################################################
    ## Action Functions                                                       ##
    ############################################################################
    list() {
        file_contents=$(cat $PATH_FILE_RC);

        #Turn the contents of file into an array without the : chars.
        array=(${file_contents//:/ });

        #Bookmark that has the greater name.
        greater_length=0;

        #Find the length of the name of the bookmark that has the longer name.
        for index in "${!array[@]}"
        do
            #Bookmarks are located in even indexes.
            if [ $((index % 2)) -eq 0 ]; then

                value=${array[index]};    #Value of the array at index.
                current_length=${#value}; #Lemgth of this bookmark name.
                #Update the length if needed.
                if [ $current_length -gt $greater_length ]; then
                    greater_length=$current_length;
                fi
            fi
        done

        #Print the bookmarks...
        for index in "${!array[@]}"
        do
            value=${array[index]}; #Current value of the array.

            #Names are located in even indexes, paths in odd indexes.
            if [ $((index % 2)) -eq 0 ]; then
                current_length=${#value};
                fmt="%-0$greater_length""s";

                #Put colors...
                if [ $NO_COLORS = false ]; then
                    tput setaf 2;
                fi;

                #Print the bookmark name.
                printf $fmt $value;

                #Put colors...
                if [ $NO_COLORS = false ]; then
                    tput sgr0;
                fi;

                #Print the separator.
                printf " : ";

            else
                echo $value;
            fi
        done
    }

    add() {
        name=$1;

        #Check if the bookmark with this name already exists.
        bookmark_exists $name
        if [[ $? == 0 ]]; then
            print_error "Bookmark (${name}) already exists";
            fatal 1;
        fi

        #Check if we got a value to add and if it is a valid directory.
        value=$2
        if [[ -z $value ]]; then
            print_error "Cannot add a bookmark (${name}) - missing path"
            fatal 1;
        fi
        value=$(expand_path $2)
        if [[ ! -d "$value" ]]; then
            print_error "Cannot add a bookmark (${name}) - path is invalid (${value})"
            fatal 1;
        fi

        #Everything is ok...
        #Add the bookmark
        echo "${name} ${BOOKMARK_SEP} ${value}" >> $PATH_FILE_RC

        #Keep the file organized.
        sort_file

        echo -e "\tAdded bookmark ${name} : ${value}";
    }

    remove() {
        name=$1;

        #Check if the bookmark with this name exists.
        bookmark_exists $name
        if [[ $? != 0 ]]; then
            print_error "Bookmark (${name}) does not exists";
            fatal 1;
        fi

        #Search and print the inverse into a temp file.
        #Next move the temp file into the rc file.
        grep -v "${name}" "${PATH_FILE_RC}" > "${PATH_TEMP_FILE}";\
        mv "${PATH_TEMP_FILE}" ${PATH_FILE_RC}

        #Keep the file organized.
        sort_file

        echo -e "\tRemoved bookmark ${name}";
    }

    update() {
        #Update is remove and add a bookmark.
        remove $1
        add $1 $2
        #Keep the file organized.
        sort_file
    }

    go()
    {
        name=$1;
        #Check if we have a bookmark with this name.
        bookmark_exists $name
        if [[ $? != 0 ]]; then
            print_error "Bookmark (${name}) does not exists";
            fatal 1;
        fi

        path=$(path_for_bookmark $name);
        echo $path
    }

    ############################################################################
    ## Initialization                                                         ##
    ############################################################################
    while getopts "hva:r:u:lgn" o; do
        case "${o}" in
            h) help_arg="true"      ;;
            v) version_arg="true"   ;;
            a) add_arg=${OPTARG}    ;;
            r) remove_arg=${OPTARG} ;;
            u) update_arg=${OPTARG} ;;
            l) list_arg="true"      ;;
            g) go_arg="true"        ;;
            n) no_colors_arg="true" ;;
        esac
    done
    shift $((OPTIND-1))

    check_dir_and_files

    #Help/Version.
    if [ -n "${help_arg}" ]; then
        show_help; exit 0;
    fi;
    if [ -n "${version_arg}" ]; then
        show_version; exit 0;
    fi;

    ##No Colors.
    if [ -n "${no_colors_arg}" ]; then
        NO_COLORS=true;
    fi;

    #ADD
    if [ -n "${add_arg}" ]; then
        add $add_arg $@; exit 0
    fi;
    #REMOVE
    if [ -n "${remove_arg}" ]; then
        remove $remove_arg; exit 0;
    fi;
    #UPDATE
    if [ -n "${update_arg}" ]; then
        update $update_arg $@; exit 0;
    fi;
    #LIST
    if [ -n "${list_arg}" ]; then
        list; exit 0;
    fi;
    #GO
    if [ -n "${go_arg}" ]; then
        go $@; exit 0;
    fi;
)

gosh-go() {

    if [ -n "${1}" ]; then
        path=$(gosh -g $1);
        cd $path && pwd;
    else
        gosh -h;
    fi
}
