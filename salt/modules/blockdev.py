# -*- coding: utf-8 -*-

"""
blockdev - call block device ioctls from the command line
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


def _cmd_run_all(command, devices):
    ret = __salt__['cmd.run_all'](
        'blockdev --{command} {devices}'.format(command, ' '.join(devices))
    )
    if ret['retcode'] == 0:
        return ret['stdout'].splitlines()
    else:
        return False


def get(command, *devices):
    '''
    Gets the the value or status of selected block devices

    CLI Example:

    .. code-block:: bash

        salt '*' blockdev.get min_io_size /dev/md0
        salt '*' blockdev.get read_ahead /dev/xvdf1 /dev/xvdf2

    Valid options are::

        block_size: Print blocksize in bytes.
        discard_zeroes: Get discard zeroes support status.
        filesystem_read_ahead: Get filesystem readahead in 512-byte sectors.
        min_io_size: Get minimum I/O size.
        opt_io_size: Get optimal I/O size.
        max_sectors: Get max sectors per request
        physical_block_size: Get physical block (sector) size.
        read_ahread: Print readahead (in 512-byte sectors).
        read_only: Get read-only. Print 1 if the device is read-only, 0 otherwise.
        size_bytes: Print device size in bytes.
        size:  Print sectorsize in bytes - usually 512.
        sector_size: Get size in 512-byte sectors.


    See the get commands in the ``blockdev(8)`` manpage.
    '''

    options_map = {
        'align_off': 'alignoff',
        'block_size': 'bsz',
        'discard_zeroes': 'discardzeroes',
        'filesystem_read_ahead': 'fra',
        'min_io_size': 'iomin',
        'opt_io_size': 'ioopt',
        'max_sectors': 'maxsect',
        'physical_block_size': 'pbsz',
        'read_ahead': 'ra',
        'read_only': 'ro',
        'size_bytes': 'size64',
        'size': 'sz',
        'sector_size': 'ss',
    }
    if command in options_map:
        command = options_map[command]
    command = 'get{}'.format(command)
    return _cmd_run_all(command, devices)


def set(command, value, *devices):
    '''
    Sets a value or run command on selected block devices

    CLI Example:

    .. code-block:: bash

        salt '*' blockdev.set read_only /dev/xvdb
        salt '*' blockdev.set read_ahead 32 /dev/xvdf1 /dev/xvdf2

    Valid options are::

        block_size: Set blocksize.
        filesystem_read_ahead: Set filesystem readahead (same like --setra on 2.6 kernels).
        read_ahread: Set readahead (in 512-byte sectors).
        read_only: Set read-only.
        read_write: Set read-write.

    See the set commands in the ``blockdev(8)`` manpage.
    '''
    options_map = {
        'block_size': 'bsz',
        'filesystem_read_ahead': 'fra',
        'read_ahead': 'ra',
        'read_only': 'ro',
        'read_write': 'rw',
    }
    if command in options_map:
        command = options_map[command]
    # value may be a value or a device here but it doesn't make a difference
    command = 'set{} {}'.format(command, value)
    return _cmd_run_all(command, devices)


def flush_buffers(*devices):
    '''
    Flush buffers of selected devices

    CLI Example:

    .. code-block:: bash

        salt '*' blockdev.flush_buffers /dev/xvdb
        salt '*' blockdev.flush_buffers /dev/xvdf1 /dev/xvdf2

    See the --flushbufs command in the ``blockdev(8)`` manpage.
    '''
    return _cmd_run_all('flushbufs', devices)


def flush_buffers(*devices):
    '''
    Flush buffers of selected devices

    CLI Example:

    .. code-block:: bash

        salt '*' blockdev.flush_buffers /dev/xvdb
        salt '*' blockdev.flush_buffers /dev/xvdf1 /dev/xvdf2

    See the --flushbufs command in the ``blockdev(8)`` manpage.
    '''
    return _cmd_run_all('rereadpt', devices)
