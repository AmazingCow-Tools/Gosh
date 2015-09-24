BASH_PROFILE=~/.bash_profile

install:
	#Install gosh.
	cp -f ./gosh.sh /usr/local/bin/gosh

	#Make the backup of the original bash_profile.
	cp $(BASH_PROFILE) ~/.bash_profile_gosh_backup

	#Clean up everything about the gosh from file.
	grep -vi gosh $(BASH_PROFILE) > ~/.gosh_temp
	mv ~/.gosh_temp $(BASH_PROFILE)

	#Add the lines to source the gosh program.
	echo "## AmazingCow - Gosh ##"    >> $(BASH_PROFILE)
	echo "source /usr/local/bin/gosh" >> $(BASH_PROFILE)

uninstall:
	#Remove gosh.
	sudo rm -rf /usr/local/bin/gosh

	#Make the backup of the original bash_profile.
	cp $(BASH_PROFILE) ~/.bash_profile_gosh_backup

	#Clean up everything about the gosh from file.
	grep -vi gosh $(BASH_PROFILE) > ~/.gosh_temp
	mv ~/.gosh_temp $(BASH_PROFILE)
