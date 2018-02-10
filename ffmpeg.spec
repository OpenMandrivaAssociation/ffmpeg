%define major		57
%define ppmajor 	54
%define avumajor 	55
%define swsmajor 	4
%define filtermajor 	6
%define swrmajor 	2
%define	avrmajor	3
%define libavcodec	%mklibname avcodec %{major}
%define	libavdevice	%mklibname avdevice %{major}
%define libavfilter	%mklibname avfilter %{filtermajor}
%define libavformat	%mklibname avformat %{major}
%define libavutil	%mklibname avutil %{avumajor}
%define libpostproc	%mklibname postproc %{ppmajor}
%define libswresample	%mklibname swresample %{swrmajor}
%define libswscale	%mklibname swscaler %{swsmajor}
%define	libavresample	%mklibname avresample %{avrmajor}
%define devname		%mklibname %{name} -d
%define statname	%mklibname %{name} -s -d

#####################
# Hardcode PLF build
%define build_plf 0
#####################

%{?_with_plf: %{expand: %%global build_plf 1}}
%if %{build_plf}
%define distsuffix plf
# make EVR of plf build higher than regular to allow update, needed with rpm5 mkrel
%define extrarelsuffix plf
%bcond_with dlopen
%else
%bcond_without dlopen
%endif

# OpenCL can speed up things and offload work to the GPU, but as of 2014/12/21
# (Mesa 10.4.0, Xorg 1.6.3, Intel driver 2.99.917), it causes crashes on startup
%bcond_with	opencl

%bcond_without	swscaler
%bcond_with	faac
# bootstrap
# rebuild ffmpeg after MESA api upgrade
# 1. rebuild ffmpeg with disabled opencv
# 2. rebuild opencv with new ffmpeg
# 3. rebuild ffmpeg again
# 4. PROFIT
%bcond_with	opencv
%bcond_without	swscaler

Summary:	Hyper fast MPEG1/MPEG4/H263/H264/H265/RV and AC3/MPEG audio encoder
Name:		ffmpeg
Version:	3.3.4
Release:	5
%if %{build_plf}
License:	GPLv3+
%else
License:	GPLv2+
%endif
Group:		Video
Url:		http://ffmpeg.org/
Source0:	http://ffmpeg.org/releases/%{name}-%{version}.tar.bz2
Patch1:		ffmpeg-3.0-dlopen-faac-mp3lame-opencore-x264-x265-xvid.patch
Patch2:		ffmpeg-1.0.1-time.h.patch
Patch3:		ffmpeg-2.5-fix-build-with-flto-and-inline-assembly.patch
Patch4:		ffmpeg-local-headers-for-dlopen.patch
# Fix build with openjpeg 2.2
Patch5:		https://github.com/FFmpeg/FFmpeg/commit/078322f33ced4b2db6ac3e5002f98233d6fbf643.patch
BuildRequires:	texi2html
BuildRequires:	yasm
BuildRequires:	bzip2-devel
BuildRequires:	flite-devel
BuildRequires:	gsm-devel
BuildRequires:	jpeg-devel
BuildRequires:	ladspa-devel
BuildRequires:	libgme-devel
BuildRequires:	libnut-devel
BuildRequires:	pkgconfig(caca)
BuildRequires:	pkgconfig(celt)
BuildRequires:	pkgconfig(fontconfig)
%if !%{with dlopen} || "%{disttag}" == "mdk"
BuildRequires:	pkgconfig(fdk-aac)
%endif
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(gnutls)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(jack)
BuildRequires:	pkgconfig(libass)
BuildRequires:	pkgconfig(libavc1394)
BuildRequires:	pkgconfig(libbluray)
BuildRequires:	pkgconfig(libbs2b)
BuildRequires:	pkgconfig(libcdio_paranoia)
BuildRequires:	pkgconfig(libdc1394-2)
BuildRequires:	pkgconfig(libiec61883)
BuildRequires:	pkgconfig(libilbc)
BuildRequires:	pkgconfig(libmodplug)
BuildRequires:	pkgconfig(libopenjp2)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(librtmp)
BuildRequires:	pkgconfig(libssh)
BuildRequires:	pkgconfig(libva)
BuildRequires:	pkgconfig(libv4l2)
BuildRequires:	pkgconfig(libwebp)
BuildRequires:	pkgconfig(libzmq)
BuildRequires:	pkgconfig(openal)
%if %{with opencv}
BuildRequires:	pkgconfig(opencv)
BuildRequires:	pkgconfig(frei0r)
%endif
BuildRequires:	pkgconfig(opus)
BuildRequires:	pkgconfig(speex)
BuildRequires:	pkgconfig(sdl2)
BuildRequires:	pkgconfig(schroedinger-1.0)
%if 0
BuildRequires:	pkgconfig(shine)
%endif
BuildRequires:	pkgconfig(soxr)
BuildRequires:	pkgconfig(theora)
BuildRequires:	pkgconfig(twolame)
BuildRequires:	pkgconfig(vdpau)
BuildRequires:	pkgconfig(vidstab)
BuildRequires:	pkgconfig(vorbis)
BuildRequires:	pkgconfig(vpx)
BuildRequires:	pkgconfig(wavpack)
BuildRequires:	pkgconfig(xavs)
BuildRequires:	pkgconfig(zvbi-0.2)
BuildRequires:	lame-devel
%if %{build_plf} || "%{disttag}" == "mdk"
BuildRequires:	x264-devel >= 0.148
BuildRequires:	pkgconfig(x265)
BuildRequires:	opencore-amr-devel
BuildRequires:	libvo-amrwbenc-devel
BuildRequires:	xvid-devel
%endif
%if %{with faac}
BuildRequires:	faac-devel
%endif
%ifnarch %{armx}
BuildRequires:	crystalhd-devel >= 0-0.20121105.1
%endif
%if %{with opencl}
BuildRequires:	opencl-devel
%endif

