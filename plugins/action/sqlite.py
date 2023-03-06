# Copyright 2012, Dag Wieers <dag@wieers.com>
# Copyright 2016, Toshio Kuratomi <tkuratomi@ansible.com>
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.errors import AnsibleUndefinedVariable
from ansible.module_utils.six import string_types
from ansible.module_utils._text import to_text, to_native
from ansible.plugins.action import ActionBase
import sqlite3


class ActionModule(ActionBase):
    ''' Print statements during execution '''

    TRANSFERS_FILES = False
    _VALID_ARGS = frozenset(('dbpath', 'tablename', 'os'))

    def run(self, tmp=None, task_vars=None):
        if task_vars is None:
            task_vars = dict()

        validation_result, new_module_args = self.validate_argument_spec(
            argument_spec={
                'dbpath': {'type': 'raw', 'default': 'Hello world!'},
                'tablename': {'type': 'raw'},
                'os': {'type': 'raw'},
            },
        )


        result = super(ActionModule, self).run(tmp, task_vars)
        del tmp  # tmp no longer has any effect

        db_file = new_module_args['dbpath']
        conn = sqlite3.connect(db_file)

        tb_name = new_module_args['tablename']
        os_name = new_module_args['os']

        c = conn.cursor()
        c.execute(f"SELECT password FROM {tb_name} WHERE os == '{os_name}'")
        # Add each host in table
        for row in c.fetchall():
            v11 = row[0].replace("\\n", "\n")
            result['message'] = to_native(self._loader._vault.decrypt(v11))


        return result

