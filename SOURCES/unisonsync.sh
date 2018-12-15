#!/bin/sh
################################################################################
# unisonsync.sh - Start unisonsync.py with environment variables as arguments
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
# https://github.com/radiorabe/roaming-profiles
#
# Authors:
#  Simon Nussbaum <smirta@gmx.net>
#
# Description:
# <LONGER-DESCRIPTION>
#

RP_CONF_DIR="/etc/roaming-profiles"
source "${RP_CONF_DIR%/}/roaming-profiles.conf"
source "${RP_CONF_DIR%/}/defaults.conf"

userExclusionList=${USER_EXC_LIST}

if [[ ! ${userExclusionList[*]} =~ ${USER} ]]
then
  python "${RP_LIB_DIR%/}/unisonsync.py" --port="${SSH_PORT}" \
                                         --ssh-path="${SSH_EXEC}" \
                                         --unison-path="${UNISON_EXEC}" \
                                         --email-path="${MAIL_EXEC}" \
                                         --messages-path="${MESSAGES_PATH}" \
                                         "${SSH_SERVER}"

fi
