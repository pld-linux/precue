Summary:	This application is used as a web/mobile frontend to Lyricue
Name:		precue
Version:	1.9
Release:	0.1
License:	GPL
Group:		Applications/WWW
Source0:	https://launchpad.net/~chris-debenham/+archive/lyricue/+files/%{name}_%{version}lucid.tar.gz
# Source0-md5:	2365e75164ad8b76175c82734e326fee
URL:		http://www.lyricue.org/precue/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	webapps
%if %{with trigger}
Requires(triggerpostun):	sed >= 4.0
%endif
Requires:	php-mysql
Requires:	webserver(indexfile)
Requires:	webserver(php)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

%description
With Precue you can provide users access to your lyricue installation
in order to check what songs are available, add/edit/remove playlists
and add new songs

%prep
%setup -q -n %{name}

cat > apache.conf <<'EOF'
Alias /%{name} %{_appdir}
<Directory %{_appdir}>
	Allow from all
</Directory>
EOF

cat > lighttpd.conf <<'EOF'
alias.url += (
    "/%{name}" => "%{_appdir}",
)
EOF

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir}}

cp -a apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -a apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
cp -a lighttpd.conf $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf
mv {includes,$RPM_BUILD_ROOT%{_sysconfdir}}/config.inc
mv {,.}htaccess

install -d images $RPM_BUILD_ROOT%{_appdir}/images/
install -d includes $RPM_BUILD_ROOT%{_appdir}/includes/
install .htaccess $RPM_BUILD_ROOT%{_appdir}/
install *.{php,js,css} $RPM_BUILD_ROOT%{_appdir}/
install blank.html $RPM_BUILD_ROOT%{_appdir}/
install images/*.{jpg,png,svg} $RPM_BUILD_ROOT%{_appdir}/images/
install includes/*.inc $RPM_BUILD_ROOT%{_appdir}/includes/
install includes/.htaccess $RPM_BUILD_ROOT%{_appdir}/includes/

ln -sf %{_sysconfdir}/config.inc $RPM_BUILD_ROOT%{_appdir}/includes/config.inc

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerin -- lighttpd
%webapp_register lighttpd %{_webapp}

%triggerun -- lighttpd
%webapp_unregister lighttpd %{_webapp}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README CHANGELOG
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/config.inc
%{_appdir}
