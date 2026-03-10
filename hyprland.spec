# Copyright (c) 2026 Eugen Iofciu Vasile
# SPDX-License-Identifier: MIT

# =============================================================================
# Version definitions (single source of truth)
# =============================================================================
%global hyprland_version        0.54.2
%global hyprland_protocols_ver  0.7.0
%global hyprwayland_scanner_ver 0.4.5
%global hyprutils_ver           0.11.0
%global hyprlang_ver            0.6.8
%global hyprcursor_ver          0.1.13
%global hyprgraphics_ver        0.5.0
%global aquamarine_ver          0.10.0
%global hyprwire_ver            0.3.0
%global glaze_ver               7.0.0

# Build assets release (udis86, glaze tarballs)
%global build_assets_release    v0.54-fedora

# Exclude auto-requires for vendored Hyprland libraries
%global __requires_exclude pkgconfig\\((aquamarine|hyprutils|hyprlang|hyprcursor|hyprgraphics|hyprwayland-scanner|hyprland-protocols|hyprwire)\\)

Name:           hyprland
Version:        %{hyprland_version}
Release:        1%{?dist}
Summary:        Dynamic tiling Wayland compositor
License:        BSD-3-Clause
URL:            https://github.com/hyprwm/Hyprland

# Main source
Source0:        https://github.com/hyprwm/Hyprland/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

# Git submodules
Source10:       https://github.com/hyprwm/hyprland-protocols/archive/refs/tags/v%{hyprland_protocols_ver}.tar.gz#/hyprland-protocols-%{hyprland_protocols_ver}.tar.gz
Source11:       https://github.com/AshBuk/Hyprland-Fedora/releases/download/%{build_assets_release}/udis86-hyprland.tar.gz

# Hyprland pinned deps
Source20:       https://github.com/hyprwm/hyprwayland-scanner/archive/refs/tags/v%{hyprwayland_scanner_ver}.tar.gz#/hyprwayland-scanner-%{hyprwayland_scanner_ver}.tar.gz
Source21:       https://github.com/hyprwm/hyprutils/archive/refs/tags/v%{hyprutils_ver}.tar.gz#/hyprutils-%{hyprutils_ver}.tar.gz
Source22:       https://github.com/hyprwm/hyprlang/archive/refs/tags/v%{hyprlang_ver}.tar.gz#/hyprlang-%{hyprlang_ver}.tar.gz
Source23:       https://github.com/hyprwm/hyprcursor/archive/refs/tags/v%{hyprcursor_ver}.tar.gz#/hyprcursor-%{hyprcursor_ver}.tar.gz
Source24:       https://github.com/hyprwm/hyprgraphics/archive/refs/tags/v%{hyprgraphics_ver}.tar.gz#/hyprgraphics-%{hyprgraphics_ver}.tar.gz
Source25:       https://github.com/hyprwm/aquamarine/archive/refs/tags/v%{aquamarine_ver}.tar.gz#/aquamarine-%{aquamarine_ver}.tar.gz
Source26:       https://github.com/hyprwm/hyprwire/archive/refs/tags/v%{hyprwire_ver}.tar.gz#/hyprwire-%{hyprwire_ver}.tar.gz
Source30:       https://github.com/stephenberry/glaze/archive/refs/tags/v%{glaze_ver}.tar.gz#/glaze-%{glaze_ver}.tar.gz

# Build dependencies
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  git
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  pkgconf-pkg-config
BuildRequires:  python3
BuildRequires:  cairo-devel
BuildRequires:  glm-devel
BuildRequires:  glslang-devel
BuildRequires:  hwdata
BuildRequires:  libdisplay-info-devel
BuildRequires:  libdrm-devel
BuildRequires:  libepoxy-devel
BuildRequires:  mesa-libgbm-devel
BuildRequires:  mesa-libEGL-devel
BuildRequires:  libglvnd-devel
BuildRequires:  libglvnd-gles
BuildRequires:  libinput-devel
BuildRequires:  libjxl-devel
BuildRequires:  libliftoff-devel
BuildRequires:  libspng-devel
BuildRequires:  libwebp-devel
BuildRequires:  libxcb-devel
BuildRequires:  libXcursor-devel
BuildRequires:  libxcvt-devel
BuildRequires:  libxkbcommon-devel
BuildRequires:  pango-devel
BuildRequires:  pixman-devel
BuildRequires:  pugixml-devel
BuildRequires:  re2-devel
BuildRequires:  scdoc
BuildRequires:  libseat-devel
BuildRequires:  systemd-devel
BuildRequires:  tomlplusplus-devel
BuildRequires:  wayland-devel
BuildRequires:  wayland-protocols-devel
BuildRequires:  libzip-devel
BuildRequires:  librsvg2-devel
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  libpng-devel
BuildRequires:  file-devel
BuildRequires:  xcb-util-devel
BuildRequires:  xcb-util-errors-devel
BuildRequires:  xcb-util-image-devel
BuildRequires:  xcb-util-renderutil-devel
BuildRequires:  xcb-util-wm-devel
BuildRequires:  xorg-x11-server-Xwayland
BuildRequires:  libXfont2-devel
BuildRequires:  xkeyboard-config
BuildRequires:  glib2-devel
BuildRequires:  libuuid-devel
BuildRequires:  libffi-devel
BuildRequires:  muParser-devel

