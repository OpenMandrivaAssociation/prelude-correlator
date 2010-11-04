%define _localstatedir %{_var}

Summary:        Correlates events from the prelude manager
Name:           prelude-correlator
Version:        1.0.0
Release:        %mkrel 2
Epoch:          0
License:        GPLv2+
Group:          System/Servers
URL:            http://www.prelude-ids.org/
Source0:        http://www.prelude-ids.com/download/releases/prelude-correlator/%name-%version.tar.gz
Source1:        prelude-correlator.init
Buildarch:	noarch
Requires:       prelude-manager
Requires(preun): rpm-helper
Requires(post): rpm-helper
Obsoletes:	%name < 0:1.0.0
BuildRequires:	python-setuptools
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
prelude-correlator correlates events from the prelude manager.

%prep
%setup -q -n %{name}-%{version}

%build
python setup.py build

%install
%{__rm} -rf %{buildroot}
python setup.py install --root=%buildroot

%{__cat} > README.urpmi << EOF
In order to start the prelude-correlator service you must configure it first.
This is not done automatically. To make a basic configuration,
please run:

%{_bindir}/prelude-adduser register prelude-correlator "idmef:rw" localhost --uid 0 --gid 0
EOF

%{__mkdir_p} %{buildroot}%{_initrddir}
%{__cp} -a %{SOURCE1} %{buildroot}%{_initrddir}/prelude-correlator
%{__mkdir_p} %{buildroot}/var/run/prelude-correlator

%post
%_post_service prelude-correlator

%preun
%_preun_service prelude-correlator

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(0644,root,root,0755)
%doc AUTHORS ChangeLog COPYING HACKING.README NEWS README.urpmi
%attr(0755,root,root) %{_bindir}/prelude-correlator
%attr(0755,root,root) %{_initrddir}/prelude-correlator
%python_sitelib/*
%_sysconfdir/%name
%_var/lib/%name
