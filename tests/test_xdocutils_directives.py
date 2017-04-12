# -*- coding: utf8 -*-

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


import sys
import textwrap

import docutils.frontend
import docutils.parsers.rst
import docutils.utils
import pytest

import pylatest.xdocutils.directives
import pylatest.xdocutils.core


def _parse(rst_str):
    """
    Parse given string with rst parser, returns pformat string result.
    """
    # setup, see `docutils.utils.new_document()` or `docutils.parsers.rst`
    # docstrings for details
    rst_parser = docutils.parsers.rst.Parser()
    opt_parser = docutils.frontend.OptionParser(
        components=(docutils.parsers.rst.Parser,))
    settings = opt_parser.get_default_values()
    # setup: disable docutils error messages
    settings.report_level = 5
    settings.halt_level = 5
    document = docutils.utils.new_document('_testparse() method', settings)
    # parsing
    rst_parser.parse(rst_str, document)
    return document.pformat()


def _test_directive(rst_input, exp_result):
    result = _parse(rst_input)
    assert result == exp_result


@pytest.fixture
def register_all_plain(scope="module"):
    """
    Register pylatest docutils extensions (nodes, directives ... but no
    transforms).
    """
    pylatest.xdocutils.core.register_all(use_plain=True)


def test_docutils_works_fine_empty(register_all_plain):
    rst_input = ""
    exp_result = '<document source="_testparse() method">\n'
    _test_directive(rst_input, exp_result)


def test_docutils_works_fine_somedirective(register_all_plain):
    rst_input = textwrap.dedent('''\
    .. container::

        Lorem ipsum.
    ''')
    exp_result = textwrap.dedent('''\
    <document source="_testparse() method">
        <container>
            <paragraph>
                Lorem ipsum.
    ''')
    _test_directive(rst_input, exp_result)


@pytest.mark.parametrize("action_id", [1, 23, 129])
@pytest.mark.parametrize("action_name", ["test_step", "test_result"])
def test_oldtestaction_empty(register_all_plain, action_id, action_name):
    rst_input = '.. {}:: {}'.format(action_name, action_id)
    exp_result = textwrap.dedent('''\
    <document source="_testparse() method">
        <test_action_node action_id="{}" action_name="{}">
    '''.format(action_id, action_name))
    _test_directive(rst_input, exp_result)


@pytest.mark.parametrize("action_name", ["test_step", "test_result"])
def test_oldtestaction_empty_noid(register_all_plain, action_name):
    rst_input = '.. {}::'.format(action_name)
    exp_result = textwrap.dedent('''\
    <document source="_testparse() method">
        <system_message level="3" line="1" source="_testparse() method" type="ERROR">
            <paragraph>
                Error in "{0}" directive:
                1 argument(s) required, 0 supplied.
            <literal_block xml:space="preserve">
                .. {0}::
    '''.format(action_name))
    _test_directive(rst_input, exp_result)


@pytest.mark.xfail(reason="https://gitlab.com/mbukatov/pylatest/issues/10")
@pytest.mark.parametrize("action_id", ["foo", None])
@pytest.mark.parametrize("action_name", ["test_step", "test_result"])
def test_oldtestaction_empty_wrongid(register_all_plain, action_id, action_name):
    rst_input = '.. {}:: {}'.format(action_name, action_id)
    exp_result = textwrap.dedent('''\
    <document source="_testparse() method">
        <test_action_node action_id="{}" action_name="{}">
    '''.format(action_id, action_name))
    _test_directive(rst_input, exp_result)


@pytest.mark.parametrize("action_name", ["test_step", "test_result"])
def test_oldtestaction_simple(register_all_plain, action_name):
    rst_input = textwrap.dedent('''\
    .. {}:: 7

        Some content.
    '''.format(action_name))
    exp_result = textwrap.dedent('''\
    <document source="_testparse() method">
        <test_action_node action_id="7" action_name="{}">
            <paragraph>
                Some content.
    '''.format(action_name))
    _test_directive(rst_input, exp_result)


@pytest.mark.parametrize("action_name", ["test_step", "test_result"])
def test_oldtestaction_paragraph(register_all_plain, action_name):
    rst_input = textwrap.dedent('''\
    .. {}:: 7

        Some content.

        Donec et mollis dolor::

            $ foo --extra sth
            $ bar -vvv
    '''.format(action_name))
    exp_result = textwrap.dedent('''\
    <document source="_testparse() method">
        <test_action_node action_id="7" action_name="{}">
            <paragraph>
                Some content.
            <paragraph>
                Donec et mollis dolor:
            <literal_block xml:space="preserve">
                $ foo --extra sth
                $ bar -vvv
    '''.format(action_name))
    _test_directive(rst_input, exp_result)


@pytest.mark.parametrize("req_id", ["SOME_ID", 111])
def test_testmetadata_full_nooptions(register_all_plain, req_id):
    rst_input = textwrap.dedent('''\
    .. requirement:: {}

        Some content.
    '''.format(req_id))
    exp_result = textwrap.dedent('''\
    <document source="_testparse() method">
        <requirement_node req_id="{}">
            <paragraph>
                Some content.
    '''.format(req_id))
    _test_directive(rst_input, exp_result)


def test_testmetadata_full_alloptions(register_all_plain):
    rst_input = textwrap.dedent('''\
    .. requirement:: FOO123
        :priority: high

        Natus illum repudiandae consequatur.

        Expedita saepe architecto numquam accusamus.
    ''')
    exp_result = textwrap.dedent('''\
    <document source="_testparse() method">
        <requirement_node priority="high" req_id="FOO123">
            <paragraph>
                Natus illum repudiandae consequatur.
            <paragraph>
                Expedita saepe architecto numquam accusamus.
    ''')
    _test_directive(rst_input, exp_result)