%track
prog %name = {
	url = http://ffmpeg.org/download.html
	version = %version
	regex = "(__VER__) was released on"
}

%description
ffmpeg is a hyper fast realtime audio/video encoder, a streaming server
and a generic audio and video file converter.

It can grab from a standard Video4Linux video source and convert it into
several file formats based on DCT/motion compensation encoding. Sound is
compressed in MPEG audio layer 2 or using an AC3 compatible stream.

%if %{build_plf}
This package is in Restricted as it violates several patents.
%endif

%package doc
Summary:	Documentation for %{name}
Group:		Development/Other
BuildArch:	noarch
Conflicts:	%{name} < 3.0.2-2

%description doc
Documentation for %{name}.

%package -n	%{libavcodec}
Summary:	Shared library part of ffmpeg
Group:		System/Libraries
%if %{with dlopen}
%if "%{disttag}" == "mdk"
%if %{with faac}
Suggests:	%{dlopen_req faac}
%endif
Suggests:	%{dlopen_req x264}
Suggests:	%{dlopen_req x265}
Suggests:	%{dlopen_req opencore-amrnb}
Suggests:	%{dlopen_req opencore-amrwb}
Suggests:	%{dlopen_req mp3lame}
Suggests:	%{dlopen_req xvidcore}
%else
%if %{with faac}
Suggests:	libfaac.so.0%{_arch_tag_suffix}
%endif
Suggests:	libx264.so.148%{_arch_tag_suffix}
Suggests:	libx265.so.95%{_arch_tag_suffix}
Suggests:	libopencore-amrnb.so.0%{_arch_tag_suffix}
Suggests:	libopencore-amrwb.so.0%{_arch_tag_suffix}
Suggests:	libmp3lame.so.0%{_arch_tag_suffix}
Suggests:	libxvidcore.so.4%{_arch_tag_suffix}
Suggests:	libfdk-aac.so.1%{_arch_tag_suffix}
%endif
%endif
Obsoletes:	%{_lib}ffmpeg54 < 1.1-3

%description -n	%{libavcodec}
This package contains a shared library for %{name}.

%package -n	%{libavdevice}
Summary:	Shared library part of ffmpeg
Group:		System/Libraries
Conflicts:	%{_lib}avformats54 < 1.1-3

%description -n %{libavdevice}
This package contains a shared library for %{name}.

%package -n	%{libavfilter}
Summary:	Shared library part of ffmpeg
Group:		System/Libraries

