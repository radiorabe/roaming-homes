Name:           roaming-homes
Version:        master 
Release:        0%{?dist}
Summary:        Roaming homes/profiles using unison

License:        GPLv3+
URL:            https://github.com/radiorabe/roaming-homes
Source0:        https://github.com/radiorabe/roaming-homes/archive/%{version}/%{name}-%{version}.tar.gz

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

install -m 0644 %{name}.conf %{buildroot}/etc/%{name}/%{name}.conf
install -m 0644 defaults.conf %{buildroot}/etc/%{name}/defaults.conf
install -m 0644 messages %{buildroot}/etc/%{name}/messages

install -m 0644 unisonsetup.sh %{buildroot}/etc/profile.d/unisonsetup.sh

install -m 0644 unisonsync.sh %{buildroot}/usr/lib/%{name}/unisonsync.sh
install -m 0644 unisonsync.py %{buildroot}/usr/lib/%{name}/unisonsync.py

install -m 0644 common.prf %{buildroot}/usr/share/%{name}/unison/common.prf 
install -m 0644 home-dir.prf %{buildroot}/usr/share/%{name}/unison/home-dir.prf
install -m 0644 HOSTNAME-sync.prf %{buildroot}/usr/share/%{name}/unison/HOSTNAME-sync.prf

install -m 0644 unisonsync.timer %{buildroot}/%{_userunitdir}/unisonsync.timer
install -m 0644 unisonsync.service %{buildroot}/%{_userunitdir}/unisonsync.service

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


