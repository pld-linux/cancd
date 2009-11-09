# TODO:
# - fix alpha build:
#  alpha-pld-linux-gcc -Wall -O2 -mieee  -DVERSION="\"0.1.0\""   -c -o cancd.o cancd.c
#  cancd.c: In function `setup_signals':
#  cancd.c:95: error: structure has no member named `sa_restorer'
#  make: *** [cancd.o] Error 1

Summary:	The CA NetConsole Daemon
Summary(pl.UTF-8):	Demon CA NetConsole
Name:		cancd
Version:	0.1.0
Release:	2
License:	GPL
Group:		Applications/File
Source0:	http://oss.oracle.com/projects/cancd/dist/files/source/%{name}-%{version}.tar.gz
# Source0-md5:	3eb4a75cfa4d1a860ea547fdc76c6d4d
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-make.patch
Patch1:		%{name}-nullterminate.patch
Patch2:		%{name}-c_cleanup.patch
Patch3:		%{name}-limits.patch
URL:		http://oss.oracle.com/projects/cancd/
BuildRequires:	rpmbuild(macros) >= 1.228
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	/sbin/chkconfig
Requires:	rc-scripts >= 0.4.0.17
Provides:	group(cancd)
Provides:	user(cancd)
ExcludeArch:	alpha
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is the CA NetConsole Daemon, a daemon to receive output from the
Linux netconsole driver.

%description -l pl.UTF-8
To jest demon CA NetConsole - demon odbierający wyjście z linuksowego
sterownika netconsole (konsoli sieciowej).

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p0

%build
%{__make} \
	CC="%{__cc}" \
	OPTFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{rc.d/init.d,sysconfig},/var/log/cancd}
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/cancd
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/cancd

%clean
rm -rf "$RPM_BUILD_ROOT"

%pre
%groupadd -g 162 cancd
%useradd -u 162 -c "CA NetConsole Daemon" -g cancd cancd

%post
/sbin/chkconfig --add cancd
%service cancd restart

%preun
if [ "$1" = "0" ]; then
	%service cancd stop
	/sbin/chkconfig --del cancd
fi

%postun
if [ "$1" = "0" ]; then
	%userremove cancd
	%groupremove cancd
fi

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/cancd
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/cancd
%attr(754,root,root) /etc/rc.d/init.d/cancd
%attr(770,root,cancd) %dir /var/log/cancd
