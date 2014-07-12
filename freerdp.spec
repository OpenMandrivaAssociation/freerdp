%define major 1.0

Summary:	A free remote desktop protocol client
Name:		freerdp
Version:	1.0.2
Release:	6.1
License:	Apache License
Group:		Networking/Remote access
Url:		http://freerdp.sourceforge.net/
Source0:	https://github.com/downloads/FreeRDP/FreeRDP/%{name}-%{version}.tar.gz
BuildRequires:	cmake
BuildRequires:	docbook-style-xsl
BuildRequires:	xmlto
BuildRequires:	cups-devel
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xcursor)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xinerama)
BuildRequires:	pkgconfig(xkbfile)
BuildRequires:	pkgconfig(xv)

%description
FreeRDP is a fork of the rdesktop project.

%files
%doc ChangeLog LICENSE README
%{_bindir}/*
%{_libdir}/%{name}
%{_datadir}/%{name}
%{_mandir}/man1/xfreerdp.1.*

#----------------------------------------------------------------------------

%define libcache %mklibname freerdp-cache %{major}

%package -n %{libcache}
Summary:	Shared library for %{name}
Group:		System/Libraries
Conflicts:	%{_lib}freerdp1 < 1.0.2

%description -n %{libcache}
Shared library for %{name}.

%files -n %{libcache}
%{_libdir}/libfreerdp-cache.so.%{major}*

#----------------------------------------------------------------------------

%define libchannels %mklibname freerdp-channels %{major}

%package -n %{libchannels}
Summary:	Shared library for %{name}
Group:		System/Libraries
Conflicts:	%{_lib}freerdp1 < 1.0.2

%description -n %{libchannels}
Shared library for %{name}.

%files -n %{libchannels}
%{_libdir}/libfreerdp-channels.so.%{major}*

#----------------------------------------------------------------------------

%define libcodec %mklibname freerdp-codec %{major}

%package -n %{libcodec}
Summary:	Shared library for %{name}
Group:		System/Libraries
Conflicts:	%{_lib}freerdp1 < 1.0.2

%description -n %{libcodec}
Shared library for %{name}.

%files -n %{libcodec}
%{_libdir}/libfreerdp-codec.so.%{major}*

#----------------------------------------------------------------------------

%define libcore %mklibname freerdp-core %{major}

%package -n %{libcore}
Summary:	Shared library for %{name}
Group:		System/Libraries
Conflicts:	%{_lib}freerdp1 < 1.0.2
Obsoletes:	%{_lib}freerdp1 < 1.0.2

%description -n %{libcore}
Shared library for %{name}.

%files -n %{libcore}
%{_libdir}/libfreerdp-core.so.%{major}*

#----------------------------------------------------------------------------

%define libgdi %mklibname freerdp-gdi %{major}

%package -n %{libgdi}
Summary:	Shared library for %{name}
Group:		System/Libraries
Conflicts:	%{_lib}freerdp1 < 1.0.2

%description -n %{libgdi}
Shared library for %{name}.

%files -n %{libgdi}
%{_libdir}/libfreerdp-gdi.so.%{major}*

#----------------------------------------------------------------------------

%define libkbd %mklibname freerdp-kbd %{major}

%package -n %{libkbd}
Summary:	Shared library for %{name}
Group:		System/Libraries
Conflicts:	%{_lib}freerdp1 < 1.0.2

%description -n %{libkbd}
Shared library for %{name}.

%files -n %{libkbd}
%{_libdir}/libfreerdp-kbd.so.%{major}*

#----------------------------------------------------------------------------

%define librail %mklibname freerdp-rail %{major}

%package -n %{librail}
Summary:	Shared library for %{name}
Group:		System/Libraries
Conflicts:	%{_lib}freerdp1 < 1.0.2

%description -n %{librail}
Shared library for %{name}.

%files -n %{librail}
%{_libdir}/libfreerdp-rail.so.%{major}*

#----------------------------------------------------------------------------

%define libutils %mklibname freerdp-utils %{major}

%package -n %{libutils}
Summary:	Shared library for %{name}
Group:		System/Libraries
Conflicts:	%{_lib}freerdp1 < 1.0.2
Obsoletes:	%{mklibname freerdp 1} < 1.0.2

%description -n %{libutils}
Shared library for %{name}.

%files -n %{libutils}
%{_libdir}/libfreerdp-utils.so.%{major}*

#----------------------------------------------------------------------------

%define devname %mklibname %{name} -d

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/C++
Requires:	%{libcache} = %{EVRD}
Requires:	%{libchannels} = %{EVRD}
Requires:	%{libcodec} = %{EVRD}
Requires:	%{libcore} = %{EVRD}
Requires:	%{libgdi} = %{EVRD}
Requires:	%{libkbd} = %{EVRD}
Requires:	%{librail} = %{EVRD}
Requires:	%{libutils} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n %{devname}
Development files and headers for %{name}.

%files -n %{devname}
%{_libdir}/*.so
%{_includedir}/%{name}
%{_libdir}/pkgconfig/freerdp.pc

#----------------------------------------------------------------------------

%prep
%setup -q -n FreeRDP-%{version}

%build
%cmake \
    -DWITH_CUPS=ON \
    -DWITH_PULSEAUDIO=ON \
    -DWITH_X11=ON \
    -DWITH_XCURSOR=ON \
    -DWITH_XEXT=ON \
    -DWITH_XINERAMA=ON \
    -DWITH_XKBFILE=ON \
    -DWITH_XV=ON \
    -DWITH_ALSA=OFF \
    -DWITH_CUNIT=OFF \
    -DWITH_DIRECTFB=OFF \
    -DWITH_FFMPEG=OFF \
    -DWITH_SSE2=OFF \
    -DCMAKE_INSTALL_LIBDIR:PATH=%{_lib}
%make

%install
%makeinstall_std -C build

