#!/bin/sh
sudo dnf install 'pkgconfig(x264)' 'pkgconfig(x265)' 'pkgconfig(fdk-aac)' faad2-devel 'pkgconfig(opencore-amrwb)' 'pkgconfig(opencore-amrnb)' xvid-devel
LOCALDIR=$(realpath $(dirname $0))
TMPDIR=`mktemp -d /tmp/mmheadersXXXXXX`
mkdir -p $TMPDIR/localinc
cd /usr/include
cp -a fdk-aac neaacdec.h opencore-amrwb opencore-amrnb x264_config.h x264.h x265_config.h x265.h xvid.h $TMPDIR/localinc
cd $TMPDIR
tar cJf $LOCALDIR/restricted-multimedia-headers.tar.xz localinc
cd $LOCALDIR
rm -rf $TMPDIR
