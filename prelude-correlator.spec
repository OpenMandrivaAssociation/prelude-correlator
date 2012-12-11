%define _localstatedir %{_var}

Summary:        Correlates events from the prelude manager
Name:           prelude-correlator
Version:        1.0.1
Release:        1
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

%description
prelude-correlator correlates events from the prelude manager.

%prep

%setup -q -n %{name}-%{version}

cp %{SOURCE1} prelude-correlator.init

%build
python setup.py build

%install

python setup.py install --root=%buildroot

cat > README.urpmi << EOF
In order to start the prelude-correlator service you must configure it first.
This is not done automatically. To make a basic configuration,
please run:

%{_bindir}/prelude-adduser register prelude-correlator "idmef:rw" localhost --uid 0 --gid 0
EOF

install -d %{buildroot}%{_initrddir}
install -m0755 prelude-correlator.init %{buildroot}%{_initrddir}/prelude-correlator
install -d %{buildroot}/var/run/prelude-correlator

%post
%_post_service prelude-correlator

%preun
%_preun_service prelude-correlator

%files
%doc AUTHORS ChangeLog COPYING HACKING.README NEWS README.urpmi
%attr(0755,root,root) %{_bindir}/prelude-correlator
%attr(0755,root,root) %{_initrddir}/prelude-correlator
%python_sitelib/*
%_sysconfdir/%name
%_var/lib/%name


%changelog
* Mon Jul 16 2012 Oden Eriksson <oeriksson@mandriva.com> 0:1.0.1-1
+ Revision: 809794
- 1.0.1

* Thu Nov 04 2010 Funda Wang <fwang@mandriva.org> 0:1.0.0-2mdv2011.0
+ Revision: 593082
- BR setuptools
- rebuild for py2.7

* Sun Apr 25 2010 Funda Wang <fwang@mandriva.org> 0:1.0.0-1mdv2010.1
+ Revision: 538676
- 1.0.0

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

* Sun Aug 10 2008 David Walluck <walluck@mandriva.org> 0:0.9.0-1mdv2009.0
+ Revision: 270121
- BuildRequires: lua5.1-devel
- 0.9.0-beta3

* Tue Jan 22 2008 Funda Wang <fwang@mandriva.org> 0:0.9.0-0.8775.2mdv2008.1
+ Revision: 156134
- BR prelude-devel
- rebuild against latest gnutls

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

