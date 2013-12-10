# -*- coding: utf-8 -*-

"""
Manage Block Devices using blockdev
===================================

The utility blockdev allows one to call block device input/output controls from the command line.
"""

import os
import logging
from salt import exceptions, utils

log = logging.getLogger(__name__)

log = logging.getLogger(__name__)
log.debug("module blockdev loaded")


def __virtual__():
    """
    Verify blockdev is installed.
    """
    try:
        utils.check_or_die('blockdev')
        log.debug("blockdev is available")
    except exceptions.CommandNotFoundError:
        log.error("blockdev is not available")
        return False
    return 'blockdev'


def _error(ret, message):
    ret['result'] = False
    ret['comment'] = message
    return ret


def read_ahead(name,
               sectors,
               devices=None):
    '''
    Ensures a block device read ahead value is set to a specific value

    name
        The name of the salt state. This can be whatever you want.

    sectors
        The number of read ahead sectors (in 512-byte sectors) to set the devices

    devices
        The list of devices that will be set. If a device listed here does
        not exist then the state will fail. If the list is empty the state
        will fail.
    '''

    ret = {'name': name,
           'changes': {},
           'result': True,
           'comment': 'Block devices {0} have read ahead set to'.format(name)}

    if not devices:
        return _error(ret, 'Parameter `devices` must be set to a single or list of block devices')

    if isinstance(devices, basestring):
        devices = [devices]

    try:
        sectors = int(sectors)
    except ValueError, e:
        return _error(ret, 'Parameter `sectors` must be an integer not {}'.format(sectors))

    # check current settings of block devices
    results = __salt__['blockdev.get']('read_ahead', *devices)

    changes = dict()
    for device_index, setting in enumerate(results):

        if 'blockdev: cannot open' in setting:
            device = setting.split()[3][:-1]
            return _error(ret, 'Parameter `devices` contains an invalid device {}'.format(device))

        try:
            setting = int(setting)
        except ValueError, e:
            return _error(ret, 'Unexpected return value from blockdev.get {}'.format(setting))

        if setting != sectors:
            device = devices[device_index]
            changes[device] = 'Changing {} read ahead from {} to {}'.format(device, setting, sectors)

    if not changes:
        return ret

    if __opts__['test']:
        ret['result'] = None
        ret['comment'] = ('The following user attributes are set to be '
                          'changed:\n')
        for key, val in changes.items():
            ret['comment'] += '{0}: {1}\n'.format(key, val)
        return ret

    results = __salt__['blockdev.set']('read_ahead', sectors, *changes.keys())

    if results:
        return _error(ret, 'Set operation failed with message {}'.format(results))

    return ret
