install: SwayMonMan.py 95-monitor.rules
	@cp SwayMonMan.py /usr/local/bin/SwayMonMan
	@cp 95-monitor.rules /etc/udev/rules.d/95-monitor.rules
	@echo "You may need to reload udev or reboot"

uninstall:
	@rm -f /usr/local/bin/SwayMonMan
	@rm -f /etc/udev/rules.d/95-monitor.rules
