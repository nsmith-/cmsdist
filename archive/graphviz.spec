### RPM external graphviz 2.49.0
Source: https://gitlab.com/api/v4/projects/4207231/packages/generic/%{n}-releases/%{realversion}/%{n}-%{realversion}.tar.gz
Requires: expat zlib libjpeg-turbo libpng
BuildRequires: autotools
%prep
%setup -n %{n}-%{realversion}

# Update config.{guess,sub} scripts to detect aarch64 and ppc64le
rm -f %{_tmppath}/config.{sub,guess}
%get_config_guess %{_tmppath}/config.guess
%get_config_sub %{_tmppath}/config.sub
for CONFIG_GUESS_FILE in $(find $RPM_BUILD_DIR -name 'config.guess')
do
  rm -f $CONFIG_GUESS_FILE
  cp %{_tmppath}/config.guess $CONFIG_GUESS_FILE
  chmod +x $CONFIG_GUESS_FILE
done
for CONFIG_SUB_FILE in $(find $RPM_BUILD_DIR -name 'config.sub')
do
  rm -f $CONFIG_SUB_FILE
  cp %{_tmppath}/config.sub $CONFIG_SUB_FILE
  chmod +x $CONFIG_SUB_FILE
done

%build
%ifnos darwin
        ADDITIONAL_OPTIONS="--with-freetype2=no --disable-shared --enable-static --disable-ltdl"
%else
        ADDITIONAL_OPTIONS="--with-freetype2=no"
%endif
./configure \
  --disable-silent-rules \
  --with-expatlibdir=$EXPAT_ROOT/lib \
  --with-expatincludedir=$EXPAT_ROOT/include \
  --with-zincludedir=$ZLIB_ROOT/include \
  --with-zlibdir=$ZLIB_ROOT/lib \
  --with-pngincludedir=$LIBPNG_ROOT/include \
  --with-pnglibdir=$LIBPNG_ROOT/lib \
  --with-jpegincludedir=$LIBJPEG_TURBO_ROOT/include \
  --with-jpeglibdir=$LIBJPEG_TURBO_ROOT/lib64 \
  --without-x \
  --without-tclsh \
  --without-tcl \
  --without-fontconfig \
  --without-tk \
  --without-perl \
  --without-python \
  --without-ruby \
  --disable-ruby \
  --disable-perl \
  --without-pangocairo \
  --without-fontconfig \
  --without-gdk-pixbuf \
  --with-libgd=no \
  --disable-sharp \
  --disable-guile \
  --disable-java \
  --disable-lua \
  --disable-ocaml \
  --disable-perl \
  --disable-php \
  --disable-python \
  --with-qt=no \
  --prefix=%{i} \
  $ADDITIONAL_OPTIONS

make %{makeprocesses}

%install
make install
%define drop_files %{i}/share

rm -rf %{i}/lib/pkgconfig

# To match configure options above
%ifnos darwin
        ln -s dot_static %{i}/bin/dot
%endif
# Drop static libraries.
rm -rf %{i}/lib/*.{l,}a
