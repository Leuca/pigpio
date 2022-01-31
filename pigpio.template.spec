%global subver %(curl https://raw.githubusercontent.com/joan2937/pigpio/master/pigpio.h | sed -ne '/VERSION/p' | cut -d" " -f 3)
%global pigpio_version 1.%{subver}
%global _description_python %{expand:
A python module which allows control of the General Purpose Input Outputs (GPIO).}

Name:       {{{ git_dir_name }}}
Version:    %{pigpio_version}_{{{ git_dir_version }}}
Release:    %{?dist}
Summary:    C library for the Raspberry which allows control of the GPIO

ExclusiveArch:  aarch64 %{arm}

License:    Unlicense
URL:        https://github.com/joan2937/pigpio
VCS:        {{{ git_dir_vcs }}}

BuildRequires: gcc python3-devel
%if 0%{?rhel} < 9
BuildRequires: python2-devel
%endif

Source:     {{{ git_dir_pack }}}

%if 0%{?rhel} < 9
%package -n python2-{{{ git_dir_name }}}
Summary:    Python 2 module for the Raspberry which allows control of the GPIO
Requires:   {{{ git_dir_name }}}
BuildArch:  noarch
%endif

%package -n python3-{{{ git_dir_name }}}
Summary:    Python 3 module for the Raspberry which allows control of the GPIO
Requires:   {{{ git_dir_name }}}
BuildArch:  noarch

%description
pigpio is a C library for the Raspberry which allows control of the General Purpose Input Outputs (GPIO).

%if 0%{?rhel} < 9
%description -n python2-{{{ git_dir_name }}} %_description_python
%endif

%description -n python3-{{{ git_dir_name }}} %_description_python

%prep
{{{ git_dir_setup_macro }}}

%build
make

%install
make DESTDIR=%{buildroot} prefix=%{_prefix} libdir=%{_libdir} mandir=%{_mandir} install
mkdir -p %{buildroot}/%{_prefix}/lib/systemd/system
install -m 0644 util/pigpiod.service %{buildroot}/%{_prefix}/lib/systemd/system

%files
%license UNLICENCE
# %doc README
/opt/pigpio/cgi
%{_includedir}/pigpio.h
%{_includedir}/pigpiod_if.h
%{_includedir}/pigpiod_if2.h
%{_libdir}/libpigpio.so.1
%{_libdir}/libpigpiod_if.so.1
%{_libdir}/libpigpiod_if2.so.1
%{_libdir}/libpigpio.so
%{_libdir}/libpigpiod_if.so
%{_libdir}/libpigpiod_if2.so
%{_bindir}/pig2vcd
%{_bindir}/pigpiod
%{_bindir}/pigs
%{_mandir}/man1
%{_mandir}/man3
%{_mandir}/man1/pig2vcd.1
%{_mandir}/man1/pigpiod.1
%{_mandir}/man1/pigs.1
%{_mandir}/man3/pigpio.3
%{_mandir}/man3/pigpiod_if2.3
%{_mandir}/man3/pigpiod_if.3
%{_prefix}/lib/systemd/system/pigpiod.service

%if 0%{?rhel} < 9
%files -n python2-{{{ git_dir_name }}}
%license UNLICENCE
%{python2_sitelib}/pigpio-%{pigpio_version}-py%{python2_version}.egg-info
%{python2_sitelib}/pigpio.py
%{python2_sitelib}/pigpio.pyc
%endif

%files -n python3-{{{ git_dir_name }}}
%license UNLICENCE
%{python3_sitelib}/pigpio-%{pigpio_version}-py%{python3_version}.egg-info
%pycached %{python3_sitelib}/pigpio.py

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%changelog
{{{ git_dir_changelog }}}
