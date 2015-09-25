#!/bin/bash
#COWTODO: Add the license.

#COWTODO: Comment.
alias losh-list="losh -l";
alias losh-add="losh -a";
alias losh-remove="losh -r";
alias losh-update="losh -u";
alias losh-go="losh ";

function losh
{
    #COWTODO: Change the path after.
    local GOSH_CORE=/Users/mesquitax/Documents/Projects/AmazingCow/OpenSource/Tools/Gosh/losh.py 

    #COWTODO: Comment.
    local OPT_HELP=0;
    local OPT_VERSION=0;
    local OPT_ADD=0;    
    local OPT_REMOVE=0;
    local OPT_UPDATE=0;
    local OPT_LIST=0;
    local OPT_NO_COLORS="";
    
    #COWTODO: Comment.
    if [ $# -eq 0 ]; then
        echo "NOA GASD";
        return;
    fi;

    #COWTODO: Comment.
    while getopts :hvaruln FLAG; do        
        case $FLAG in
             h) OPT_HELP=1      ;;
             v) OPT_VERSION=1   ;;
             l) OPT_LIST=1      ;;
             r) OPT_REMOVE=1    ;;
             a) OPT_ADD=1       ;;             
             u) OPT_UPDATE=1    ;;             
             n) OPT_NO_COLORS="no-colors" ;;
            \?) OPT_HELP=1      ;;
        esac
    done
    shift $((OPTIND-1))  #This tells getopts to move on to the next argument.

    #COWTODO: Check if this is ok to do?
    unset OPTARG;
    unset OPTIND;
    
    #COWTODO: Comment.
    if   [ $OPT_HELP    = 1 ]; then $GOSH_CORE "help";
    elif [ $OPT_VERSION = 1 ]; then $GOSH_CORE "version";        
    elif [ $OPT_LIST    = 1 ]; then $GOSH_CORE "list"         $OPT_NO_COLORS;
    elif [ $OPT_REMOVE  = 1 ]; then $GOSH_CORE "remove" $1    $OPT_NO_COLORS;
    elif [ $OPT_ADD     = 1 ]; then $GOSH_CORE "add"    $1 $2 $OPT_NO_COLORS;
    elif [ $OPT_UPDATE  = 1 ]; then $GOSH_CORE "update" $1 $2 $OPT_NO_COLORS;
        

    #COWTODO: Comment.
    else 
        GOSH_CMD=$($GOSH_CORE $1);
        RET_VAL=$(echo $GOSH_CMD | cut -d"#" -f1);
        RET_STR=$(echo $GOSH_CMD | cut -d"#" -f2);

        #COWTODO: This is very ugly, 
        #COWTODO: Comment.
        if [[ $RET_VAL = 0 ]]; then
            cd $RET_STR &&    \
            echo -n "Gosh: "; \
            tput setaf 5;     \
            echo $RET_STR;    \
            tput sgr0;
            return;
        
        #COWTODO: Comment.
        else
            echo $RET_STR;
            return;
        fi;
    
    fi; #COWTODO: Comment what if it's correspond.

}
