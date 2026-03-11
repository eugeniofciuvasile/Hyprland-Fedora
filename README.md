# Hyprland for Fedora
[![Copr build status](https://copr.fedorainfracloud.org/coprs/mreuz/Hyprland-Fedora/package/hyprland/status_image/last_build.png)](https://copr.fedorainfracloud.org/coprs/mreuz/Hyprland-Fedora/package/hyprland/)

**The latest stable Hyprland releases for Fedora, built using modern, isolated packaging.**

This project provides RPM specification files and build scripts to package Hyprland and its core components for Fedora. The goal is a "hermetic" build that is stable and doesn't interfere with your system libraries.

### Key Features

- **Isolated Build:** Core Hyprland libraries (`aquamarine`, `hyprlang`, etc.) are built from source and installed to a private directory (`/usr/libexec/hyprland/vendor/`).
- **RPATH Linking:** Binaries find their libraries via `RPATH`, avoiding any need for global `LD_LIBRARY_PATH` changes.
- **Clean Integration:** Packages integrate seamlessly with `dnf` and avoid version conflicts with official Fedora repos.
- **Support for Fedora 41+:** Optimized for modern Fedora releases.

### Quick Start (Local Build)

1. **Install tools:**
   ```bash
   sudo dnf install rpm-build mock curl grep rpm-devtools
   ```
2. **Create SRPM:**
   ```bash
   ./create-srpm.sh
   ```
3. **Build RPM (using Mock):**
   ```bash
   mock -r fedora-43-x86_64 --rebuild srpm/*.src.rpm
   ```

### COPR Setup (Automated Build)

1. Create a project on [Fedora COPR](https://copr.fedorainfracloud.org/).
2. Enable "GitHub integration" pointing to your repository.
3. Use the build command: `./create-srpm.sh && cp srpm/*.src.rpm .`
4. COPR will build the packages for you, allowing easy installation via:
   ```bash
   sudo dnf copr enable [username]/[project]
   sudo dnf install hyprland xdg-desktop-portal-hyprland
   ```

### Included Packages

- `hyprland`: The compositor, `hyprctl`, `hyprpm`, and `start-hyprland`.
- `xdg-desktop-portal-hyprland`: Screen sharing and portal backend support.

## License

This project's build scripts and SPEC files are licensed under the **MIT License**. Upstream Hyprland and its libraries are licensed under their respective terms (BSD-3-Clause).
