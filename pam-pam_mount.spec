# TODO
# - man -l pam_mount.8 | perl -pe 's/.\cH//g' >pam_mount.txt;
#   man: invalid option -- 'l'
#   man, version 1.6f
%define		modulename pam_mount
Summary:	A PAM module that can mount remote volumes for a user session
Summary(pl.UTF-8):	Moduł PAM, pozwalający montować zdalne zasoby na czas sesji użytkownika
Name:		pam-%{modulename}
Version:	2.20
Release:	1
License:	LGPL v2.1+ (library and PAM module), GPL v3+ (tools)
Group:		Base
Source0:	https://inai.de/files/pam_mount/%{modulename}-%{version}.tar.xz
# Source0-md5:	31a2275f389ed53f2fd35a82c5899b24
Source1:	%{name}.tmpfiles
URL:		https://inai.de/projects/pam_mount/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
BuildRequires:	cryptsetup-devel >= 1.1.2
BuildRequires:	glib2-devel
BuildRequires:	libHX-devel >= 3.12.1
BuildRequires:	libmount-devel >= 2.20
BuildRequires:	libtool
BuildRequires:	libxml2-devel >= 1:2.6
BuildRequires:	openssl-devel >= 0.9.8
BuildRequires:	pam-devel
BuildRequires:	pcre2-8-devel
BuildRequires:	pkgconfig
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz >= 1:4.999.7
BuildRequires:	zlib-devel
Obsoletes:	pam_mount
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This module is aimed to environments with SMB (Samba or Windows NT)
and/or NCP (Netware or Mars-NWE) servers that Unix users want or need
to access, and some users have / every user has private volumes in
that servers. The module also supports mounting home directories using
loopback encrypted filesystems (see also
http://www.tldp.org/HOWTO/Loopback-Encrypted-Filesystem-HOWTO.html).
 - Every user can access his/her own volumes
 - The user needs to type the password just once (at login) (*)
 - The mouting process is transparent to the users
 - There is no need to keep the login passwords in any additional file
 - The volumes are unmount upon logout, so it saves system resources,
   avoiding the need of listing every every possibly useful remote volume
   in /etc/fstab or in an automount/supermount config file. This is also
   necessary for securing encrypted filesystems.

(*) Obviously, the user password in the Unix system and in the remote
servers must be the same ;)

Pam_mount "understands" SMB, NCP, and encrypted loopback volumes, but
this can be extended very easily.

%description -l pl.UTF-8
Przeznaczeniem tego modułu są środowiska z protokołem SMB (Samba lub
Windows NT) i/lub NCP (Netware lub Mars-NWE), w których użytkownicy
chcą lub potrzebują indywidualnych zasobów. Moduł ten wspiera także
montowanie katalogów domowych z zaszyfrowanych systemów plików przy
użyciu loopbacka (zobacz także:
http://www.tldp.org/HOWTO/Loopback-Encrypted-Filesystem-HOWTO.html).
 - każdy użytkownik ma dostęp do swoich zasobów
 - użytkownik musi wpisać swoje hasło tylko raz (przy logowaniu) (*)
 - proces montowania jest niewidzialny dla użytkownika
 - nie ma potrzeby trzymania hasła i loginu w żadnym dodatkowym pliku
 - katalogi są odmontowywane podczas wylogowania, co oszczędza zasoby
   systemowe, zabezpiecza przed koniecznością umieszczenia każdego
   potrzebnego zdalnego zasobu w /etc/fstab lub w konfiguracji
   automounta/supermounta. Jest to także konieczne do zabezpieczenia
   zaszyfrowanych systemów plików.

(*) Oczywiście hasło na lokalnym i zdalnym systemie musi być
identyczne ;)

pam_mount "rozumie" SMB, NCP oraz zaszyfrowane systemy plików po
loopbacku, ale może być rozszerzony w prosty sposób.

%package -n libcryptmount
Summary:	libcryptmount library
Summary(pl.UTF-8):	Biblioteka libcryptmount
Group:		Libraries

%description -n libcryptmount
libcryptmount library.

%description -n libcryptmount -l pl.UTF-8
Biblioteka libcryptmount

%package -n libcryptmount-devel
Summary:	Header files for libcryptmount library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libcryptmount
Group:		Development/Libraries
Requires:	libcryptmount = %{version}-%{release}
Requires:	libHX-devel >= 3.12.1

%description -n libcryptmount-devel
Header files for libcryptmount library.

%description -n libcryptmount-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libcryptmount.

%prep
%setup -q -n %{modulename}-%{version}

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--with-rundir=/var/run \
	--with-slibdir=/%{_lib}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/security,/var/run/pam_mount,%{_bindir}} \
	$RPM_BUILD_ROOT%{systemdtmpfilesdir}

%{__make} -j1 install \
	moduledir=/%{_lib}/security \
	DESTDIR=$RPM_BUILD_ROOT

cp -a config/pam_mount.conf.xml $RPM_BUILD_ROOT/etc/security
ln -sf /sbin/mount.crypt $RPM_BUILD_ROOT%{_bindir}/mount.crypt

cp -p %{SOURCE1} $RPM_BUILD_ROOT%{systemdtmpfilesdir}/pam_mount.conf

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libcryptmount.la

%clean
rm -rf $RPM_BUILD_ROOT

%post   -n libcryptmount -p /sbin/ldconfig
%postun -n libcryptmount -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING doc/{bugs.rst,faq.txt,news.rst,options.txt,todo.txt}
%attr(755,root,root) /%{_lib}/security/pam_mount.so
%config(noreplace) %verify(not md5 mtime size) /etc/security/pam_mount.conf.xml
%attr(755,root,root) %{_bindir}/mount.crypt
%attr(755,root,root) %{_sbindir}/mount.crypt
%attr(755,root,root) %{_sbindir}/mount.crypt_LUKS
%attr(755,root,root) %{_sbindir}/mount.crypto_LUKS
%attr(755,root,root) %{_sbindir}/pmt-ehd
%attr(755,root,root) %{_sbindir}/pmvarrun
%attr(755,root,root) %{_sbindir}/umount.crypt
%attr(755,root,root) %{_sbindir}/umount.crypt_LUKS
%attr(755,root,root) %{_sbindir}/umount.crypto_LUKS
%dir /var/run/pam_mount
%{systemdtmpfilesdir}/pam_mount.conf
%{_mandir}/man5/pam_mount.conf.5*
%{_mandir}/man8/mount.crypt.8*
%{_mandir}/man8/mount.crypt_LUKS.8*
%{_mandir}/man8/mount.crypto_LUKS.8*
%{_mandir}/man8/pam_mount.8*
%{_mandir}/man8/pmt-ehd.8*
%{_mandir}/man8/pmvarrun.8*
%{_mandir}/man8/umount.crypt.8*
%{_mandir}/man8/umount.crypt_LUKS.8*
%{_mandir}/man8/umount.crypto_LUKS.8*

# TODO: for --with-selinux
#   /etc/selinux/strict/src/policy/file_contexts/misc/pam_mount.fc
#   /etc/selinux/strict/src/policy/macros/pam_mount_macros.te

%files -n libcryptmount
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcryptmount.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcryptmount.so.0

%files -n libcryptmount-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcryptmount.so
%{_includedir}/libcryptmount.h
%{_pkgconfigdir}/libcryptmount.pc
