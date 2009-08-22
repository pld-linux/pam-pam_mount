# TODO
# - man -l pam_mount.8 | perl -pe 's/.\cH//g' >pam_mount.txt;
#   man: invalid option -- 'l'
#   man, version 1.6f
%define 	modulename pam_mount
Summary:	A PAM module that can mount remote volumes for a user session
Summary(pl.UTF-8):	Moduł PAM, pozwalający montować zdalne zasoby na czas sesji użytkownika
Name:		pam-%{modulename}
Version:	1.27
Release:	1
Epoch:		0
License:	LGPL
Group:		Base
Source0:	http://dl.sourceforge.net/pam-mount/%{modulename}-%{version}.tar.bz2
# Source0-md5:	f06da34db9d578c40f3d47b394f9c5a3
URL:		http://pam-mount.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	glib2-devel
BuildRequires:	libHX-devel
BuildRequires:	libtool
BuildRequires:	libxml2-devel
BuildRequires:	openssl-devel >= 0.9.8
BuildRequires:	pam-devel
BuildRequires:	pkgconfig
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

%prep
%setup -q -n %{modulename}-%{version}

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-static
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/security,/sbin}

%{__make} install \
	moduledir=/%{_lib}/security \
	DESTDIR=$RPM_BUILD_ROOT

install config/pam_mount.conf.xml $RPM_BUILD_ROOT/etc/security
ln -sf /sbin/mount.crypt $RPM_BUILD_ROOT%{_bindir}/mount.crypt

rm -f $RPM_BUILD_ROOT/%{_lib}/security/pam_mount.la

# void code on non-OpenBSD, besides broken
rm -f $RPM_BUILD_ROOT{%{_bindir}/mount_ehd,%{_mandir}/man8/mount_ehd.8}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/security/pam_mount.so
%config(noreplace) %verify(not md5 mtime size) /etc/security/pam_mount.conf.xml
%attr(755,root,root) /sbin/mount.crypt
%attr(755,root,root) /sbin/mount.crypt_LUKS
%attr(755,root,root) /sbin/mount.crypto_LUKS
%attr(755,root,root) /sbin/mount.encfs13
%attr(755,root,root) /sbin/umount.crypt
%attr(755,root,root) /sbin/umount.crypt_LUKS
%attr(755,root,root) /sbin/umount.crypto_LUKS
%attr(755,root,root) %{_bindir}/mount.crypt
%attr(755,root,root) %{_bindir}/pmt-fd0ssh
%attr(755,root,root) %{_bindir}/pmt-ofl
%attr(755,root,root) %{_sbindir}/pmt-ehd
%attr(755,root,root) %{_sbindir}/pmvarrun
%{_mandir}/man1/pmt-fd0ssh.1*
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
