# SwayMonMan

An easy-to-use manager for complex monitor setups in changing environments using sway

## How to use SwayMonMan

### Install

Install by running `make install` with root privileges (make sure /usr/local/bin is in your $PATH)

### Configuration

1. Connect your monitors, enable/disable as desired
2. The configuration file for your current setup is located at $XGD_CONFIG_HOME/SwayMonMan/ (usually ~/.config/SwayMonMan/)
3. Edit the created config file.

### Use SwayMonMan

SwayMonMan is automatically executed on every DRM change detected by udev. 

If you need to run it manually, just run `SwayMonMan`

### Uninstall

Before you uninstall SwayMonMan, consider opening an issue or provide a patch;)

If you really want to get rid of SwayMonMan, run `make uninstal` with root privileges.
