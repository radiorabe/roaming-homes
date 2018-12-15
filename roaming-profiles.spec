Name:           roaming-profiles
Version:        0.1 
Release:        1%{?dist}
Summary:        Roaming profiles using unison

License:        GPLv3+
URL:            https://github.com/radiorabe/fedora-rpm-roaming-profiles.git
Source0:        https://github.com/radiorabe/fedora-rpm-roaming-profiles/SOURCES

BuildRequires:  
Requires:       python
Requires:       unison

%description
Roaming profiles using unison and user systemd.

%prep
# no source


%build

%install
rm -rf $RPM_BUILD_ROOT
install -m 0755 -d $RPM_BUILD_ROOT/etc/roaming-profiles
install -m 0755 -d $RPM_BUILD_ROOT/usr/lib/roaming-profiles
install -m 0755 -d $RPM_BUILD_ROOT/usr/share/roaming-profiles
install -m 0755 -d $RPM_BUILD_ROOT/usr/share/roaming-profiles/unison
install -m 0755 -d $RPM_BUILD_ROOT/usr/share/doc/roaming-profiles

install -m 0644 roaming-profiles.conf $RPM_BUILD_ROOT/etc/roaming-profiles/roaming-profiles.conf
install -m 0644 defaults.conf $RPM_BUILD_ROOT/etc/roaming-profiles/defaults.conf
install -m 0644 messages $RPM_BUILD_ROOT/etc/roaming-profiles/messages

install -m 0644 unisonsetup.sh $RPM_BUILD_ROOT/etc/profiles.d/unisonsetup.sh

install -m 0644 unisonsync.sh $RPM_BUILD_ROOT/usr/lib/roaming-profiles/unisonsync.sh
install -m 0644 unisonsync.py $RPM_BUILD_ROOT/usr/lib/roaming-profiles/unisonsync.py

install -m 0644 common.prf $RPM_BUILD_ROOT/usr/share/roaming-profiles/unison/common.prf 
install -m 0644 home-dir.prf $RPM_BUILD_ROOT/usr/share/roaming-profiles/unison/home-dir.prf
install -m 0644 HOSTNAME-sync.prf $RPM_BUILD_ROOT/usr/share/roaming-profiles/unison/HOSTNAME-sync.prf

install -m 0644 unisonsync.timer $RPM_BUILD_ROOT/usr/lib/systemd/user/unisonsync.timer
install -m 0644 unisonsync.service $RPM_BUILD_ROOT/usr/lib/systemd/user/unisonsync.service

install -m 0644 readme.md $RPM_BUILD_ROOT/usr/share/doc/roaming-profiles/readme.md

echo -e "systemctl --user restart unisonsync.service" > /etc/skel/.bash_logout # run unison sync on bash logoff
echo -e '#!/bin/bash\n\systemctl --user restart unisonsync.service\n\nexit 0' > /etc/gdm/PostSession/Default # run unison sync on gdm logoff

systemctl --user --global enable unisonsync.timer

%files
/etc/roaming-profiles/roaming-profiles.conf
/etc/roaming-profiles/defaults.conf
/etc/roaming-profiles/messages
/etc/profile.d/unisonsetup.sh
/usr/lib/roaming-profiles/unisonsync.sh
/usr/lib/roaming-profiles/unisonsync.py
/usr/share/roaming-profiles/unison/common.prf
/usr/share/roaming-profiles/unison/home-dir.prf
/usr/share/roaming-profiles/unison/HOSTNAME-sync.prf
/usr/share/doc/roaming-profiles/readme.md
/usr/lib/systemd/user/unisonsync.timer
/usr/lib/systemd/user/unisonsync.service

%changelog
* Sat Dec 15 2018 Simon Nussbaum <smirta@gmx.net>
- Untested initial RPM 


