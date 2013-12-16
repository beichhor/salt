# -*- coding: utf-8 -*-

"""
Module for managing ext2/3/4 file systems
===================================

Ensure devices has a specified file system
"""

import os
import logging
from salt import exceptions, utils

log = logging.getLogger(__name__)

log = logging.getLogger(__name__)
log.debug("module extfs loaded")


def __virtual__():
    '''
    Only work on POSIX-like systems
    '''
    if utils.is_windows():
        return False
    return 'extfs'


def _error(ret, message):
    ret['result'] = False
    ret['comment'] = message
    return ret


def exists(name,
           fs_type='ext4',
           **kwargs):
    '''
    Ensures a file system exists on the specified device

    Valid options are::

        fs_type: set the filesystem type, one of ext2, ext3 or ext4 (DEFAULT)
        block_size: 1024, 2048 or 4096
        check: check for bad blocks
        direct: use direct IO
        ext_opts: extended file system options (comma-separated)
        fragment_size: size of fragments
        force: setting force to True will cause mke2fs to specify the -F option
               twice (it is already set once); this is truly dangerous
        blocks_per_group: number of blocks in a block group
        number_of_groups: ext4 option for a virtual block group
        bytes_per_inode: set the bytes/inode ratio
        inode_size: size of the inode
        journal: set to True to create a journal (default on ext3/4)
        journal_opts: options for the fs journal (comma separated)
        blocks_file: read bad blocks from file
        label: label to apply to the file system
        reserved: percentage of blocks reserved for super-user
        last_dir: last mounted directory
        test: set to True to not actually create the file system (mke2fs -n)
        number_of_inodes: override default number of inodes
        creator_os: override "creator operating system" field
        opts: mount options (comma separated)
        revision: set the filesystem revision (default 1)
        super: write superblock and group descriptors only
        usage_type: how the filesystem is going to be used
        uuid: set the UUID for the file system
    '''

    ret = {'name': name,
           'changes': {},
           'result': True,
           'comment': 'Block devices {0} have read ahead set to'.format(name)}

    if fs_type not in ['ext2', 'ext3', 'ext4']:
        return _error(ret, 'Parameter `fs_type` must be set to ext2, ext3 or ext4')

    cmd = 'e2fsck -n {1}'.format(name)
    ret = __salt__['cmd.run_all'](cmd)

    # file system exists
    if ret['retcode'] < 8:
        return ret

    if __opts__['test']:
        ret['result'] = None
        ret['comment'] = ('File system was not found and would have been created')
        return ret

    # check current settings of block devices
    results = __salt__['extfs.mkfs'](name, fs_type=fs_type, **kwargs)

    if not results:
        return _error(ret, 'Failed to create file system')

    return ret
