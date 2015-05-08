%define major           56
%define avdevmajor      56
%define filtermajor     5
%define avfmtmajor      56
%define avumajor        54
%define ppmajor         53
%define swrmajor        1
%define swsmajor        3
%define libavcodec      %mklibname avcodec %{major}
%define libavdevice     %mklibname avdevice %{avdevmajor}
%define libavfilter     %mklibname avfilter %{filtermajor}
%define libavformat     %mklibname avformat %{avfmtmajor}
%define libavutil       %mklibname avutil %{avumajor}
%define libpostproc     %mklibname postproc %{ppmajor}
%define libswresample   %mklibname swresample %{swrmajor}
%define libswscale      %mklibname swscaler %{swsmajor}
%define devname         %mklibname %{name} -d
%define statname        %mklibname %{name} -s -d

#####################
# Hardcode PLF build
%define build_plf 0
#####################

%{?_with_plf: %{expand: %%global build_plf 1}}
%if %{build_plf}
%define distsuffix plf
# make EVR of plf build higher than regular to allow update, needed with rpm5 mkrel
%define extrarelsuffix plf
%bcond_with	dlopen
%else
%bcond_without	dlopen
%endif

%bcond_without	swscaler
%bcond_without	opencv
%bcond_with	faac

Summary:	Hyper fast MPEG1/MPEG4/H263/RV and AC3/MPEG audio encoder
Name:		ffmpeg
Version:	2.5.4
Release:	4.1%{?extrarelsuffix}
%if %{build_plf}
License:	GPLv3+
%else
License:	GPLv2+
%endif
Group:		Video
Url:		http://ffmpeg.org/
Source0:	http://ffmpeg.org/releases/%{name}-%{version}.tar.bz2
# https://github.com/hrydgard/ppsspp-ffmpeg/commit/bf46d9937f8fcb3456b786f64c13e5e069d32c8f
Patch0:		ffmpeg-atrac3plus-fix-gha.patch
Patch1:		ffmpeg-2.5-dlopen-faac-mp3lame-opencore-x264-x265-xvid.patch
Patch2:		ffmpeg-1.0.1-time.h.patch
Patch3:		ffmpeg-2.5-fix-build-with-flto-and-inline-assembly.patch
Patch4:		ffmpeg-2.5-local-headers-for-dlopen.patch
Patch5:		ffmpeg-xbmc-support.patch
BuildRequires:	texi2html
BuildRequires:	yasm
BuildRequires:	bzip2-devel
BuildRequires:	gsm-devel
BuildRequires:	jpeg-devel
BuildRequires:	ladspa-devel
BuildRequires:	libnut-devel
BuildRequires:	libschroedinger-devel
# Maybe needs to be updated in future
BuildConflicts:	crystalhd-devel

BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(celt)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(gnutls) >= 3.0
BuildRequires:	pkgconfig(jack)
BuildRequires:	pkgconfig(libass)
BuildRequires:	pkgconfig(libbluray)
BuildRequires:	pkgconfig(libcdio)
BuildRequires:	pkgconfig(libcdio_paranoia)
BuildRequires:	pkgconfig(libdc1394-2)
BuildRequires:	pkgconfig(libmodplug)
BuildRequires:	pkgconfig(libopenjpeg1)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(librtmp)
BuildRequires:	pkgconfig(libva)
BuildRequires:	pkgconfig(libv4l2)
%if %{with opencv}
BuildRequires:	pkgconfig(opencv)
%endif
BuildRequires:	pkgconfig(opus)
BuildRequires:	pkgconfig(sdl)
BuildRequires:	pkgconfig(soxr)
BuildRequires:	pkgconfig(speex)
BuildRequires:	pkgconfig(theora)
BuildRequires:	pkgconfig(vdpau)
BuildRequires:	pkgconfig(vorbis)
BuildRequires:	pkgconfig(vpx)
BuildRequires:	pkgconfig(wavpack)
%if %{build_plf}
BuildRequires:	liblame-devel
BuildRequires:	xvid-devel
BuildRequires:	pkgconfig(opencore-amrnb)
BuildRequires:	pkgconfig(opencore-amrwb)
BuildRequires:	pkgconfig(vo-aacenc)
BuildRequires:	pkgconfig(vo-amrwbenc)
BuildRequires:	pkgconfig(x264)
BuildRequires:	pkgconfig(x265)
%endif
%if %{with faac}
BuildRequires:	libfaac-devel
%endif
%if 0
Buildrequires:	pkgconfig(frei0r)
%endif

%description
ffmpeg is a hyper fast realtime audio/video encoder, a streaming server
and a generic audio and video file converter.