# Runtime deps
Requires:       cairo
Requires:       hwdata
Requires:       libdisplay-info
Requires:       libdrm
Requires:       libepoxy
Requires:       mesa-libgbm
Requires:       libinput
Requires:       libjxl
Requires:       libliftoff
Requires:       libspng
Requires:       libwebp
Requires:       libxcb
Requires:       libXcursor
Requires:       libxcvt
Requires:       libxkbcommon
Requires:       pango
Requires:       pixman
Requires:       pugixml
Requires:       re2
Requires:       libseat
Requires:       libwayland-client
Requires:       libwayland-server
Requires:       libzip
Requires:       librsvg2
Requires:       xcb-util
Requires:       xcb-util-errors
Requires:       xcb-util-image
Requires:       xcb-util-renderutil
Requires:       xcb-util-wm
Requires:       xorg-x11-server-Xwayland
Requires:       libffi
Requires:       muParser

%description
Hyprland is a dynamic tiling Wayland compositor with modern Wayland features.
This build vendors core Hyprland libraries to ensure stability on Fedora.

%prep
%autosetup -n Hyprland-%{version}

# Unpack submodules
rm -rf subprojects/hyprland-protocols subprojects/udis86
tar -xzf %{SOURCE10} -C subprojects
mv subprojects/hyprland-protocols-%{hyprland_protocols_ver} subprojects/hyprland-protocols
tar -xzf %{SOURCE11} -C subprojects

# Unpack vendored deps
tar -xzf %{SOURCE20}
tar -xzf %{SOURCE21}
tar -xzf %{SOURCE22}
tar -xzf %{SOURCE23}
tar -xzf %{SOURCE24}
tar -xzf %{SOURCE25}
tar -xzf %{SOURCE26}
tar -xzf %{SOURCE30}

%build
mkdir -p pkgconfig
cat > pkgconfig/hwdata.pc << 'EOF'
prefix=/usr
datarootdir=${prefix}/share
pkgdatadir=${datarootdir}/hwdata
Name: hwdata
Description: Hardware identification databases
Version: 0.385
EOF

VENDOR_PREFIX="$(pwd)/vendor"
export PATH="$VENDOR_PREFIX/bin:$PATH"
export PKG_CONFIG_PATH="$VENDOR_PREFIX/lib64/pkgconfig:$VENDOR_PREFIX/lib/pkgconfig:$(pwd)/pkgconfig:%{_libdir}/pkgconfig:%{_datadir}/pkgconfig"
export CMAKE_PREFIX_PATH="$VENDOR_PREFIX"

GCC15_CXXFLAGS="%{optflags} -fpermissive"

# 1) hyprwayland-scanner
pushd hyprwayland-scanner-%{hyprwayland_scanner_ver}
cmake -B build -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="$VENDOR_PREFIX" -DCMAKE_INSTALL_LIBDIR=lib64
cmake --build build --parallel %{_smp_build_ncpus}
cmake --install build
popd

# 2) hyprutils
pushd hyprutils-%{hyprutils_ver}
cmake -B build -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="$VENDOR_PREFIX" -DCMAKE_INSTALL_LIBDIR=lib64
cmake --build build --parallel %{_smp_build_ncpus}
cmake --install build
popd

# 3) hyprlang
pushd hyprlang-%{hyprlang_ver}
cmake -B build -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="$VENDOR_PREFIX" -DCMAKE_INSTALL_LIBDIR=lib64
cmake --build build --parallel %{_smp_build_ncpus}
cmake --install build
popd

