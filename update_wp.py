#!/usr/bin/python


# Copyright 2013
# Eyedarts Website Creations
# (http://eyedarts.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import sys, os
from fabric.api import hosts, local, settings, abort, run, cd, env
from fabric.contrib.console import confirm

WP_SITES_LOCAL="wp_sites_local.txt"
WP_SITES_SSH="ssh_sites.txt"

def Does_File_Exist(file):
    '''
    This function checks to make sure a file exists.
    '''
    try:
        with open(file):
            return True
    except IOError:
           print ("\nCan't find \033[31m%s\033[0m\n" % file)

def set_hosts(host, user):
    env.host_string = host
    env.user = user

def Questions_For_Updates(site_path, site_name, type, loc, host):
    '''
    This function formats and displays the questions for updating plugins and themes.
    '''
    # Display list
    print ("\nListing \033[33m%ss\033[0m for \033[33m%s\033[0m" % (type, site_name))
    if loc == 'l':
        local("wp --path=%s %s list" % (site_path, type))
    if loc == 'r':
        run("wp --path=%s %s list" % (site_path, type))

    # Ask which to update
    answer = raw_input("Which \033[33m%ss\033[0m do you want to update?\n(\033[33ma\033[0m)ll, (\033[33mn\033[0m)one, or enter %ss separated by spaces\n" % (type, type))

    if answer == 'a':
        # update all plugins that have updates available
        print ("Updating \033[33mall\033[0m %ss" % type)
        if loc =='l':
            local("wp --path=%s %s update-all version-latest" % (site_path, type))
        if loc =='r':
            run("wp --path=%s %s update-all version-latest" % (site_path, type))
        
    elif answer == 'n':
        # don't update any plugins
        print ("No \033[33m%ss\033[0m have been updated." % type)

    else:
        # update selected plugins
        if loc == 'l':
            for ans in answer.split(' '):
                print ("Updating \033[33m%s\033[0m %s." % (ans, type))
                local ("wp --path=%s %s update %s" % (site_path, type, ans))

        if loc == 'r':
            for ans in answer.split(' '):
                print ("Updating \033[33m%s\033[0m %s." % (ans, type))
                run ("wp --path=%s %s update %s" % (site_path, type, ans))

def update_core(site_name, site_path, loc):
    core_answer = raw_input("Do you want to update \033[33mWP Core\033[0m for \033[33m%s\033[0m? (\033[33my\033[0m/\033[33mn\033[0m)\n" % site_name)

    if core_answer == 'y':
        print ("Updating \033[33mWP Core\033[0m for \033[33m%s\033[0m" % site_name)
        if loc == 'l':
            local("wp --path=%s core update" % site_path)
        if loc =='r':
            run("wp --path=%s core update" % site_path)

    if core_answer =='n':
        print ("\033[33mWP Core\033[0m not updated for \033[33m%s\033[0m." % site_name)

                                                
### Local Sites Section ###

if Does_File_Exist(WP_SITES_LOCAL):
    # if file exists, open file and read each line into a list
    with open(WP_SITES_LOCAL, 'r') as f:
        sites = f.readlines()

    # go through each site and run WP-CLI commands
    for site in sites:
        # format site path for better use
        site_path = site.rstrip('\n')
        site_name = site_path.split('/')[-1]
        host = ''

        # print the lists and ask the user which to update
        Questions_For_Updates(site_path, site_name, 'plugin', 'l', host)
        Questions_For_Updates(site_path, site_name, 'theme', 'l', host)

        # start WP core update process
        update_core(site_name, site_path, 'l')
        
else:
    # Exit if file cannot be found.
    sys.exit()


### Start SSH Section ###
    
if Does_File_Exist(WP_SITES_SSH):
    # if file exists, open file and read each line into a list
    with open(WP_SITES_SSH, 'r') as f:
        sites = f.readlines()

    # go through each site and run WP-CLI commands
    for site in sites:
        # format site path for better use
        site = site.replace(',', '\n').rsplit('\n')
        site_name = site[0].split('@')
        site_path = site[1]
        host = site[0]
        set_hosts(site_name[-1], site_name[0])

        # print the lists and ask the user which to update
        Questions_For_Updates(site_path, site_name[-1], 'plugin', 'r', host)
        Questions_For_Updates(site_path, site_name[-1], 'theme', 'r', host) 

        # start WP Core update process
        update_core(site_name[-1], site_path, 'r')

else:
    # Exit if file cannot be found.
    sys.exit() 


print ('''\n\032[34m***************************************\n
     Updates Completed Successfully!\n
***************************************\033[0m\n''')
