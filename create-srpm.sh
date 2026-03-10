#!/bin/bash
# Script to create SRPM for Hyprland and Portal
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Function to parse versions from a spec file
parse_spec_global() {
    local spec=$1
    local var=$2
    grep -oP "^%global $var\\s+\\K\\S+" "$spec"
}

download() {
    local file=$1
    local url=$2
    if [ ! -f "sources/$file" ]; then
        echo "Downloading $file..."
        curl -L -o "sources/$file" "$url"
    else
        echo "$file already exists, skipping."
    fi
}

mkdir -p sources srpm

# Determine Fedora version for dist suffix
FEDORA_VER=$(rpm -E %fedora)
[ "$FEDORA_VER" = "%fedora" ] && FEDORA_VER="43"
DIST_VAL=".fc$FEDORA_VER"

# Process Hyprland SPEC
SPEC_HYPR="hyprland.spec"
if [ -f "$SPEC_HYPR" ]; then
    echo "=== Processing $SPEC_HYPR ==="
    V_HYPR=$(parse_spec_global "$SPEC_HYPR" "hyprland_version")
    V_PROT=$(parse_spec_global "$SPEC_HYPR" "hyprland_protocols_ver")
    V_SCAN=$(parse_spec_global "$SPEC_HYPR" "hyprwayland_scanner_ver")
    V_UTIL=$(parse_spec_global "$SPEC_HYPR" "hyprutils_ver")
    V_LANG=$(parse_spec_global "$SPEC_HYPR" "hyprlang_ver")
    V_CURS=$(parse_spec_global "$SPEC_HYPR" "hyprcursor_ver")
    V_GRAP=$(parse_spec_global "$SPEC_HYPR" "hyprgraphics_ver")
    V_AQUA=$(parse_spec_global "$SPEC_HYPR" "aquamarine_ver")
    V_WIRE=$(parse_spec_global "$SPEC_HYPR" "hyprwire_ver")
    V_GLAZ=$(parse_spec_global "$SPEC_HYPR" "glaze_ver")
    B_ASSET=$(parse_spec_global "$SPEC_HYPR" "build_assets_release")

    download "hyprland-${V_HYPR}.tar.gz" "https://github.com/hyprwm/Hyprland/archive/refs/tags/v${V_HYPR}.tar.gz"
    download "hyprland-protocols-${V_PROT}.tar.gz" "https://github.com/hyprwm/hyprland-protocols/archive/refs/tags/v${V_PROT}.tar.gz"
    download "hyprwayland-scanner-${V_SCAN}.tar.gz" "https://github.com/hyprwm/hyprwayland-scanner/archive/refs/tags/v${V_SCAN}.tar.gz"
    download "hyprutils-${V_UTIL}.tar.gz" "https://github.com/hyprwm/hyprutils/archive/refs/tags/v${V_UTIL}.tar.gz"
    download "hyprlang-${V_LANG}.tar.gz" "https://github.com/hyprwm/hyprlang/archive/refs/tags/v${V_LANG}.tar.gz"
    download "hyprcursor-${V_CURS}.tar.gz" "https://github.com/hyprwm/hyprcursor/archive/refs/tags/v${V_CURS}.tar.gz"
    download "hyprgraphics-${V_GRAP}.tar.gz" "https://github.com/hyprwm/hyprgraphics/archive/refs/tags/v${V_GRAP}.tar.gz"
    download "aquamarine-${V_AQUA}.tar.gz" "https://github.com/hyprwm/aquamarine/archive/refs/tags/v${V_AQUA}.tar.gz"
    download "hyprwire-${V_WIRE}.tar.gz" "https://github.com/hyprwm/hyprwire/archive/refs/tags/v${V_WIRE}.tar.gz"
    download "glaze-${V_GLAZ}.tar.gz" "https://github.com/stephenberry/glaze/archive/refs/tags/v${V_GLAZ}.tar.gz"
    
    # Note: Using the known working patched version of udis86 for Hyprland
    download "udis86-hyprland.tar.gz" "https://github.com/AshBuk/Hyprland-Fedora/releases/download/${B_ASSET}/udis86-hyprland.tar.gz"

    rpmbuild -bs "$SPEC_HYPR" \
             --define "_sourcedir $SCRIPT_DIR/sources" \
             --define "_srcrpmdir $SCRIPT_DIR/srpm" \
             --define "dist $DIST_VAL"
fi

# Process Portal SPEC
SPEC_PORTAL="xdg-desktop-portal-hyprland.spec"
if [ -f "$SPEC_PORTAL" ]; then
    echo "=== Processing $SPEC_PORTAL ==="
    V_PORTAL=$(parse_spec_global "$SPEC_PORTAL" "portal_version")
    download "xdg-desktop-portal-hyprland-${V_PORTAL}.tar.gz" "https://github.com/hyprwm/xdg-desktop-portal-hyprland/archive/refs/tags/v${V_PORTAL}.tar.gz"
    
    rpmbuild -bs "$SPEC_PORTAL" \
             --define "_sourcedir $SCRIPT_DIR/sources" \
             --define "_srcrpmdir $SCRIPT_DIR/srpm" \
             --define "dist $DIST_VAL"
fi

echo "=== SRPMs created successfully! ==="
ls -la srpm/*.src.rpm