%description -n	%{libavfilter}
This package contains a shared library for %{name}.

%package -n	%{libavformat}
Summary:	Shared library part of ffmpeg
Group:		System/Libraries
Obsoletes:	%{_lib}avformats54 < 1.1-3

%description -n %{libavformat}
This package contains a shared library for %{name}.

%package -n	%{libavutil}
Summary:	Shared library part of ffmpeg
Group:		System/Libraries
Obsoletes:	%{mklibname avutil 51} < 1.1

%description -n %{libavutil}
This package contains a shared library for %{name}.

%package -n	%{libpostproc}
Summary:	Shared library part of ffmpeg
Group:		System/Libraries

%description -n	%{libpostproc}
This package contains a shared library for %{name}.

%package -n	%{libswresample}
Summary:	Shared library part of ffmpeg
Group:		System/Libraries

%description -n %{libswresample}
This package contains a shared library for %{name}.

%if %{with swscaler}
%package -n	%{libswscale}
Summary:	Shared library part of ffmpeg
Group:		System/Libraries

%description -n %{libswscale}
This package contains a shared library for %{name}.
%endif

%package -n	%{libavresample}
Summary:	Shared library part of ffmpeg
Group:		System/Libraries

%description -n %{libavresample}
This package contains a shared library for %{name}.

%package -n	%{devname}
Summary:	Header files for the ffmpeg codec library
Group:		Development/C
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
Provides:	%{name}-devel = %{EVRD}

%description -n	%{devname}
This package contains the development files for %{name}.

%package -n	%{statname}
Summary:	Static library for the ffmpeg codec library
Group:		Development/C
Requires:	%{devname} = %{EVRD}
Provides:	%{name}-static-devel = %{EVRD}

%description -n	%{statname}
This package contains the static libraries for %{name}.

%prep
%setup -q
%patch2 -p1 -b .timeh~
%if %{with dlopen}
%patch1 -p1 -b .dlopen~
%if "%{disttag}" == "omv"
%patch4 -p1 -b .dl_headers~
%endif
%endif
%patch3 -p1 -b .flto_inline_asm~
%patch5 -p1 -b .openjpeg22~

# The debuginfo generator doesn't like non-world readable files
find . -name "*.c" -o -name "*.h" -o -name "*.asm" |xargs chmod 0644
# use headers from current packages in restricted repo

%build
export CFLAGS="%{optflags} -fPIC -I/usr/include/openjpeg-2.2"
export LDFLAGS="%{ldflags}"

# why?
%define	__cc	gcc
%define	__cxx	g++
if ! ./configure \
	--cc=%{__cc} \
	--cxx=%{__cxx} \
	--prefix=%{_prefix} \
	--enable-shared \
	--libdir=%{_libdir} \
	--shlibdir=%{_libdir} \
	--incdir=%{_includedir} \
	--disable-stripping \
	--enable-avresample \
	--enable-postproc \
	--enable-gpl \
	--enable-version3 \
	--enable-nonfree \
	--enable-ffplay \
%ifarch %{ix86} x86_64
	--disable-lto \
%else
	--enable-lto \
%endif
	--enable-pthreads \
	--enable-libtheora \
	--enable-libvorbis \
	--disable-encoder=vorbis \
	--enable-libvpx \
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
	--enable-frei0r \
%endif
	--enable-libopenjpeg \
	--enable-libxavs \
	--enable-libmodplug \
	--enable-libass \
	--enable-gnutls \
	--enable-libcdio \
	--enable-libpulse \
	--enable-libv4l2 \
	--enable-openal \
	--enable-opengl \
	--enable-libzmq \
	--enable-libzvbi \
	--enable-libwavpack \
	--enable-libssh \
	--enable-libsoxr \
	--enable-libtwolame \
	--enable-libopus \
	--enable-libilbc \
	--enable-libiec61883 \
	--enable-libgme \
	--enable-libcaca \
	--enable-libbluray \
	--enable-ladspa \
	--enable-libwebp \
	--enable-avisynth \
	--enable-fontconfig \
%if 0
	--enable-libshine \
