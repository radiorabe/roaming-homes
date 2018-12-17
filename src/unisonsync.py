#!/usr/bin/python
################################################################################
# unisonsync.py - Synchronize user profile with server
################################################################################
#
# Copyright (C) $( 2018 ) Radio Bern RaBe
#                    Switzerland
#                    http://www.rabe.ch
#
# This program is free software: you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public
# License as published  by the Free Software Foundation, version
# 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License  along with this program.
# If not, see <http://www.gnu.org/licenses/>.
#
# Please submit enhancements, bugfixes or comments via:
# https://github.com/radiorabe/roaming-homes
#
# Authors:
#  Simon Nussbaum <smirta@gmx.net>
#
# Description:
# <LONGER-DESCRIPTION>
#
# Usage:
# python unisonsync.py [options] hostname
#

import os
import subprocess
import optparse
from optparse import OptionParser
import imp

# Initialize libnotify for gnome if it's a x-session
havedisplay = "DISPLAY" in os.environ
if havedisplay:
    import gi
    gi.require_version('Notify', '0.7')
    from gi.repository import Notify
    from gi.repository import GLib
    main_loop = GLib.MainLoop()

# set default values
hostname = os.uname()[1]
servername = ''
serverport = '22'
unison_exec = '/usr/bin/unison'
xdgemail_exec = '/usr/bin/xdg-email'
ssh_exec = '/usr/bin/ssh'
messages_path = '/etc/roaming-homes/messages'

unison_cmd = [
            unison_exec, hostname+'-sync',
            '-ui', 'text',
            '-auto', '-batch'
]

# function to read predefined text from /etc/roaming-homes/messages
def getVarFromFile(filename):
    import imp
    f = open(filename)
    global data
    data = imp.load_source('data', '', f)
    f.close()

# run unison gui when the resolve button in the notification was clicked
def resolv_func(notification = None, action = None, user_data = None):
    os.spawnlp(os.P_NOWAIT, unison_exec, unison_exec, 
               str(hostname)+'-sync')
    close_func()

# open mail program with predefined text if "mailto" in the notification was clicked
def mailto_func(notification = None, action = None, user_data = None):
    mail_subject, mail_body, mail_receiver, cmd_output = user_data
    os.spawnlp(os.P_NOWAIT, xdgemail_exec, xdgemail_exec,
               '--subject', str(mail_subject),
               '--body', str(mail_body)+str(cmd_output),
               str(mail_receiver))
    close_func()

# close the notification if button or cross was clicked in the notification
def close_func(notification = None, action = None, user_data = None):
    main_loop.quit()
    quit()

def main ():
    # Initialize help menu
    usage = "usage: %prog [options] hostname"
    parser = OptionParser(usage)
    parser.add_option("-p", "--port", dest="port", default="22", help="SSH Port [default: %default]")
    parser.add_option("-s", "--ssh-path", dest="ssh_path", default="/usr/bin/ssh", help="Path to ssh binary [default: %default]")
    parser.add_option("-u", "--unison-path", dest="unison_path", default="/usr/bin/unison", help="Path to unison binary [default: %default]")
    parser.add_option("-e", "--email-path", dest="email_path", default="/usr/bin/xdg-email", help="Path to mail program binary [default: %default]")
    parser.add_option("-m", "--messages-path", 
                      dest="messages_path", 
                      default="/etc/roaming-homes/messages", 
                      help="Path to file containing predefined text " 
                           "\n\n[default: %default]")

    # get options and arguments passed
    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("incorrect number of arguments")
    if options.port:
        serverport = options.port
    if options.ssh_path:
        ssh_exec = options.ssh_path
    if options.unison_path:
        unison_exec = options.unison_path
    if options.email_path:
        email_exec = options.email_path
    if options.messages_path:
        messages_path = options.messages_path

    servername = args[0]

    # check if ssh server is reachable
    p = subprocess.Popen([ssh_exec, '-p', serverport, '-q', servername, 'exit'])
    p.wait()

    # if connection attempt to ssh server was successful, try to sync
    if p.returncode == 0:
        getVarFromFile(messages_path)

        try:
            cmd_output = str(subprocess.check_output(unison_cmd, stderr=subprocess.STDOUT))
        except subprocess.CalledProcessError as unisonexc:
            retcode = unisonexc.returncode
            cmd_output = unisonexc.output

            notify_str = str(data.notify_title)+' (Err: '+str(retcode)+')'
            print(notify_str+str(cmd_output))

            if havedisplay:

                Notify.init(str(data.notify_title))
                UHSf = Notify.Notification.new(str(data.notify_title), 
                                               str(data.notify_message), 
                                               'dialog-error')

                UHSf.connect('closed', close_func)

                UHSf.add_action(
                    'resolv_click',
                    str(data.notify_resolv),
                    resolv_func,
                    None # Arguments
                )

                UHSf.add_action(
                    'mailto_click',
                    str(data.notify_mail),
                    mailto_func,
                    data.mail_subject, data.mail_body, data.mail_receiver, cmd_output # Arguments
                )

                UHSf.add_action(
                    'ignore_click',
                    str(data.notify_ignore),
                    close_func,
                    None # Arguments
                )

                UHSf.show()
                main_loop.run()

main()