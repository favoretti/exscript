# Copyright (C) 2007-2010 Samuel Abels.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2, as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
from Exscript.stdlib.util import secure_function

@secure_function
def new(scope):
    """
    Returns a new, empty list.

    @rtype:  string
    @return: The model of the remote device.
    """
    return []

@secure_function
def unique(scope, source):
    """
    Returns a copy of the given list in which all duplicates are removed
    such that one of each item remains in the list.

    @type  source: string
    @param source: A list of strings.
    @rtype:  string
    @return: The cleaned up list of strings.
    """
    return dict(map(lambda a: (a, 1), source)).keys()
