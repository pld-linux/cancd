Summary:	The CA NetConsole Daemon
Name:		cancd
Version:	0.1.0
Release:	0.5
License:	GPL
Group:		Applications/File
Source0:	http://oss.oracle.com/projects/cancd/dist/files/source/%{name}-%{version}.tar.gz
# Source0-md5:	3eb4a75cfa4d1a860ea547fdc76c6d4d
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-make.patch
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
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is the CA NetConsole Daemon, a daemon to receive output from the
Linux netconsole driver.

%prep
%setup -q
%patch0 -p1

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
