#/usr/bin/env bash
##~---------------------------------------------------------------------------##
##                     _______  _______  _______  _     _                     ##
##                    |   _   ||       ||       || | _ | |                    ##
##                    |  |_|  ||       ||   _   || || || |                    ##
##                    |       ||       ||  | |  ||       |                    ##
##                    |       ||      _||  |_|  ||       |                    ##
##                    |   _   ||     |_ |       ||   _   |                    ##
##                    |__| |__||_______||_______||__| |__|                    ##
##                             www.amazingcow.com                             ##
##  File      : install.sh                                                    ##
##  Project   : Gosh                                                          ##
##  Date      : Jan 02, 2018                                                  ##
##  License   : GPLv3                                                         ##
##  Author    : n2omatt <n2omatt@amazingcow.com>                              ##
##  Copyright : AmazingCow - 2018                                             ##
##                                                                            ##
##  Description :                                                             ##
##                                                                            ##
##---------------------------------------------------------------------------~##

##----------------------------------------------------------------------------##
## Helper Functions                                                           ##
##----------------------------------------------------------------------------##
warn()
{
    echo "[WARN]" "$1";
}

is_installed()
{
    RET=$(whereis -b $1 | cut -d":" -f2 | awk '{$1=$1};1' | cut -d" " -f1)

    if [ -n "$RET" ]; then
        return 0;
    fi;

    return 1;
}

find_real_user_home()
{
    ## Restore it at the end of the function.
    if [ $UID == 0 ]; then
        USER=$(printenv SUDO_USER);
        if [ -z "$USER" ]; then
            echo "Installing as root user...";
            export REAL_USER_HOME="$HOME";
        else
            echo "Installing with sudo...";
            export REAL_USER_HOME=$(getent passwd "$USER" | cut -d: -f6);
        fi;
    else
        echo "Installing as normal user...";
        export REAL_USER_HOME="$HOME";
    fi;
}


##----------------------------------------------------------------------------##
## Variables                                                                  ##
##----------------------------------------------------------------------------##
find_real_user_home;

BASH_PROFILE=$REAL_USER_HOME/.bashrc
DESTDIR=/usr/local/bin


##------------------------------------------------------------------------------
## Check if we have pkg-config
## COWTODO(n2omatt): Check another way to achieve that...
##  On BSD the pkg-config isn't equal to GNU one...
is_installed pkg-config;
if [ $? == 0 ]; then
    BASH_COMPLETION_DIR=$(pkg-config --variable=completionsdir bash-completion);
else
    warn "pkg-config isn't installed";
fi;


##----------------------------------------------------------------------------##
## Functions                                                                  ##
##----------------------------------------------------------------------------##
install_gosh()
{
    ##--------------------------------------------------------------------------
    ## Gosh.
    echo "--> Installing gosh.";
    echo "      .bashrc         location: ($BASH_PROFILE)";
    echo "      bash-completion location: ($BASH_COMPLETION_DIR)";
    echo "      destination     location: ($DESTDIR)";


    cp -f ./gosh-core.py  $DESTDIR/gosh-core
    cp -f ./gosh.sh       $DESTDIR/gosh

    chmod 755 $DESTDIR/gosh-core
    chmod 755 $DESTDIR/gosh

    echo "    [Done]";

    ##--------------------------------------------------------------------------
    ## Completion.
    echo "--> Install the bash completion script at ($BASH_COMPLETION_DIR).";

    if [ -n "$BASH_COMPLETION_DIR" ]; then
       cp -f ./gosh_bash-completion.sh $BASH_COMPLETION_DIR/gosh;
    else
       echo "    [SKIPPING] ($BASH_COMPLETION_DIR) does not exists...";
       echo "    You may want set BASH_COMPLETION_DIR to the actual dir.";
    fi

    echo "    [Done]";

    ##--------------------------------------------------------------------------
    ## Profile.
    echo "--> Make the backup of the original ($BASH_PROFILE).";

    cp $BASH_PROFILE ~/.bash_profile_gosh_backup

    grep -vi gosh $BASH_PROFILE > ~/.gosh_temp
    cat ~/.gosh_temp > $BASH_PROFILE
    rm ~/.gosh_temp

    echo "## AmazingCow - Gosh ##" >> $BASH_PROFILE;
    echo "source $DESTDIR/gosh"    >> $BASH_PROFILE;

    echo "    [Done]";


    ##--------------------------------------------------------------------------
    ## Done...
    echo "Everything done - Enjoy gosh :)"
}

uninstall_gosh()
{
    ##--------------------------------------------------------------------------
    ## Gosh
    echo "--> Uninstall gosh.";

    rm -f $DESTDIR/gosh-core;
    rm -f $DESTDIR/gosh;

    echo "    [Done]";

    ##--------------------------------------------------------------------------
    ## Completion.
    echo "--> Remove the bash completion script at ($BASH_COMPLETION_DIR).";

    if [ -f $BASH_COMPLETION_DIR/gosh ]; then
       rm -f $BASH_COMPLETION_DIR/gosh;
    else
       echo "    [SKIPPING] ($BASH_COMPLETION_DIR/gosh) does not exists...";
       echo "    You may want set BASH_COMPLETION_DIR to the actual dir.";
    fi

    echo "    [Done]";

    ##--------------------------------------------------------------------------
    ## Profile
    echo "--> Make the backup of the original ($BASH_PROFILE).";
    cp $BASH_PROFILE ~/.bash_profile_gosh_backup

    grep -vi gosh $BASH_PROFILE > ~/.gosh_temp
    cat ~/.gosh_temp > $BASH_PROFILE
    rm ~/.gosh_temp

    echo "    [Done]";

    ##--------------------------------------------------------------------------
    ## Done...
    echo "Everything done - I hope see you again :\`(";
}


##----------------------------------------------------------------------------##
## Script                                                                     ##
##----------------------------------------------------------------------------##
OPTION=$1;
if [ -z "$1" ] || [ "$1" == "install" ]; then
    install_gosh;
elif [ "$1" == "uninstall" ]; then
    uninstall_gosh;
else
    echo "Invalid option: ($1)";
    echo "Usage: install.sh [install] [uninstall]";
fi;
