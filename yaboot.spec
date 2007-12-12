# libdir independent location, i.e. always /usr/lib/yaboot/
%define yabootdir %{_prefix}/lib/yaboot

# define to use "ofpath" from the powerpc-utils package (default for ppc64)
%define ppcutils_ofpath 0
%ifarch ppc64
%define ppcutils_ofpath 1
%endif

Summary:	New World Mac Bootloader
Name:		yaboot
Version:	1.3.13
Release:	8mdk
License:	GPL
Group:		System/Kernel and hardware
ExclusiveArch: 	ppc ppc64

Source:		http://penguinppc.org/usr/yaboot/yaboot-%{version}.tar.bz2
Patch1: 	yaboot-1.3.3-man.patch.bz2
Patch2: 	yaboot-1.3.6-ofboot.patch.bz2
Patch3:		yaboot-1.3.13-ofpath-usb-storage.patch.bz2
Patch4:		yaboot-1.3.13-buildfix.patch.bz2
Patch5:		yaboot-1.3.13-ofpath-sbp2.patch.bz2
Patch6:		yaboot-1.3.13-ofpath-disable-devicetree-check.patch.bz2
Patch7:		yaboot-1.3.13-ppc64.patch.bz2
Patch8:		yaboot-1.3.13-netboot.patch.bz2
Patch9:		yaboot-1.3.13-confarg.patch.bz2
Patch10:	yaboot-1.3.13-ibm-vscsi.patch.bz2
Patch11:	yaboot-1.3.13-ybin-raw-install-return0.patch.bz2

Url:		http://penguinppc.org/projects/yaboot/
BuildRoot:	%_tmppath/%name-%version-root

Requires(post):	powerpc-utils >= 0.0.1-4mdk
Requires: powerpc-utils >= 0.0.1-4mdk
Provides: bootloader ybin

%description
Ybin is a GNU/Linux utility to install the yaboot  boot loader onto a 
bootstrap partition. It will not run from MacOS.                        

Yaboot is the bootloader for NewWorld PowerMacs and  IBM CHRP hardware 
architectures. It will not work on OldWorld PowerMacs. 
                       
ybin (YaBoot INstaller) was created so that there could be a lilo/quik 
style bootloader installer for PowerPC based machines which require 
bootstrap partitions rather then a traditional bootblock (ie all 
`newworld' Macintoshes). It is designed to install yaboot, an  
OpenFirmware bootloader for GNU/Linux written by Benjamin Herrenschmidt. 
When ybin is configured correctly you can simply type ybin, and the 
bootloader and its configuration will be installed/updated on the 
bootstrap partition without any further user intervention.  ybin also 
supports IBM bootstrap partitions. 

%prep
%setup -q
%patch1 -p0
%patch2 -p1
%patch3 -p1 -b .usb-storage
%patch4 -p1 -b .fix
%patch5 -p1 -b .sbp2
%patch6 -p1 -b .disable-devicetree-check
%patch7 -p1 -b .ppc64
%patch8 -p1 -b .netboot
%patch9 -p1 -b .confarg
%patch10 -p1 -b .ibm-vscsi
%patch11 -p1 -b .ybin-raw-install-return0

#change some install paths
perl -pi -e 's|-o root -g root||g' Makefile
#bzip man-pages
perl -pi -e 's|gzip -9|bzip2 -9|g' Makefile
perl -pi -e 's|8.gz|8.bz2|g' Makefile
perl -pi -e 's|5.gz|5.bz2|g' Makefile
perl -pi -e 's|gunzip man/\*.gz|bunzip2 man/\*.bz2|g' Makefile

%build
%make

%install
%makeinstall ROOT=$RPM_BUILD_ROOT PREFIX=%{_prefix} MANDIR=share/man

%if %{ppcutils_ofpath}
rm -f $RPM_BUILD_ROOT%{_sbindir}/ofpath
rm -f $RPM_BUILD_ROOT%{_mandir}/man8/ofpath.8.bz2
%endif

%clean
rm -fr %buildroot

%post
USELOCAL=`grep '\/usr\/local' /etc/yaboot.conf`
if [ -n "$USELOCAL" ]; then
perl -pi -e 's|/usr/local|/usr|g' /etc/yaboot.conf
fi
/usr/sbin/ybin
true

%files
%defattr(-,root,root)
%doc COPYING README* doc/*
%config(noreplace) /etc/yaboot.conf
%{_sbindir}/ybin
%{_sbindir}/yabootconfig
%{_sbindir}/mkofboot
%{yabootdir}/addnote
%{yabootdir}/ofboot
%{yabootdir}/yaboot
%{_mandir}/man8/bootstrap.8.bz2
%{_mandir}/man8/mkofboot.8.bz2
%{_mandir}/man8/yaboot.8.bz2
%{_mandir}/man8/ybin.8.bz2
%{_mandir}/man5/yaboot.conf.5.bz2
%{_mandir}/man8/yabootconfig.8.bz2
%if ! %{ppcutils_ofpath}
%{_sbindir}/ofpath
%{_mandir}/man8/ofpath.8.bz2
%endif