%endif
	--enable-libvidstab \
	--enable-libflite \
	--enable-libxcb \
	--enable-libxcb-shm \
	--enable-libxcb-xfixes \
	--enable-libxcb-shape \
	--enable-libbs2b \
	--enable-libmp3lame \
%if %{build_plf}
	--enable-libfdk-aac \
	--enable-libopencore-amrnb \
	--enable-libopencore-amrwb \
	--enable-version3 \
	--enable-libx264 \
	--enable-libx265 \
	--enable-libvo-amrwbenc \
	--enable-libxvid \
%else
%if %{with dlopen}
	--enable-libfdk-aac-dlopen \
	--enable-libopencore-amrnb-dlopen \
	--enable-libopencore-amrwb-dlopen \
	--enable-libx264-dlopen \
	--enable-libx265-dlopen \
	--enable-libxvid-dlopen \
%if %{with faac}
	--enable-libfaac-dlopen \
%endif
%endif
%endif
%if %{with faac} && !%{with dlopen}
	--enable-nonfree \
	--enable-libfaac \
%endif
%if %{with opencl}
	--enable-opencl \
%else
	--disable-opencl \
%endif
%if 0
	--disable-libaacplus \
	--disable-libstagefright-h264 \
	--disable-decklink \
%endif
	; then
	cat config.log
	exit 1
fi

%make V=1

%install
%makeinstall_std SRC_PATH=`pwd`

%files
%{_bindir}/*
%{_mandir}/man1/*
%{_datadir}/ffmpeg
%exclude %{_datadir}/ffmpeg/examples

%files doc
%doc doc/*.html doc/*.txt doc/*.conf
%{_docdir}/ffmpeg/*.html

%files -n %{libavcodec}
%{_libdir}/libavcodec.so.%{major}*

%files -n %{libavdevice}
%{_libdir}/libavdevice.so.%{major}*

%files -n %{libavfilter}
%{_libdir}/libavfilter.so.%{filtermajor}*

%files -n %{libavformat}
%{_libdir}/libavformat.so.%{major}*

%files -n %{libavutil}
%{_libdir}/libavutil.so.%{avumajor}*

%files -n %{libpostproc}
%{_libdir}/libpostproc.so.%{ppmajor}*

%files -n %{libswresample}
%{_libdir}/libswresample.so.%{swrmajor}*

%if %{with swscaler}
%files -n %{libswscale}
%{_libdir}/libswscale.so.%{swsmajor}*
%endif

%files -n %{libavresample}
%{_libdir}/libavresample.so.%{avrmajor}*

%files -n %{devname}
%{_includedir}/libavcodec
%{_includedir}/libavdevice
%{_includedir}/libavformat
%{_includedir}/libavresample
%{_includedir}/libavutil
%{_includedir}/libpostproc
%{_includedir}/libavfilter
%{_includedir}/libswresample
%{_libdir}/libavcodec.so
%{_libdir}/libavdevice.so
%{_libdir}/libavformat.so
%{_libdir}/libavresample.so
%{_libdir}/libavutil.so
%{_libdir}/libpostproc.so
%{_libdir}/libavfilter.so
%{_libdir}/libswresample.so
%if %{with swscaler}
%{_libdir}/libswscale.so
%{_includedir}/libswscale
%{_libdir}/pkgconfig/libswscale.pc
%endif
%{_libdir}/pkgconfig/libavcodec.pc
%{_libdir}/pkgconfig/libavdevice.pc
%{_libdir}/pkgconfig/libavformat.pc
%{_libdir}/pkgconfig/libavresample.pc
%{_libdir}/pkgconfig/libavutil.pc
%{_libdir}/pkgconfig/libpostproc.pc
%{_libdir}/pkgconfig/libavfilter.pc
%{_libdir}/pkgconfig/libswresample.pc
%doc %{_mandir}/man3/libavcodec.3*
%doc %{_mandir}/man3/libavdevice.3*
%doc %{_mandir}/man3/libavfilter.3*
%doc %{_mandir}/man3/libavformat.3*
%doc %{_mandir}/man3/libavutil.3*
%doc %{_mandir}/man3/libswresample.3*
%doc %{_mandir}/man3/libswscale.3*
%{_datadir}/ffmpeg/examples

%files -n %{statname}
%{_libdir}/*.a
