# -*- coding: utf8 -*-

"""
ReStructuredText directives for test steps and actions.
"""

# Copyright (C) 2015 martin.bukatovic@gmail.com
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
import os.path

from docutils import nodes
from docutils.parsers import rst

from pylatest.transforms import FooBarTransform


class Hello(rst.Directive):
    """
    Hello World rst directive (this is just minimal example).
    """

    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    has_content = False

    def run(self):
        content = "Hello World {0}!".format(self.arguments[0])
        node = nodes.paragraph(text=content)
        node_list = [node]
        return node_list


class SimpleAction(rst.Directive):
    """
    Simple action directive.
    """

    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    has_content = True

    def run(self):
        self.assert_has_content()
        # TODO: proper error handling
        action_id = int(self.arguments[0])
        # setup header node
        head_text = "There is action #{0}.".format(action_id)
        head_node = nodes.paragraph(text=head_text)
        # setup list node
        list_node = nodes.enumerated_list()
        # add items with content into list node
        for line in self.content:
            # TODO: find a better node for text content
            # text_node = nodes.Text(line) ?
            text_node = nodes.inline(text=line)
            item_node = nodes.list_item()
            item_node += text_node
            list_node += item_node
        # construct final result
        node_list = [head_node, list_node]
        return node_list


class FooBar(rst.Directive):
    """
    Create node structure using pending elements and rst transformations.
    """

    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False
    has_content = True

    def run(self):
        # first of all, parse text. content of this directive
        # into anonymous node element (can't be used directly in the tree)
        node = nodes.Element()
        self.state.nested_parse(self.content, self.content_offset, node)
        # create new pending node, which:
        #  - holds actual data (parsed content of the directive)
        #  - references transform class which is concerned with this node.
        # later when whole document is parsed, transformer uses this
        # information to execute the transformation operation
        pending = nodes.pending(FooBarTransform)
        # add content into pending node
        pending.details['nodes'] = node
        # register pending node
        # without this, transformer wouldn't know about this pending node
        self.state_machine.document.note_pending(pending)
        return [pending]
