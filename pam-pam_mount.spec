%define 	modulename pam_mount
Summary:	A PAM module that can mount remote volumes for a user session
Summary(pl):	Modu� PAM, pozwalaj�cy montowa� zdalne zasoby na czas sesji u�ytkownika
Name:		pam-%{modulename}
Version:	0.18
Release:	2
Epoch:		0
License:	LGPL
Group:		Base
Source0:	http://dl.sourceforge.net/pam-mount/%{modulename}-%{version}.tar.bz2
# Source0-md5:	c2e2a7eee61596a8c72d79d8bba3538d
URL:		http://pam-mount.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	glib2-devel
BuildRequires:	libtool
BuildRequires:	openssl-devel >= 0.9.7d
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

%description -l pl
Przeznaczeniem tego modu�u s� �rodowiska z protoko�em SMB (Samba lub
Windows NT) i/lub NCP (Netware lub Mars-NWE), w kt�rych u�ytkownicy
chc� lub potrzebuj� indywidualnych zasob�w. Modu� ten wspiera tak�e
montowanie katalog�w domowych z zaszyfrowanych system�w plik�w przy
u�yciu loopbacka (zobacz tak�e:
http://www.tldp.org/HOWTO/Loopback-Encrypted-Filesystem-HOWTO.html).
 - ka�dy u�ytkownik ma dost�p do swoich zasob�w
 - u�ytkownik musi wpisa� swoje has�o tylko raz (przy logowaniu) (*)
 - proces montowania jest niewidzialny dla u�ytkownika
 - nie ma potrzeby trzymania has�a i loginu w �adnym dodatkowym pliku
 - katalogi s� odmontowywane podczas wylogowania, co oszcz�dza zasoby
   systemowe, zabezpiecza przed konieczno�ci� umieszczenia ka�dego
   potrzebnego zdalnego zasobu w /etc/fstab lub w konfiguracji
   automounta/supermounta. Jest to tak�e konieczne do zabezpieczenia
   zaszyfrowanych system�w plik�w.

(*) Oczywi�cie has�o na lokalnym i zdalnym systemie musi by�
identyczne ;)

pam_mount "rozumie" SMB, NCP oraz zaszyfrowane systemy plik�w po
loopbacku, ale mo�e by� rozszerzony w prosty spos�b.

%prep
%setup -q -n %{modulename}-%{version}

%build
%{__libtoolize}
%{__aclocal}
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

install config/pam_mount.conf $RPM_BUILD_ROOT/etc/security
ln -sf /sbin/mount.crypt $RPM_BUILD_ROOT/%{_bindir}/mount.crypt

rm -f $RPM_BUILD_ROOT/%{_lib}/security/pam_mount.la

# void code on non-OpenBSD, besides broken
rm -f $RPM_BUILD_ROOT{%{_bindir}/mount_ehd,%{_mandir}/man8/mount_ehd.8}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog FAQ NEWS README TODO
%attr(755,root,root) /%{_lib}/security/pam_mount.so
%config(noreplace) %verify(not md5 mtime size) /etc/security/pam_mount.conf
%attr(755,root,root) /sbin/mount.crypt
%attr(755,root,root) /sbin/umount.crypt
%attr(755,root,root) %{_bindir}/autoehd
%attr(755,root,root) %{_bindir}/mkehd
%attr(755,root,root) %{_bindir}/mount.crypt
%attr(755,root,root) %{_bindir}/passwdehd
%attr(755,root,root) %{_sbindir}/pmvarrun
%{_mandir}/man1/mkehd.1*
%{_mandir}/man8/autoehd.8*
%{_mandir}/man8/mount.crypt.8*
%{_mandir}/man8/pam_mount.8*
%{_mandir}/man8/passwdehd.8*
%{_mandir}/man8/pmvarrun.8*
%{_mandir}/man8/umount.crypt.8*
