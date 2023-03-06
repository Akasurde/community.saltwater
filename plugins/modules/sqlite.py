#!/usr/bin/python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: my_test

short_description: This is my test module

version_added: "2.4"

description: This is my longer description explaining my test module.

options:
    name:
        description:
            - This is the message to send to the test module.
        required: true
        type: str
    new:
        description:
            - Control to demo if the result of this module is changed or not.
        required: false
        type: bool

author:
    - Your Name (@yourhandle)
'''

EXAMPLES = r'''# '''

RETURN = r'''#
'''

from ansible.module_utils.basic import AnsibleModule
import sqlite3
from ansible.module_utils._text import to_bytes, to_text, to_native


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        dbpath=dict(type='str', required=True),
        tablename=dict(type='str', required=True),
        os=dict(type='str', required=True),
    )

    result = dict(
        changed=False,
        message=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)


    db_file = module.params.get('dbpath')
    conn = sqlite3.connect(db_file)

    tb_name = module.params.get('tablename')
    os_name = module.params.get('os')

    c = conn.cursor()
    c.execute(f"SELECT password FROM {tb_name} WHERE os == '{os_name}'")
    # Add each host in table
    for row in c.fetchall():
        secret_var = row[0].replace("\\n", "\n")
        #secret_var = row[0]
        result['message'] = "!vault | %s" % secret_var
        break
    
    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()

