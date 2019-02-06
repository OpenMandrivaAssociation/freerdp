# "fix" underlinking:
%define _disable_ld_no_undefined 1

%define up_name		freerdp2

%define winpr_major	2
%define uwac_major	0
%define major		2
%define libname		%mklibname %{name} %{major}
%define develname	%mklibname %{name} -d

%define rc_ver		1
%define rc_name		rc4
%if %{rc_ver}
%define release		%mkrel -c %{rc_name} %{rel}
%define tarballver	%{version}-%{rc_name}
%define tarballdir	%{version}-%{rc_name}
%else
%define release		%mkrel %{rel}
%define tarballver	%{version}
%define tarballdir	v%{version}
%endif

%define rel		1

# Momentarily disable GSS support
# https://github.com/FreeRDP/FreeRDP/issues/4348
#global _with_gss 1

Name:		freerdp
Version:	2.0.0
Release:	%{release}
Summary:	A free remote desktop protocol client
License:	Apache License
Group:		Networking/Remote access
Url:		http://www.freerdp.com/
Source0:	https://github.com/FreeRDP/FreeRDP/archive/%{tarballdir}/FreeRDP-%{tarballver}.tar.gz
BuildRequires:	cmake
BuildRequires:	docbook-style-xsl
BuildRequires:	xmlto
BuildRequires:	cups-devel
BuildRequires:	ffmpeg-devel
BuildRequires:	gsm-devel
BuildRequires:  pkgconfig(alsa)
BuildRequires:	pkgconfig(libjpeg)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(xcursor)
BuildRequires:	pkgconfig(xinerama)
BuildRequires:	pkgconfig(xkbfile)
BuildRequires:	pkgconfig(xv)
BuildRequires:	pkgconfig(x11)
BuildRequires:  pam-devel
BuildRequires:	pkgconfig(gstreamer-1.0)
BuildRequires:	pkgconfig(gstreamer-base-1.0)
BuildRequires:	pkgconfig(gstreamer-app-1.0)
BuildRequires:	pkgconfig(gstreamer-audio-1.0)
BuildRequires:	pkgconfig(gstreamer-fft-1.0)
BuildRequires:	pkgconfig(gstreamer-pbutils-1.0)
BuildRequires:	pkgconfig(gstreamer-video-1.0)
%{?_with_gss:BuildRequires:  pkgconfig(krb5) >= 1.13}
BuildRequires:	pkgconfig(libpcsclite)
BuildRequires:	pkgconfig(systemd)
BuildRequires:	pkgconfig(xdamage)
BuildRequires:	pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:	pkgconfig(xrandr)
BuildRequires:	pkgconfig(xi)
BuildRequires:	pkgconfig(xkbcommon)
BuildRequires:	pkgconfig(zlib)

%description
FreeRDP is a fork of the rdesktop project.

#----------------------------------------------------

%package -n	%{libname}
Summary:	Main library for %{name}
Group:		System/Libraries
# ease for update
Conflicts:	%{mklibname freerdp 1} < 1.2.0-5

%description -n	%{libname}
Shared libraries for %{name}.

#----------------------------------------------------

%package -n	%{develname}
Summary:	Development files for %{name}
Group:		Development/C++
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n	%{develname}
Development files and headers for %{name}.

#----------------------------------------------------

%prep
%setup -qn FreeRDP-%{tarballver}

%build
%cmake \
    -DWITH_ALSA=ON \
    -DWITH_CUPS=ON \
    -DWITH_CHANNELS=ON -DBUILTIN_CHANNELS=OFF \
    -DWITH_CLIENT=ON \
    -DWITH_DIRECTFB=OFF \
    -DWITH_GSM=ON \
    -DWITH_GSSAPI=%{?_with_gss:ON}%{?!_with_gss:OFF} \
    -DWITH_GSTREAMER_1_0=ON -DWITH_GSTREAMER_0_10=OFF \
    -DGSTREAMER_1_0_INCLUDE_DIRS=%{_includedir}/gstreamer-1.0 \
    -DWITH_IPP=OFF \
    -DWITH_JPEG=ON \
    -DWITH_MANPAGES=ON \
    -DWITH_OPENSSL=ON \
    -DWITH_PCSC=ON \
    -DWITH_PULSE=ON \
    -DWITH_SERVER=ON -DWITH_SERVER_INTERFACE=ON \
    -DWITH_SHADOW_X11=ON -DWITH_SHADOW_MAC=ON \
    -DWITH_WAYLAND=ON \
    -DWITH_X11=ON \
    -DWITH_XCURSOR=ON \
    -DWITH_XEXT=ON \
    -DWITH_XKBFILE=ON \
    -DWITH_XI=ON \
    -DWITH_XINERAMA=ON \
    -DWITH_XRENDER=ON \
    -DWITH_XTEST=OFF \
    -DWITH_XV=ON \
    -DWITH_ZLIB=ON \
    -DWITH_FFMPEG=ON \
%ifarch %{x86_64}
    -DWITH_SSE2=ON \
%else
    -DWITH_SSE2=OFF \
%endif
%ifarch armv7hl
    -DARM_FP_ABI=hard \
    -DWITH_NEON=OFF \
%endif
%ifarch armv7hnl aarch64
    -DARM_FP_ABI=hard \
    -DWITH_NEON=ON \
%endif
    -DCMAKE_INSTALL_LIBDIR:PATH=%{_lib}

%make_build

%install
%make_install -C build

# we don't want these
find %{buildroot} -name '*.la' -delete
find %{buildroot} -name '*.a' -delete

%files
%doc ChangeLog README LICENSE
%{_bindir}/*
%{_libdir}/%{name}2/
%{_mandir}/man1/xfreerdp.1.*
%{_mandir}/man1/freerdp-shadow-cli.1.*
%{_mandir}/man1/winpr-hash.1.*
%{_mandir}/man1/winpr-makecert.1.*
%{_mandir}/man1/wlfreerdp.1.*
%{_mandir}/man7/wlog.7.*

%files -n %{libname}
%{_libdir}/lib*%{name}*.so.%{major}*
%{_libdir}/libwinpr*.so.%{winpr_major}*
%{_libdir}/libuwac*.so.%{uwac_major}*

%files -n %{develname}
%{_libdir}/*.so
%{_includedir}/%{up_name}/
%{_includedir}/winpr*/
%{_includedir}/uwac*/
%{_libdir}/pkgconfig/%{name}*.pc
%{_libdir}/pkgconfig/winpr*.pc
%{_libdir}/pkgconfig/uwac*.pc
%{_libdir}/cmake/FreeRDP*/
%{_libdir}/cmake/WinPR*/
%{_libdir}/cmake/uwac*/
