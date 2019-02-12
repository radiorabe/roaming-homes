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
install -m 0755 -d %{buildroot}%{_sysconfdir}/%{name}
install -m 0755 -d %{buildroot}%{_sysconfdir}/profile.d
install -m 0755 -d %{buildroot}%{_libdir}/%{name}
install -m 0755 -d %{buildroot}%{_userunitdir}
install -m 0755 -d %{buildroot}%{_datadir}/%{name}
install -m 0755 -d %{buildroot}%{_datadir}/%{name}/unison
install -m 0755 -d %{buildroot}%{_docdir}/%{name}

install -m 0644 src/%{name}.conf %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf
install -m 0644 src/defaults.conf %{buildroot}%{_sysconfdir}/%{name}/defaults.conf
install -m 0644 src/messages %{buildroot}%{_sysconfdir}/%{name}/messages

install -m 0644 src/unisonsetup.sh %{buildroot}%{_sysconfdir}/profile.d/unisonsetup.sh

install -m 0644 src/unisonsync.sh %{buildroot}%{_libdir}/%{name}/unisonsync.sh
install -m 0644 src/unisonsync.py %{buildroot}%{_libdir}/%{name}/unisonsync.py

install -m 0644 src/common.prf %{buildroot}%{_datadir}/%{name}/unison/common.prf 
install -m 0644 src/home-dir.prf %{buildroot}%{_datadir}/%{name}/unison/home-dir.prf
install -m 0644 src/HOSTNAME-sync.prf %{buildroot}%{_datadir}/%{name}/unison/HOSTNAME-sync.prf

install -m 0644 src/unisonsync.timer %{buildroot}/%{_userunitdir}/unisonsync.timer
install -m 0644 src/unisonsync.service %{buildroot}/%{_userunitdir}/unisonsync.service

install -m 0644 README.md %{buildroot}%{_docdir}/%{name}/README.md
install -m 0644 LICENSE %{buildroot}%{_docdir}/%{name}/LICENSE

%post
echo -e "systemctl --user restart unisonsync.service" >> %{_sysconfdir}/skel/.bash_logout # run unison sync on bash logoff
sed -i 's/exit 0/systemctl --user restart unisonsync.service\n&/' %{_sysconfdir}/gdm/PostSession/Default # run unison sync on gdm logoff
%systemd_user_post unisonsync.timer

%preun
%systemd_user_preun unisonsync.timer

%postun
sed -i '\!^systemctl --user restart unisonsync.service!d' %{_sysconfdir}/skel/.bash_logout
sed -i '\!^systemctl --user restart unisonsync.service!d' %{_sysconfdir}/gdm/PostSession/Default

%clean
rm -rf %{buildroot}

%files
%{_sysconfdir}/%{name}/defaults.conf
%{_sysconfdir}/%{name}/messages
%{_sysconfdir}/profile.d/unisonsetup.sh
%{_libdir}/%{name}/unisonsync.sh
%{_libdir}/%{name}/unisonsync.py
%{_libdir}/%{name}/unisonsync.pyc
%{_libdir}/%{name}/unisonsync.pyo
%{_datadir}/%{name}/unison/common.prf
%{_datadir}/%{name}/unison/home-dir.prf
%{_datadir}/%{name}/unison/HOSTNAME-sync.prf
%{_userunitdir}/unisonsync.timer
%{_userunitdir}/unisonsync.service
%doc %{_docdir}/%{name}/README.md
%license %{_docdir}/%{name}/LICENSE
%dir %{_libdir}/%{name}
%dir %{_datadir}/%{name}
%dir %{_docdir}/%{name}
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf

%changelog
* Mon Feb 11 2019 Simon Nussbaum <smirta@gmx.net>
- Replaced paths with macros

* Sat Dec 15 2018 Simon Nussbaum <smirta@gmx.net>
- Untested initial RPM 

