#!/usr/bin/env python3

import subprocess
import json
import hashlib
from pathlib import Path

DEBUG = False


def list_digest(strings):
    strings.sort()
    sha1 = hashlib.sha1()
    for s in strings:
        sha1.update(s.encode())
        sha1.update(b'\0')
    return sha1.hexdigest()


result = subprocess.run(['swaymsg', '-t', 'get_outputs'], stdout=subprocess.PIPE)
outputs = json.loads(result.stdout)
monitor_serials = [monitor['serial'] for monitor in outputs]
configuration_identifier = list_digest(monitor_serials)
configuration_file = Path(configuration_identifier)
if configuration_file.is_file():
    with open(configuration_file, 'r') as read_file:
        configuration = json.load(read_file)
        # Enable / disable outputs first
        for output in configuration:
            if output['active']:
                result = subprocess.run(['swaymsg', 'output', output['name'], 'enable'], stdout=subprocess.PIPE)
                if DEBUG:
                    print(result.args)
                if result.returncode != 0:
                    print("Enabling " + output['name'] + " failed.")
            else:
                result = subprocess.run(['swaymsg', 'output', output['name'], 'disable'], stdout=subprocess.PIPE)
                if DEBUG:
                    print(result.args)
                if result.returncode != 0:
                    print("Disabling " + output['name'] + " failed.")

        # Now set mode, scale and position
        for output in configuration:
            if output['active']:
                result = subprocess.run(['swaymsg', 'output', output['name'],
                                         'mode', output['mode'],
                                         'scale', str(output['scale']),
                                         'pos', str(output['x_pos']), str(output['y_pos'])]
                                        , stdout=subprocess.PIPE)
                if DEBUG:
                    print(result.args)
                if result.returncode != 0:
                    print("Setting configuration for " + output['name'] + " failed.")
else:
    config = []
    for output_desc in outputs:
        output_cfg = {key: output_desc[key] for key in ['name', 'serial', 'active']}
        if output_desc['active']:
            output_cfg['scale'] = output_desc['scale']
            output_cfg['mode'] = str(output_desc['rect']['width']) + 'x' + str(output_desc['rect']['height'])
            output_cfg['x_pos'] = str(output_desc['rect']['x'])
            output_cfg['y_pos'] = str(output_desc['rect']['y'])
        else:
            output_cfg['scale'] = 1
            output_cfg['mode'] = '800x600'
            output_cfg['x_pos'] = '0'
            output_cfg['y_pos'] = '0'
        config.append(output_cfg)
    with open(configuration_file, "w") as data_file:
        json.dump(config, data_file, indent=4)
    print("Empty configuration created for " + str(configuration_identifier))
    # in case the user did things wrong: enable at least 1 output
    active_outputs = [output for output in outputs if output['active']]
    if not active_outputs:
        output_desc = outputs[0]
        result = subprocess.run(['swaymsg', 'output', output_desc['name'], 'enable'], stdout=subprocess.PIPE)
