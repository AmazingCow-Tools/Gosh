##----------------------------------------------------------------------------##
##               █      █                                                     ##
##               ████████                                                     ##
##             ██        ██                                                   ##
##            ███  █  █  ███                                                  ##
##            █ █        █ █        Makefile                                  ##
##             ████████████         Gosh    	                              ##
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

BASH_PROFILE=~/.bash_profile
BASH_COMPLETION_DIR=/etc/bash_completion

install:
	@ echo "---> Install gosh."
	cp -f ./gosh-core.py  /usr/local/bin/gosh-core
	cp -f ./gosh.sh       /usr/local/bin/gosh

	chmod 747 /usr/local/bin/gosh-core
	chmod 747 /usr/local/bin/gosh

	@ echo "\n---> Make the backup of the original ($(BASH_PROFILE))."
	cp $(BASH_PROFILE) ~/.bash_profile_gosh_backup

	@ echo "\n---> Clean up everything about the gosh from file."
	grep -vi gosh $(BASH_PROFILE) > ~/.gosh_temp
	mv ~/.gosh_temp $(BASH_PROFILE)

	@ echo "\n---> Add the lines to source the gosh program."
	echo "## AmazingCow - Gosh ##"    >> $(BASH_PROFILE)
	echo "source /usr/local/bin/gosh" >> $(BASH_PROFILE)

	@echo "\n---> Install the bash completion script at ($(BASH_COMPLETION_DIR))."
	@if [ -d $(BASH_COMPLETION_DIR) ]; then \
	   echo "cp -f ./_gosh.sh $(BASH_COMPLETION_DIR)"; \
	   cp -f ./_gosh.sh $(BASH_COMPLETION_DIR); \
	else \
	   echo "[SKIPPING] $(BASH_COMPLETION_DIR) does not exists..."; \
	   echo "You may want set BASH_COMPLETION_DIR to the actual dir."; \
	fi

	@echo "\n---> done..."


uninstall:
	@ echo "---> Remove gosh."
	rm -f /usr/local/bin/gosh
	rm -f /usr/local/bin/gosh-core

	@ echo "\n---> Make the backup of the original $(BASH_PROFILE)."
	cp $(BASH_PROFILE) ~/.bash_profile_gosh_backup

	@echo "\n---> Clean up everything about the gosh from $(BASH_PROFILE)."
	grep -vi gosh $(BASH_PROFILE) > ~/.gosh_temp
	mv ~/.gosh_temp $(BASH_PROFILE)

	@echo "\n---> Remove the bash completion script at ($(BASH_COMPLETION_DIR))."
	@if [ -f $(BASH_COMPLETION_DIR)/_gosh.sh ]; then \
	   echo "rm -f $(BASH_COMPLETION_DIR)/_gosh.sh"; \
	   rm -f $(BASH_COMPLETION_DIR)/_gosh.sh; \
	else \
	   echo "[SKIPPING] $(BASH_COMPLETION_DIR)/_gosh.sh does not exists..."; \
	   echo "You may want set BASH_COMPLETION_DIR to the actual dir."; \
	fi

	@echo "\n---> done..."
