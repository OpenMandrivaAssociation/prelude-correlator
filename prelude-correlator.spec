Summary:        Correlates events from the prelude manager
Name:           prelude-correlator
Version:        1.0.1
Release:        6
Epoch:          0
License:        GPLv2+
Group:          System/Servers
URL:            http://www.prelude-ids.org/
Source0:        http://www.prelude-ids.com/download/releases/prelude-correlator/%{name}-%{version}.tar.gz
Source1:        prelude-correlator.service
Buildarch:	noarch
Requires:       prelude-manager
Requires:	python-prelude
Requires(preun): rpm-helper
Requires(post): rpm-helper
BuildRequires:	python-setuptools

%description
prelude-correlator correlates events from the prelude manager.

%prep

%setup -q -n %{name}-%{version}

cp %{SOURCE1} prelude-correlator.service

%build
python setup.py build

%install
python setup.py install --root=%{buildroot}

cat > README.urpmi << EOF
In order to start the prelude-correlator service you must configure it first.
This is not done automatically. To make a basic configuration,
please run:

%{_bindir}/prelude-adduser register prelude-correlator "idmef:rw" localhost --uid 0 --gid 0
EOF

install -d %{buildroot}%{_unitdir}
install -m0755 prelude-correlator.service %{buildroot}%{_unitdir}/prelude-correlator.service
install -d %{buildroot}/var/run/prelude-correlator

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%doc AUTHORS ChangeLog COPYING HACKING.README NEWS README.urpmi
%attr(0755,root,root) %{_bindir}/prelude-correlator
%attr(0755,root,root) %{_unitdir}/prelude-correlator.service
%{py_puresitedir}/*
%{_sysconfdir}/%{name}
%_var/lib/%{name}
