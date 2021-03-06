#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2014, Jakub Jirutka <jakub@jirutka.cz>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

DOCUMENTATION = '''
---
module: eselect
author: Jakub Jirutka
version_added: "never"
short_description: Module for Gentoo's eselect
description:
  - Module for Gentoo's multi-purpose configuration and management tool eselect.
options:
  module:
    description:
      - Name of the eselect module to run.
    required: true
  action:
    description:
      - Action of the eselect module to run.
    default: set
  options:
    description:
      - An optional options for the eselect module (space separated).
    required: false
    aliases: [value, target]
'''

EXAMPLES = '''
  - eselect: module=editor target=/usr/bin/vim

  - eselect: module=postgresql action=reset
'''


def run_eselect(module, *args):
    cmd = 'eselect --brief --colour=no %s' % ' '.join(args)
    rc, out, err = module.run_command(cmd)
    if rc != 0:
        module.fail_json(cmd=cmd, rc=rc, stdout=out, stderr=err,
                         msg='eselect failed')
    else:
        return out


def action_set(module, emodule, target):
    current = run_eselect(module, emodule, 'show').strip()
    if target != current:
        run_eselect(module, emodule, 'set', target)
        return True
    else:
        return False


def main():
    module = AnsibleModule(
        argument_spec={
            'module':   {'required': True},
            'action':   {'default': 'set'},
            'options':  {'aliases': ['value', 'target'], 'default': ''}
        }
    )

    emodule, action, options = (module.params[key] for key in ['module', 'action', 'options'])
    changed = True
    msg = ''

    if action == 'set':
        changed = action_set(module, emodule, options)
    else:
        msg = run_eselect(module, emodule, action, options)

    module.exit_json(changed=changed, msg=msg)

# import module snippets
from ansible.module_utils.basic import *
main()
