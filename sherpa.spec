### RPM external sherpa 1.3.1

#Source: http://cern.ch/service-spi/external/MCGenerators/distribution/sherpa-%{realversion}-src.tgz
Source: http://www.hepforge.org/archive/sherpa/SHERPA-MC-%{realversion}.tar.gz
#Patch0: sherpa-1.3.0-nlo_event_generation_1
Patch1: sherpa-1.3.1-fix-gcc47-cxx11
Requires: hepmc lhapdf

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx g++
%endif

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -O2 -std=c++0x
%endif

%prep
#%setup -n sherpa/%{realversion}
%setup -q -n SHERPA-MC-%{realversion}
#%patch0 -p0

# Apply C++11 / gcc 4.7.x fixes only if using a 47x architecture.
# See http://gcc.gnu.org/gcc-4.7/porting_to.html
case %cmsplatf in
  *gcc4[789]*)
%patch1 -p1
  ;;
esac

autoreconf -i --force

# Force architecture based on %%cmsplatf
case %cmsplatf in
  *_amd64_gcc*) ARCH_CMSPLATF="-m64" ;;
  *_ia32_gcc*) ARCH_CMSPLATF="-m32" ;;
esac

case %cmsplatf in
  osx*)
    perl -p -i -e 's|-rdynamic||g' \
      configure \
      AddOns/Analysis/Scripts/Makefile.in
  ;;
esac

./configure --prefix=%i --enable-analysis \
            --enable-hepmc2=$HEPMC_ROOT --enable-lhapdf=$LHAPDF_ROOT \
            --enable-multithread CXX="%cms_cxx" CXXFLAGS="-fuse-cxa-atexit $ARCH_CMSPLATF %cms_cxxflags"

%build
# Fix up a configuration mistake coming from a test being confused
# by the "skipping incompatible" linking messages when linking 32bit on 64bit
find . -name Makefile -exec perl -p -i -e 's|/usr/lib64/libm.a||g;s|/usr/lib64/libc.a||g;' {} \;

make %{makeprocesses} 

%install
make install

