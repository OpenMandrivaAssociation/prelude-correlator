%define _localstatedir %{_var}

Summary:        Correlates events from the prelude manager
Name:           prelude-correlator
Version:        0.9.0
Release:        %mkrel 1
Epoch:          0
License:        GPLv2+
Group:          System/Servers
URL:            http://www.prelude-ids.org/
Source0:        http://www.prelude-ids.com/download/releases/prelude-correlator/prelude-correlator-0.9.0-beta3.tar.gz
Source1:        prelude-correlator.init
Patch0:         prelude-correlator-paths.patch
Requires:       prelude-manager
Requires(preun): rpm-helper
Requires(post): rpm-helper
BuildRequires:  libnotify-devel
BuildRequires:  libpcre-devel
BuildRequires:  lua5.1-devel
BuildRequires:  prelude-devel
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
prelude-correlator correlates events from the prelude manager.

%package devel
Summary:        Development headers for prelude-correlator
Group:          Development/C

%description devel
Development headers for prelude-correlator.

%prep
%setup -q -n %{name}-%{version}-beta3
#%%patch0 -p1
%{__perl} -pi -e 's|/usr/lib|%{_libdir}|g' configure.in
%{__autoconf}
%{__perl} -pi -e 's/(^include = nessus\.rules\;$)/#\1/' plugins/pcre/ruleset/pcre.rules

%build
%configure2_5x
%{make} 

%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}%{_sysconfdir}/prelude-correlator
%{makeinstall_std} 
%{__mkdir_p} %{buildroot}%{_initrddir}
%{__cp} -a %{SOURCE1} %{buildroot}%{_initrddir}/prelude-correlator
%{__mkdir_p} %{buildroot}/var/run/prelude-correlator

%{__cat} > README.urpmi << EOF
In order to start the prelude-correlator service you must configure it first.
This is not done automatically. To make a basic configuration,
please run:

%{_bindir}/prelude-adduser register prelude-correlator "idmef:rw" localhost --uid 0 --gid 0
EOF

%post
%_post_service prelude-correlator

%preun
%_preun_service prelude-correlator

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(0644,root,root,0755)
%doc AUTHORS ChangeLog COPYING HACKING.README INSTALL NEWS README.urpmi
%attr(0755,root,root) %{_bindir}/prelude-correlator
%dir %{_datadir}/prelude-correlator
%dir %{_datadir}/prelude-correlator/lua
%{_datadir}/prelude-correlator/lua/lib.lua
%attr(0755,root,root) %{_initrddir}/prelude-correlator
%dir %{_libdir}/prelude-correlator
%exclude %{_libdir}/prelude-correlator/lua.la
%attr(0755,root,root) %{_libdir}/prelude-correlator/lua.so
%dir %{_sysconfdir}/prelude-correlator
%config(noreplace) %{_sysconfdir}/prelude-correlator/prelude-correlator.conf
%dir %{_sysconfdir}/prelude-correlator/lua-rules
%config(noreplace) %{_sysconfdir}/prelude-correlator/lua-rules/*.lua
%dir %{_var}/run/prelude-correlator

%files devel
%defattr(0644,root,root,0755)
%dir %{_includedir}/prelude-correlator
%{_includedir}/prelude-correlator/prelude-correlator.h


