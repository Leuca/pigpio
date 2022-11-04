%global _description_python %{expand:
A python module which allows control of the General Purpose Input Outputs (GPIO).}
%global python_pigpio_version {{{ get_pigpio_python_version }}}
%global debug_package %{nil}

Name:           {{{ git_dir_name }}}
Version:        {{{ get_pigpio_version }}}
Release:        2%{?dist}
Summary:        C library for the Raspberry which allows control of the GPIO

ExclusiveArch:  aarch64 %{arm}

License:        Unlicense
URL:            https://github.com/joan2937/pigpio
VCS:            {{{ git_dir_vcs }}}

BuildRequires:  gcc
BuildRequires:  python3-devel
%if 0%{?rhel} < 9
BuildRequires:  python2-devel
%endif
BuildRequires:  systemd-rpm-macros

Source:         {{{ git_dir_pack }}}

Patch0:         pigpio-fix-sytemd-unit.patch

%if 0%{?rhel} < 9
%package -n     python2-{{{ git_dir_name }}}
Summary:        Python 2 module for the Raspberry which allows control of the GPIO
Requires:       %{name}%{?_isa} = %{version}-%{release}
BuildArch:      noarch
%endif

%package -n     python3-{{{ git_dir_name }}}
Summary:        Python 3 module for the Raspberry which allows control of the GPIO
Requires:       %{name}%{?_isa} = %{version}-%{release}
BuildArch:      noarch

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description
pigpio is a C library for the Raspberry which allows control of the General Purpose Input Outputs (GPIO).

%if 0%{?rhel} < 9
%description -n python2-{{{ git_dir_name }}} %_description_python
%endif

%description -n python3-{{{ git_dir_name }}} %_description_python

%description    devel
Development headers and shared libraries for %{name}

%prep
{{{ git_dir_setup_macro }}}
%autopatch -p1

%build
%make_build

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_mandir}/man1
mkdir -p %{buildroot}%{_mandir}/man3
mkdir -p %{buildroot}%{_includedir}
mkdir -p %{buildroot}%{_unitdir}
%if 0%{?rhel} < 9
mkdir -p %{buildroot}%{python2_sitelib}
%endif
mkdir -p %{buildroot}%{python3_sitelib}
%make_install prefix=%{_prefix} libdir=%{_libdir} mandir=%{_mandir}
install -m 0644 util/pigpiod.service %{buildroot}%{_unitdir}

%files
%license UNLICENCE
%doc README
/opt/pigpio/cgi
%{_libdir}/libpigpio.so.1
%{_libdir}/libpigpiod_if.so.1
%{_libdir}/libpigpiod_if2.so.1
%{_bindir}/pig2vcd
%{_bindir}/pigpiod
%{_bindir}/pigs
%{_mandir}/man1/pig2vcd.1.gz
%{_mandir}/man1/pigpiod.1.gz
%{_mandir}/man1/pigs.1.gz
%{_mandir}/man3/pigpio.3.gz
%{_mandir}/man3/pigpiod_if2.3.gz
%{_mandir}/man3/pigpiod_if.3.gz
%{_unitdir}/pigpiod.service

%files devel
%{_libdir}/libpigpio.so
%{_libdir}/libpigpiod_if.so
%{_libdir}/libpigpiod_if2.so
%{_includedir}/pigpio.h
%{_includedir}/pigpiod_if.h
%{_includedir}/pigpiod_if2.h

%if 0%{?rhel} < 9
%files -n python2-{{{ git_dir_name }}}
%license UNLICENCE
%{python2_sitelib}/pigpio-%{python_pigpio_version}-py%{python2_version}.egg-info
%{python2_sitelib}/pigpio.py
%{python2_sitelib}/pigpio.pyc
%{python2_sitelib}/pigpio.pyo
%endif

%files -n python3-{{{ git_dir_name }}}
%license UNLICENCE
%{python3_sitelib}/pigpio-%{python_pigpio_version}-py%{python3_version}.egg-info
%pycached %{python3_sitelib}/pigpio.py

%post
%systemd_post pigpiod.service

%preun
%systemd_preun pigpiod.service

%postun
%systemd_postun_with_restart pigpiod.service

%changelog
{{{ git_dir_changelog }}}
