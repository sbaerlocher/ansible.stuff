#!/usr/bin/python
# (c) 2017, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible.module_utils.basic import AnsibleModule


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

try:
    import apt
    import apt.debfile
    import apt_pkg
except ImportError:
    HAS_PYTHON_APT = False

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

    cache = apt.Cache()
    cache.update()
    cache.upgrade()
    for pkg in sorted(cache.get_changes()):
        pkg_versions = pkg.versions
        if cache[pkg.name].is_installed:
            for pkg_version in pkg_versions:
                if pkg_version.is_installed:
                    pkg_new = { 
                        pkg.name : {
                            "current": pkg_version.version,
                            "available": pkg_versions[0].version
                        }
                    }
                    packages.update(pkg_new)

    result['packages'] = packages
  
    module.exit_json(**result)

if __name__ == '__main__':
    main()
