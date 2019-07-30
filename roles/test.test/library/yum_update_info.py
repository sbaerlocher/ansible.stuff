#!/usr/bin/python
# (c) 2017, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible.module_utils.basic import AnsibleModule


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

import os
import sys
import yum

yb = yum.YumBase()

def main():
    result = dict(
        changed=False,
        packages=dict()
    )
    module = AnsibleModule(
        argument_spec=dict(),
        supports_check_mode=True
    )
   
    packages = dict()

    package_install = yb.doPackageLists()
    package_update = yb.doPackageLists(pkgnarrow='updates')

    if package_update.updates:
        for pkg in sorted(package_update.updates):
            for pkg1 in sorted(package_install.installed):
                if pkg.name == pkg1.name:
                    pkg_new = { 
                        pkg.name : {
                            "current":  pkg.version + "-" + pkg.release,
                            "available": pkg1.version + "-" + pkg1.release
                        }
                    }
                    packages.update(pkg_new)

    result['packages'] = packages
  
    module.exit_json(**result)

if __name__ == '__main__':
    main()