It can grab from a standard Video4Linux video source and convert it into
several file formats based on DCT/motion compensation encoding. Sound is
compressed in MPEG audio layer 2 or using an AC3 compatible stream.

%if %{build_plf}
This package is in Restricted as it violates several patents.
%endif

%files
%doc INSTALL.md README.md doc/*.html doc/*.txt doc/*.conf
%{_bindir}/*
%{_mandir}/man1/*
%{_datadir}/ffmpeg
%exclude %{_datadir}/ffmpeg/examples

#----------------------------------------------------------------------------

%package -n	%{libavcodec}
Summary:	Shared library part of ffmpeg
Group:		System/Libraries
%if %{with dlopen}
%if "%{_lib}" == "lib64"
%global	_ext	()(64bit)
%else
%global	_ext	%{nil}
%endif
Suggests:	libfaac.so.0%{_ext}
Suggests:	libx264.so.142%{_ext}
Suggests:	libopencore-amrnb.so.0%{_ext}
Suggests:	libopencore-amrwb.so.0%{_ext}
Suggests:	libmp3lame.so.0%{_ext}
Suggests:	libxvidcore.so.4%{_ext}
%endif

%description -n	%{libavcodec}
This package contains a shared library for %{name}.

%if %{build_plf}
This package is in Restricted as it violates several patents.
%endif

%files -n %{libavcodec}
%{_libdir}/libavcodec.so.%{major}*

#----------------------------------------------------------------------------

%package -n	%{libavdevice}
Summary:	Shared library part of ffmpeg
Group:		System/Libraries

%description -n %{libavdevice}
This package contains a shared library for %{name}.

%files -n %{libavdevice}
%{_libdir}/libavdevice.so.%{avdevmajor}*

#----------------------------------------------------------------------------

%package -n	%{libavfilter}
Summary:	Shared library part of ffmpeg
Group:		System/Libraries

%description -n	%{libavfilter}
This package contains a shared library for %{name}.

%files -n %{libavfilter}
%{_libdir}/libavfilter.so.%{filtermajor}*

#----------------------------------------------------------------------------

%package -n	%{libavformat}
Summary:	Shared library part of ffmpeg
Group:		System/Libraries

%description -n %{libavformat}
This package contains a shared library for %{name}.

%files -n %{libavformat}
%{_libdir}/libavformat.so.%{avfmtmajor}*

#----------------------------------------------------------------------------

%package -n	%{libavutil}
Summary:	Shared library part of ffmpeg
Group:		System/Libraries

%description -n %{libavutil}
This package contains a shared library for %{name}.

%files -n %{libavutil}
%{_libdir}/libavutil.so.%{avumajor}*

#----------------------------------------------------------------------------

%package -n	%{libpostproc}
Summary:	Shared library part of ffmpeg
Group:		System/Libraries
Conflicts:	%{_lib}ffmpeg51

%description -n	%{libpostproc}
This package contains a shared library for %{name}.

%files -n %{libpostproc}
%{_libdir}/libpostproc.so.%{ppmajor}*

#----------------------------------------------------------------------------

%package -n	%{libswresample}
Summary:	Shared library part of ffmpeg
Group:		System/Libraries

%description -n %{libswresample}
This package contains a shared library for %{name}.

%files -n %{libswresample}
%{_libdir}/libswresample.so.%{swrmajor}*

#----------------------------------------------------------------------------

%if %{with swscaler}
%package -n	%{libswscale}
Summary:	Shared library part of ffmpeg
Group:		System/Libraries

%description -n %{libswscale}
This package contains a shared library for %{name}.

%files -n %{libswscale}
%{_libdir}/libswscale.so.%{swsmajor}*
%endif

#----------------------------------------------------------------------------

%package -n	%{devname}
Group:		Development/C
Summary:	Header files for the ffmpeg codec library
Requires:	%{libavcodec} = %{EVRD}
Requires:	%{libavdevice} = %{EVRD}
Requires:	%{libavfilter} = %{EVRD}
Requires:	%{libavformat} = %{EVRD}
Requires:	%{libavutil} = %{EVRD}
Requires:	%{libpostproc} = %{EVRD}
Requires:	%{libswresample} = %{EVRD}
%if %{with swscaler}
Requires:	%{libswscale} = %{EVRD}
%endif
Provides:	ffmpeg-devel = %{EVRD}

%description -n	%{devname}
ffmpeg is a hyper fast realtime audio/video encoder, a streaming server
and a generic audio and video file converter.

It can grab from a standard Video4Linux video source and convert it into
several file formats based on DCT/motion compensation encoding. Sound is
compressed in MPEG audio layer 2 or using an AC3 compatible stream.

Install this package if you want to compile apps with ffmpeg support.

%files -n %{devname}
%{_includedir}/libavcodec
%{_includedir}/libavdevice
%{_includedir}/libavfilter
%{_includedir}/libavformat
%{_includedir}/libavutil
%{_includedir}/libpostproc
%{_includedir}/libswresample
%{_libdir}/libavcodec.so
%{_libdir}/libavdevice.so
%{_libdir}/libavfilter.so
%{_libdir}/libavformat.so
%{_libdir}/libavutil.so
%{_libdir}/libpostproc.so
%{_libdir}/libswresample.so
%if %{with swscaler}
%{_includedir}/libswscale
%{_libdir}/libswscale.so
%{_libdir}/pkgconfig/libswscale.pc
%endif
%{_libdir}/pkgconfig/libavcodec.pc
%{_libdir}/pkgconfig/libavdevice.pc
%{_libdir}/pkgconfig/libavfilter.pc
%{_libdir}/pkgconfig/libavformat.pc
%{_libdir}/pkgconfig/libavutil.pc
%{_libdir}/pkgconfig/libpostproc.pc
%{_libdir}/pkgconfig/libswresample.pc
%{_mandir}/man3/lib*.3.*
%{_datadir}/ffmpeg/examples

#----------------------------------------------------------------------------

%package -n	%{statname}
Group:		Development/C
Summary:	Static library for the ffmpeg codec library
Requires:	%{devname} = %{EVRD}
Provides:	ffmpeg-static-devel = %{EVRD}

%description -n	%{statname}
ffmpeg is a hyper fast realtime audio/video encoder, a streaming server
and a generic audio and video file converter.

It can grab from a standard Video4Linux video source and convert it into
several file formats based on DCT/motion compensation encoding. Sound is
compressed in MPEG audio layer 2 or using an AC3 compatible stream.

Install this package if you want to compile static apps with ffmpeg support.

%files -n %{statname}
%{_libdir}/*.a

#----------------------------------------------------------------------------

%prep
%setup -q
%patch0 -p1 -b .atrac3plus~
%patch2 -p1 -b .timeh~
%patch3 -p1 -b .flto_inline_asm~
%if %{with dlopen}
%patch1 -p1 -b .dlopen~
%patch4 -p1 -b .dl_headers~
%endif
%patch5 -p1 -b .xbmc~

%build
export CFLAGS="%{optflags} -fPIC -I%{_includedir}/openjpeg-1.5/"
export LDFLAGS="%{ldflags}"

./configure --prefix=%{_prefix} \
	--enable-shared \
	--libdir=%{_libdir} \
	--shlibdir=%{_libdir} \
	--incdir=%{_includedir} \
	--disable-stripping \
	--enable-postproc \
	--enable-gpl \
	--enable-pthreads \
	--enable-ladspa \
	--enable-libbluray \
	--enable-libtheora \
	--enable-libvorbis --disable-encoder=vorbis \
	--enable-libvpx \
	--enable-x11grab \
	--enable-runtime-cpudetect \
	--enable-libdc1394 \
	--enable-libschroedinger \
	--enable-librtmp \
	--enable-libspeex \
	--enable-libfreetype \
	--enable-libnut \
	--enable-libgsm \
	--enable-libcelt \
%if %{with opencv}
	--enable-libopencv \
%else
	--disable-libopencv \
%endif
	--enable-libopenjpeg \
	--enable-libopus \
	--enable-libsoxr \
	--enable-libwavpack \
	--disable-libxavs \
	--enable-libmodplug \
	--enable-libass \
	--enable-gnutls \
	--enable-libcdio \
	--enable-libpulse \
	--enable-libv4l2 \
%if 0
	--enable-frei0r \
%endif
%if %{build_plf}
	--enable-libmp3lame \
	--enable-libopencore-amrnb \
	--enable-libopencore-amrwb \
	--enable-version3 \
	--enable-libx264 \
	--enable-libx265 \
	--enable-libvo-aacenc \
	--enable-libvo-amrwbenc \
	--enable-libxvid \
%else
	--disable-decoder=aac --disable-encoder=aac \
%if %{with dlopen}
	--enable-libmp3lame-dlopen \
	--enable-libopencore-amrnb-dlopen \
	--enable-libopencore-amrwb-dlopen \
	--enable-libx264-dlopen \
	--enable-libxvid-dlopen \
%if !%{with faac}
	--enable-libfaac-dlopen \
%endif
%endif
%endif
%if %{with faac}
	--enable-nonfree --enable-libfaac
%endif

%make

%install
%makeinstall_std SRC_PATH=`pwd`

