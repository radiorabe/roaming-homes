#!/bin/sh
################################################################################
# unisonsetup.sh - Setup of unison to provide roaming profiles
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
# Usage:
# sh unisonsetup.sh
#

# load variables from config file
RP_CONF_DIR="/etc/roaming-profiles"
source "${RP_CONF_DIR%/}/roaming-profiles.conf"
source "${RP_CONF_DIR%/}/defaults.conf"

# if user is in the exclusion list, skip
userExclusionList=${USER_EXC_LIST}

if [[ ! ${userExclusionList[*]} =~ ${USER} ]]
then

# if unison user settings directory doesn't exist, create it
[ ! -e "${UNISON_DIR}" ] && mkdir "${UNISON_DIR}"

# if the configuration file is newer than unison user settings or some preference files are missing
# (re-)create the files
if [ "${RP_CONF_DIR%/}/roaming-profiles.conf" -nt "${UNISON_DIR%/}/${HOSTNAME}-sync.prf" ] \
   || [ ! -e "${UNISON_DIR%/}/common.prf" ] \
   || [ ! -e "${UNISON_DIR%/}/home-dir.prf" ] \
   || [ ! -e "${UNISON_DIR%/}/${HOSTNAME}-sync.prf" ]
then
  /usr/bin/cp "${RP_SHARE_DIR%/}/unison/"{common.prf,home-dir.prf} "${UNISON_DIR%/}/"
  eval "echo \"$(<${RP_SHARE_DIR%/}/unison/HOSTNAME-sync.prf)\"" > "${UNISON_DIR%/}/${HOSTNAME}-sync.prf"

  printf "ignore = Name %s\n" "${IGNORE_NAME_LIST[@]}" >> "${UNISON_DIR%/}/common.prf"
  printf "ignore = Path %s\n" "${UNISON:-.unison}" >> "${UNISON_DIR%/}/common.prf"
  printf "ignore = Path %s\n" "${IGNORE_PATH_LIST[@]}" >> "${UNISON_DIR%/}/common.prf"
  printf "path = %s\n" "${INCLUDE_PATH_LIST[@]}" >> "${UNISON_DIR%/}/home-dir.prf"

fi

# Make sure only english folder names are used
LC_ALL=C xdg-user-dirs-update
echo "de_CH" > ${HOME_DIR%/}/.config/user-dirs.locale

# ignore archives that might exist on the server when logging in the first time on this host
if [ ! -e "${UNISON_DIR%/}/firstrun" ]
then
  ${UNISON_EXEC} "${HOSTNAME}-sync" -ui text -batch -auto -silent -terse -ignorearchives > /dev/null 2>&1
  touch "${UNISON_DIR%/}/firstrun"
else
  ${UNISON_EXEC} "${HOSTNAME}-sync" -ui text -batch -auto -silent -terse > /dev/null 2>&1
fi

fi
