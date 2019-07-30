#!/usr/bin/python
# (c) 2017, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible.module_utils.basic import AnsibleModule


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

import os.path
import platform

def main():
    result = dict(
        changed=False,
        reboot=False
    )
    module = AnsibleModule(
        argument_spec=dict(),
        supports_check_mode=True
    )
   
    if platform.dist()[0] == 'Ubuntu':
        if os.path.isfile('/var/run/reboot-required'): 
            result['reboot'] = True
  
    module.exit_json(**result)

if __name__ == '__main__':
    main()