# 4) hyprcursor
pushd hyprcursor-%{hyprcursor_ver}
cmake -B build -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="$VENDOR_PREFIX" -DCMAKE_INSTALL_LIBDIR=lib64
cmake --build build --parallel %{_smp_build_ncpus}
cmake --install build
popd

# 5) hyprgraphics
pushd hyprgraphics-%{hyprgraphics_ver}
cmake -B build -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="$VENDOR_PREFIX" -DCMAKE_INSTALL_LIBDIR=lib64
cmake --build build --parallel %{_smp_build_ncpus}
cmake --install build
popd

# 6) aquamarine
pushd aquamarine-%{aquamarine_ver}
cmake -B build -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="$VENDOR_PREFIX" \
  -DCMAKE_INSTALL_LIBDIR=lib64 -DCMAKE_CXX_FLAGS="$GCC15_CXXFLAGS" \
  -DOpenGL_GL_PREFERENCE=GLVND
cmake --build build --parallel %{_smp_build_ncpus}
cmake --install build
popd

# 7) hyprwire
pushd hyprwire-%{hyprwire_ver}
cmake -B build -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="$VENDOR_PREFIX" -DCMAKE_INSTALL_LIBDIR=lib64
cmake --build build --parallel %{_smp_build_ncpus}
cmake --install build
popd

# 8) hyprland-protocols
pushd subprojects/hyprland-protocols
meson setup build --prefix="$VENDOR_PREFIX"
ninja -C build
ninja -C build install
popd

# 9) glaze
pushd glaze-%{glaze_ver}
cmake -B build -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="$VENDOR_PREFIX" -Dglaze_DEVELOPER_MODE=OFF -DBUILD_TESTING=OFF
cmake --install build
popd

# 10) Hyprland
VENDOR_RPATH='$ORIGIN/../libexec/hyprland/vendor/lib64:$ORIGIN/../libexec/hyprland/vendor/lib'
cmake -B build \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_INSTALL_PREFIX=%{_prefix} \
  -DCMAKE_PREFIX_PATH="$VENDOR_PREFIX" \
  -DCMAKE_CXX_FLAGS="$GCC15_CXXFLAGS -I$VENDOR_PREFIX/include" \
  -DBUILD_TESTING=OFF \
  -DCMAKE_INSTALL_RPATH="$VENDOR_RPATH" \
  -DCMAKE_BUILD_WITH_INSTALL_RPATH=ON
cmake --build build --parallel %{_smp_build_ncpus}

%install
VENDOR_PREFIX="$(pwd)/vendor"
DESTDIR=%{buildroot} cmake --install build
ln -sf Hyprland %{buildroot}%{_bindir}/hyprland

# Install vendored runtime libs
VENDOR_DST=%{buildroot}%{_libexecdir}/%{name}/vendor
install -d "$VENDOR_DST/lib64" "$VENDOR_DST/lib"
cp -a "$VENDOR_PREFIX"/lib64/lib*.so* "$VENDOR_DST/lib64/" 2>/dev/null || true
cp -a "$VENDOR_PREFIX"/lib/lib*.so*   "$VENDOR_DST/lib/"   2>/dev/null || true

%files
%license LICENSE
%doc README.md
%{_bindir}/Hyprland
%{_bindir}/hyprland
%{_bindir}/hyprctl
%{_bindir}/hyprpm
%{_bindir}/start-hyprland
%dir %{_libexecdir}/%{name}
%{_libexecdir}/%{name}/vendor/
%{_datadir}/wayland-sessions/hyprland.desktop
%{_datadir}/hypr/
%{_datadir}/xdg-desktop-portal/hyprland-portals.conf
%{_includedir}/hyprland/
%{_datadir}/pkgconfig/hyprland.pc
%{_mandir}/man1/Hyprland.1*
%{_mandir}/man1/hyprctl.1*
%{_datadir}/bash-completion/completions/hyprctl
%{_datadir}/bash-completion/completions/hyprpm
%{_datadir}/fish/vendor_completions.d/hyprctl.fish
%{_datadir}/fish/vendor_completions.d/hyprpm.fish
%{_datadir}/zsh/site-functions/_hyprctl
%{_datadir}/zsh/site-functions/_hyprpm

%changelog
* Tue Mar 10 2026 Eugen Iofciu Vasile <eugen@iofciu.vasile> - 0.54.2-1
- Initial build for original Hyprland Fedora Packager
