#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""@pylatest
Hello World Test Case
*********************

.. test_metadata:: author foo@example.com
.. test_metadata:: date 2015-11-06
.. test_metadata:: comment This is here just to test metadata processing.

Setup
=====

#. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec a diam
   lectus. Sed sit amet ipsum mauris.

#. Use lvm disk paritioning and Leave 10G free space in volume
   called ``lv_helloword``.

#. When the system is installed, format ``lv_helloword`` volume with
   brtfs using ``--super --special --options``.

#. Mount it on a client::

    # mount -t btrfs /dev/mapper/vg_fedora/lv_helloword /mnt/helloworld

#. Ceterum censeo, lorem ipsum::

    # dnf install foobar
    # systemctl enable foobard

Test Steps
==========

.. test_step:: 1

    List files in the volume: ``ls -a /mnt/helloworld``

.. test_result:: 1

    There are no files, output should be empty.

.. test_step:: 2

    Donec et mollis dolor::

        $ foo --extra sth
        $ bar -vvv

.. test_result:: 2

    Maecenas congue ligula ac quam viverra nec
    consectetur ante hendrerit.

.. test_step:: 3

    This one has no matching test result.

.. test_result:: 4

    And this result has no test step.

Teardown
========

#. Lorem ipsum dolor sit amet: ``rm -rf /mnt/helloworld``.

#. Umount and remove ``lv_helloword`` volume.

#. The end.
"""


import sys


def main():
    print("done")

if __name__ == '__main__':
    sys.exit(main())
