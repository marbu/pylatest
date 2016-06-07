# -*- coding: utf8 -*-

"""
Pylatest test case document module.

**Pylatest document** means a description of a single test case written in rst
markup format.

This module contains information about expected structure (eg. list of section
titles) and TODO: other general functions.
"""

# Copyright (C) 2016 mbukatov@redhat.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


class PylatestDocumentError(Exception):
    pass


class PylatestActionsError(PylatestDocumentError):
    pass


class TestActions(object):
    """
    List of test actions, content of *Test Steps* section of a test case
    document.

    Action is couple of a test step and result with the same *action id*.

    Example
    -------

    Here is the rst source text of some *test action* with *action id* 42::

        .. test_step:: 42

            some step here

        .. test_result:: 42

            some result here

    And the expected structure of actions dict::

        actions_dict = {42: {'test_step': node_a, 'test_result': node_b}}

    where node_a and node_b are pending nodes of the step and resul directives.
    """

    ACTION_NAMES = ('test_step', 'test_result')
    """
    List of valid names of all pylatest actions.

    note: htmlplain div element uses just 'step' and 'result' - TODO: refactor?
    """

    # TODO: consider changing inner representation (replace action_dict with
    # something else).

    def __init__(self, enforce_id=False):
        self._actions_dict = {}
        self._enforce_id = enforce_id

    def __len__(self):
        return len(self._actions_dict)

    def __iter__(self):
        """
        Iterate over actions, yielding: *action id* and content of test step
        and test result (None is used if step or result is not specified).
        """
        for action_id, action_dict in sorted(self._actions_dict.items()):
            step = action_dict.get('test_step')
            result = action_dict.get('test_result')
            yield action_id, step, result

    def iter_content(self):
        """
        Iterate over all content.
        """
        for _, action_dict in sorted(self._actions_dict.items()):
            for name in self.ACTION_NAMES:
                content = action_dict.get(name)
                if content is None:
                    continue
                yield content

    def _get_id(self, action_name):
        if len(self._actions_dict) == 0:
            return 1
        last_id = max(self._actions_dict.keys())
        if self._actions_dict[last_id].get(action_name) is None:
            return last_id
        else:
            return last_id + 1

    def add(self, action_name, content, action_id=None):
        if action_name not in self.ACTION_NAMES:
            msg = "invalid action_name: {0}".format(action_name)
            raise PylatestActionsError(msg)
        if action_id is None:
            action_id = self._get_id(action_name)
        if self._enforce_id:
            action_dict = self._actions_dict.get(action_id)
            if action_dict is not None \
                    and action_dict.get(action_name) is not None:
                msg = "id error: such action has been already added"
                raise PylatestActionsError(msg)
        self._actions_dict.setdefault(action_id, {})[action_name] = content

    def add_step(self, content, action_id=None):
        self.add("test_step", content, action_id)

    def add_result(self, content, action_id=None):
        self.add("test_result", content, action_id)


"""
List of titles of expected sections in pylatest document (order matters).
"""
SECTIONS = (
    "Description",
    "Setup",
    "Test Steps",
    "Teardown")

"""
List of ids of expected sections in plainhtml export of pylatest document.
"""
SECTIONS_PLAINHTML = (
    "description",
    "setup",
    "teardown")

"""
Header pseudo section. It's not a real section, but a placeholder for data
which includes:

 * main headline with a name of the test case
 * pylatest metadata directives

Since this data can't be placed into a dedicated section (for obvious reasons:
it's a main headline and immediate content with metadata), this header
placeholder is not direcly included in ``SECTIONS`` tuple.
"""
HEADER = "__header__"

"""
List of titles of all sections in pylatest document (order matters),
including HEADER pseudo section.
"""
__tmp = [HEADER]
__tmp.extend(SECTIONS)
SECTIONS_ALL = tuple(__tmp)
