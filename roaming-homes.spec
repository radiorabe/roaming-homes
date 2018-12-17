#
# spec file for package roaming-homes
#
# Copyright (c) 2018 Radio Bern RaBe
#                    http://www.rabe.ch
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# Please submit enhancements, bugfixes or comments via GitHub:
# https://github.com/radiorabe/roaming-homes
#

%undefine _disable_source_fetch

Name:           roaming-homes
Version:        master 
Release:        0%{?dist}
Summary:        Roaming homes/profiles using unison

License:        GPLv3+
URL:            https://github.com/radiorabe/roaming-homes
Source0:        https://github.com/radiorabe/roaming-homes/archive/%{version}/%{name}-%{version}.tar.gz

BuildArch:      noarch
Requires:       python
Requires:       unison

%description
Roaming homes/profiles using unison and user systemd.

%prep
%autosetup -n %{name}-%{version}


%build

%install
rm -rf %{buildroot}
install -m 0755 -d %{buildroot}/etc/%{name}
install -m 0755 -d %{buildroot}/etc/profile.d
install -m 0755 -d %{buildroot}/usr/lib/%{name}
install -m 0755 -d %{buildroot}/usr/lib/systemd/user
install -m 0755 -d %{buildroot}/usr/share/%{name}
install -m 0755 -d %{buildroot}/usr/share/%{name}/unison
install -m 0755 -d %{buildroot}/usr/share/doc/%{name}

install -m 0644 src/%{name}.conf %{buildroot}/etc/%{name}/%{name}.conf
install -m 0644 src/defaults.conf %{buildroot}/etc/%{name}/defaults.conf
install -m 0644 src/messages %{buildroot}/etc/%{name}/messages

install -m 0644 src/unisonsetup.sh %{buildroot}/etc/profile.d/unisonsetup.sh

install -m 0644 src/unisonsync.sh %{buildroot}/usr/lib/%{name}/unisonsync.sh
install -m 0644 src/unisonsync.py %{buildroot}/usr/lib/%{name}/unisonsync.py

install -m 0644 src/common.prf %{buildroot}/usr/share/%{name}/unison/common.prf 
install -m 0644 src/home-dir.prf %{buildroot}/usr/share/%{name}/unison/home-dir.prf
install -m 0644 src/HOSTNAME-sync.prf %{buildroot}/usr/share/%{name}/unison/HOSTNAME-sync.prf

install -m 0644 src/unisonsync.timer %{buildroot}/%{_userunitdir}/unisonsync.timer
install -m 0644 src/unisonsync.service %{buildroot}/%{_userunitdir}/unisonsync.service

install -m 0644 README.md %{buildroot}/usr/share/doc/%{name}/README.md
install -m 0644 LICENSE %{buildroot}/usr/share/doc/%{name}/LICENSE

%post
echo -e "systemctl --user restart unisonsync.service" >> /etc/skel/.bash_logout # run unison sync on bash logoff
sed -i 's/exit 0/systemctl --user restart unisonsync.service\n&/' /etc/gdm/PostSession/Default # run unison sync on gdm logoff
%systemd_user_post unisonsync.timer

%preun
%systemd_user_preun unisonsync.timer

%postun
sed -i '\!^systemctl --user restart unisonsync.service!d' /etc/skel/.bash_logout
sed -i '\!^systemctl --user restart unisonsync.service!d' /etc/gdm/PostSession/Default

%clean
rm -rf %{buildroot}

%files
/etc/%{name}/defaults.conf
/etc/%{name}/messages
/etc/profile.d/unisonsetup.sh
/usr/lib/%{name}/unisonsync.sh
/usr/lib/%{name}/unisonsync.py
/usr/lib/%{name}/unisonsync.pyc
/usr/lib/%{name}/unisonsync.pyo
/usr/share/%{name}/unison/common.prf
/usr/share/%{name}/unison/home-dir.prf
/usr/share/%{name}/unison/HOSTNAME-sync.prf
%{_userunitdir}/unisonsync.timer
%{_userunitdir}/unisonsync.service
%doc /usr/share/doc/%{name}/README.md
%license /usr/share/doc/%{name}/LICENSE
%dir /usr/lib/%{name}
%dir /usr/share/%{name}
%dir /usr/share/doc/%{name}
%dir /etc/%{name}
%config(noreplace) /etc/%{name}/%{name}.conf

%changelog
* Sat Dec 15 2018 Simon Nussbaum <smirta@gmx.net>
- Untested initial RPM 


