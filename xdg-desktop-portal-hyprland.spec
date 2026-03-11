# Copyright (c) 2026 Eugen Iofciu Vasile
# SPDX-License-Identifier: MIT

# =============================================================================
# Version definitions (single source of truth)
# =============================================================================
%global portal_version          1.3.11
%global portal_commit           5179fb3
%global portal_date             2026-03-10
%global hyprland_min_ver        0.54.0
%global hyprwayland_scanner_ver 0.4.5
%global hyprutils_ver           0.11.0
%global hyprlang_ver            0.6.8
%global hyprland_protocols_ver  0.7.0

Name:           xdg-desktop-portal-hyprland
Version:        %{portal_version}
Release:        1%{?dist}
Summary:        XDG Desktop Portal backend for Hyprland
License:        BSD-3-Clause
URL:            https://github.com/hyprwm/xdg-desktop-portal-hyprland

# Main source
Source0:        https://github.com/hyprwm/xdg-desktop-portal-hyprland/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

# Vendored Hyprland libs (same versions as hyprland package)
Source10:       https://github.com/hyprwm/hyprwayland-scanner/archive/refs/tags/v%{hyprwayland_scanner_ver}.tar.gz#/hyprwayland-scanner-%{hyprwayland_scanner_ver}.tar.gz
Source11:       https://github.com/hyprwm/hyprutils/archive/refs/tags/v%{hyprutils_ver}.tar.gz#/hyprutils-%{hyprutils_ver}.tar.gz
Source12:       https://github.com/hyprwm/hyprlang/archive/refs/tags/v%{hyprlang_ver}.tar.gz#/hyprlang-%{hyprlang_ver}.tar.gz
Source13:       https://github.com/hyprwm/hyprland-protocols/archive/refs/tags/v%{hyprland_protocols_ver}.tar.gz#/hyprland-protocols-%{hyprland_protocols_ver}.tar.gz

# Build dependencies
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  pkgconf-pkg-config
BuildRequires:  pugixml-devel
BuildRequires:  pixman-devel
BuildRequires:  pipewire-devel >= 1.1.82
BuildRequires:  sdbus-cpp-devel >= 2.0.0
BuildRequires:  libdrm-devel
BuildRequires:  mesa-libgbm-devel
BuildRequires:  wayland-devel
BuildRequires:  wayland-protocols-devel
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtwayland-devel

# Runtime deps
Requires:       hyprland >= %{hyprland_min_ver}
Requires:       xdg-desktop-portal
Requires:       pipewire >= 1.1.82

%description
XDG Desktop Portal backend for Hyprland that provides screen sharing,
file dialogs, and other desktop integration features.
This build uses isolated Hyprland libraries.

%prep
%autosetup -n %{name}-%{version}

# Unpack vendored deps
tar -xzf %{SOURCE10}
tar -xzf %{SOURCE11}
tar -xzf %{SOURCE12}
tar -xzf %{SOURCE13}

%build
VENDOR_PREFIX="$(pwd)/vendor"
export PATH="$VENDOR_PREFIX/bin:$PATH"
export PKG_CONFIG_PATH="$VENDOR_PREFIX/lib64/pkgconfig:$VENDOR_PREFIX/lib/pkgconfig:%{_libdir}/pkgconfig:%{_datadir}/pkgconfig"
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

# 4) hyprland-protocols
pushd hyprland-protocols-%{hyprland_protocols_ver}
meson setup build --prefix="$VENDOR_PREFIX"
ninja -C build
ninja -C build install
popd

# 5) xdg-desktop-portal-hyprland
VENDOR_RPATH='%{_libexecdir}/hyprland/vendor/lib64:%{_libexecdir}/hyprland/vendor/lib'

export VERSION="%{portal_version}"
export GIT_COMMIT_HASH="%{portal_commit}"

cmake -B build \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_INSTALL_PREFIX=%{_prefix} \
  -DCMAKE_PREFIX_PATH="$VENDOR_PREFIX" \
  -DCMAKE_CXX_FLAGS="$GCC15_CXXFLAGS" \
  -DCMAKE_INSTALL_RPATH="$VENDOR_RPATH" \
  -DCMAKE_BUILD_WITH_INSTALL_RPATH=ON \
  -DVERSION="%{portal_version}"
cmake --build build --parallel %{_smp_build_ncpus}

%install
DESTDIR=%{buildroot} cmake --install build

%files
%license LICENSE
%doc README.md
%{_libexecdir}/xdg-desktop-portal-hyprland
%{_bindir}/hyprland-share-picker
%{_datadir}/xdg-desktop-portal/portals/hyprland.portal
%{_datadir}/dbus-1/services/org.freedesktop.impl.portal.desktop.hyprland.service
%{_userunitdir}/xdg-desktop-portal-hyprland.service

%changelog
* Tue Mar 10 2026 Eugen Iofciu Vasile <eugen@iofciu.vasile> - 1.3.11-1
- Initial release for original Hyprland Fedora Packager
