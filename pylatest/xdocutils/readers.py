# -*- coding: utf8 -*-

"""
Pylatest ReStructuredText Readers module.
"""

# Copyright (C) 2017 mbukatov@redhat.com
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


from docutils.readers import standalone

from pylatest.xdocutils.transforms import TestActionsTableTransform


class TestActionsTableReader(standalone.Reader):
    """
    TestActionsTableReader extends docutils standalone ReStructuredText reader
    to add transformation, everything else remains the same.
    """

    def get_transforms(self):
        transforms = standalone.Reader.get_transforms(self)
        transforms.append(TestActionsTableTransform)
        return transforms
