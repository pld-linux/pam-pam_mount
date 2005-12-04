%define 	modulename pam_mount
Summary:	A PAM module that can mount remote volumes for a user session
Summary(pl):	Modu³ PAM, pozwalaj±cy mountowaæ zdalne zasoby na czas sesji u¿ytkownika
Name:		pam-%{modulename}
Version:	0.9.20
Release:	2
Epoch:		0
License:	LGPL
Group:		Base
Vendor:		Flyn Computing
Source0:	http://www.flyn.org/projects/%{modulename}/%{modulename}-%{version}.tar.gz
# Source0-md5:	392b1d69f36d5f2d053c393594cff9cb
Patch0:		%{name}-zlib.patch
Patch1:		%{name}-evp.patch
URL:		http://www.flyn.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	pam-devel
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
Przeznaczeniem tego modu³u s± ¶rodowiska z protoko³em SMB (Samba lub
Windows NT) i/lub NCP (Netware lub Mars-NWE), w których u¿ytkownicy
chc± lub potrzebuj± takich zasobów. Modu³ ten wspiera tak¿e
mountowanie katalogów domowych z zaszyfrowanych systemów plików przy
u¿yciu loopbacka (zobacz tak¿e:
http://www.tldp.org/HOWTO/Loopback-Encrypted-Filesystem-HOWTO.html).
 - ka¿dy u¿ytkownik ma dostêp do swoich zasobów
 - u¿ytkownik musi wpisaæ swoje has³o tylko raz (przy logowaniu) (*)
 - proces mountowania jest niewidzialny dla u¿ytkownika
 - nie ma potrzeby trzymania has³a i loginu w ¿adnym dodatkowym pliku
 - katalogi s± odmountowywane podczas wylogowania, co oszczêdza zasoby
   systemowe, zabezpiecza przed konieczno¶ci± umieszczenia ka¿dego
   potrzebnego zdalnego zasobu w /etc/fstab lub w konfiguracji
   automounta/supermounta. Jest to tak¿e konieczne do zabezpieczenia
   zaszyfrowanych systemów plików.

(*) Oczywi¶cie has³o na lokalnym i zdalnym systemie musi byæ
identyczne ;)

pam_mount "rozumie" SMB, NCP oraz zaszyfrowane systemy plików po
loopbacku, ale mo¿e byæ rozszerzony w prosty sposób.

%prep
%setup -q -n %{modulename}-%{version}
%patch0 -p1
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/security

%{__make} install \
	moduledir=/%{_lib}/security \
	DESTDIR=$RPM_BUILD_ROOT

install config/pam_mount.conf $RPM_BUILD_ROOT/etc/security

rm -f $RPM_BUILD_ROOT/%{_lib}/security/pam_mount.{la,a}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) /%{_lib}/security/pam_mount.so
%config(noreplace) %verify(not md5 mtime size) /etc/security/pam_mount.conf
%{_mandir}/man8/*
