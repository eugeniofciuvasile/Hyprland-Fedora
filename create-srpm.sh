#!/bin/bash
# Script to create SRPM for Hyprland or Portal
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_SPEC=$1 # Optional: specific spec file to build

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

process_spec() {
    local spec=$1
    echo "=== Processing $spec ==="
    
    if [[ "$spec" == "hyprland.spec" ]]; then
        V_HYPR=$(parse_spec_global "$spec" "hyprland_version")
        V_PROT=$(parse_spec_global "$spec" "hyprland_protocols_ver")
        V_SCAN=$(parse_spec_global "$spec" "hyprwayland_scanner_ver")
        V_UTIL=$(parse_spec_global "$spec" "hyprutils_ver")
        V_LANG=$(parse_spec_global "$spec" "hyprlang_ver")
        V_CURS=$(parse_spec_global "$spec" "hyprcursor_ver")
        V_GRAP=$(parse_spec_global "$spec" "hyprgraphics_ver")
        V_AQUA=$(parse_spec_global "$spec" "aquamarine_ver")
        V_WIRE=$(parse_spec_global "$spec" "hyprwire_ver")
        V_GLAZ=$(parse_spec_global "$spec" "glaze_ver")
        B_ASSET=$(parse_spec_global "$spec" "build_assets_release")

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
        download "udis86-hyprland.tar.gz" "https://github.com/AshBuk/Hyprland-Fedora/releases/download/${B_ASSET}/udis86-hyprland.tar.gz"

        # NEW: Fetch commit info with User-Agent and Error Handling
        echo "Fetching commit info for v${V_HYPR}..."
        COMMIT_INFO=$(curl -s -H "User-Agent: Fedora-Copr-Builder" "https://api.github.com/repos/hyprwm/Hyprland/commits/v${V_HYPR}") || true
        
        HASH=$(echo "$COMMIT_INFO" | grep '"sha":' | head -n1 | cut -d'"' -f4 || echo "unknown")
        DATE=$(echo "$COMMIT_INFO" | grep '"date":' | head -n1 | cut -d'"' -f4 || echo "unknown")
        MESSAGE=$(echo "$COMMIT_INFO" | grep '"message":' | head -n1 | cut -d'"' -f4 | head -n1 || echo "unknown")
        
        [ -z "$HASH" ] && HASH="unknown"
        [ -z "$DATE" ] && DATE="unknown"

        echo "HASH: $HASH"
        echo "HASH=$HASH" > sources/metadata.env
        echo "DATE=$DATE" >> sources/metadata.env
        echo "BRANCH=tags/v$V_HYPR" >> sources/metadata.env
        echo "MESSAGE=$MESSAGE" >> sources/metadata.env
    
    elif [[ "$spec" == "xdg-desktop-portal-hyprland.spec" ]]; then
        V_PORTAL=$(parse_spec_global "$spec" "portal_version")
        V_PROT=$(parse_spec_global "$spec" "hyprland_protocols_ver")
        V_SCAN=$(parse_spec_global "$spec" "hyprwayland_scanner_ver")
        V_UTIL=$(parse_spec_global "$spec" "hyprutils_ver")
        V_LANG=$(parse_spec_global "$spec" "hyprlang_ver")

        download "xdg-desktop-portal-hyprland-${V_PORTAL}.tar.gz" "https://github.com/hyprwm/xdg-desktop-portal-hyprland/archive/refs/tags/v${V_PORTAL}.tar.gz"
        download "hyprland-protocols-${V_PROT}.tar.gz" "https://github.com/hyprwm/hyprland-protocols/archive/refs/tags/v${V_PROT}.tar.gz"
        download "hyprwayland-scanner-${V_SCAN}.tar.gz" "https://github.com/hyprwm/hyprwayland-scanner/archive/refs/tags/v${V_SCAN}.tar.gz"
        download "hyprutils-${V_UTIL}.tar.gz" "https://github.com/hyprwm/hyprutils/archive/refs/tags/v${V_UTIL}.tar.gz"
        download "hyprlang-${V_LANG}.tar.gz" "https://github.com/hyprwm/hyprlang/archive/refs/tags/v${V_LANG}.tar.gz"
    fi

    rpmbuild -bs "$spec" \
             --define "_sourcedir $SCRIPT_DIR/sources" \
             --define "_srcrpmdir $SCRIPT_DIR/srpm" \
             --define "dist $DIST_VAL"
}

if [ -n "$TARGET_SPEC" ]; then
    process_spec "$TARGET_SPEC"
else
    for s in *.spec; do
        process_spec "$s"
    done
fi

echo "=== SRPMs created successfully! ==="
ls -la srpm/*.src.rpm
