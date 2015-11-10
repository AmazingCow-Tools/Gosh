#!/bin/bash
##----------------------------------------------------------------------------##
##               █      █                                                     ##
##               ████████                                                     ##
##             ██        ██                                                   ##
##            ███  █  █  ███                                                  ##
##            █ █        █ █        gosh.sh                                   ##
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

#Define some alias to ease the operations.
alias gosh-list="gosh -l";
alias gosh-add="gosh -a";
alias gosh-remove="gosh -r";
alias gosh-update="gosh -u";
alias gosh-go="gosh ";

function gosh
{
    local GOSH_CORE=gosh-core

    #The command line options that we can accept.
    #They are set with 0 meaning that they're disabled.
    #Only NO_COLORS options that are set with empty string
    #because we gonna fill it with a string if user pass the option.
    local OPT_HELP=0;
    local OPT_VERSION=0;
    local OPT_ADD=0;
    local OPT_REMOVE=0;
    local OPT_UPDATE=0;
    local OPT_LIST=0;
    local OPT_LIST_LONG=0;
    local OPT_PRINT=0;
    local OPT_NO_COLORS="";

    #No args, just list the bookmarks.
    if [ $# -eq 0 ]; then
        $GOSH_CORE "list";
        return;
    fi;

    #Parse the command line options.
    while getopts :hvarulLnp FLAG; do
        case $FLAG in
             h) OPT_HELP=1                ;;
             v) OPT_VERSION=1             ;;
             l) OPT_LIST=1                ;;
             L) OPT_LIST_LONG=1           ;;
             r) OPT_REMOVE=1              ;;
             a) OPT_ADD=1                 ;;
             u) OPT_UPDATE=1              ;;
             p) OPT_PRINT=1               ;;
             n) OPT_NO_COLORS="no-colors" ;;
            \?) OPT_HELP=1                ;;
        esac
    done
    shift $((OPTIND-1))  #This tells getopts to move on to the next argument.

    #COWTODO: Check if this is ok to do?
    unset OPTARG;
    unset OPTIND;

    #Start checking with command line options were give.
    #All options are exclusive, meaning that they'll run and exit after.
    if [ $OPT_HELP = 1 ]; then
        $GOSH_CORE "gosh_opt_help";

    elif [ $OPT_VERSION = 1 ]; then
        $GOSH_CORE "gosh_opt_version";

    elif [ $OPT_LIST = 1 ]; then
        # $OPT_NO_COLORS -> empty if not defined by user.
        $GOSH_CORE "gosh_opt_list" $OPT_NO_COLORS;

    elif [ $OPT_LIST_LONG = 1 ]; then
        # $OPT_NO_COLORS -> empty if not defined by user.
        $GOSH_CORE "gosh_opt_list-long" $OPT_NO_COLORS;

    elif [ $OPT_REMOVE = 1 ];
        # $1 -> The name of bookmark.
        # $OPT_NO_COLORS -> empty if not defined by user.
        then $GOSH_CORE "gosh_opt_remove" "$1" $OPT_NO_COLORS;

    elif [ $OPT_ADD = 1 ];
        # $1 -> The name of bookmark.
        # $2 -> The path - This could be empty, gosh-core will handle this.
        # $OPT_NO_COLORS -> empty if not defined by user.
        then $GOSH_CORE "gosh_opt_add" "$1" "$2" $OPT_NO_COLORS;

    elif [ $OPT_UPDATE = 1 ]; then
        # $1 -> The name of bookmark.
        # $2 -> The path - This could be empty, gosh-core will handle this.
        # $OPT_NO_COLORS -> empty if not defined by user.
        $GOSH_CORE "gosh_opt_update" "$1" "$2" $OPT_NO_COLORS;

    elif [ $OPT_PRINT = 1 ]; then
        # $1 -> The name of bookmark.
        # $OPT_NO_COLORS -> empty if not defined by user.
        echo $($GOSH_CORE "gosh_opt_print" "$1" $OPT_NO_COLORS);

    else
        # $1 -> The name of bookmark.
        # ALWAYS NO COLORS since it will be passed to cd(1) and
        # we don't want the escape chars on it.
        local RET_VAL=$($GOSH_CORE "gosh_opt_print" "$1");
        $GOSH_CORE "gosh_opt_print" "$1" > /dev/null;

        #The gosh-core call was successful?
        if [ $? = 0 ]; then
            #Change the directory.
            cd $RET_VAL;
            if [ -z "$OPT_NO_COLORS" ]; then
                echo "Gosh:"; tput setaf 5; echo " $RET_VAL"; tput sgr0;
            else
                echo "$RET_VAL";
            fi;
        else
            echo $RET_VAL;
        fi;
    fi;

}
