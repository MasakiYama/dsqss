# DSQSS (Discrete Space Quantum Systems Solver)
# Copyright (C) 2018- The University of Tokyo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version. 
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function

import sys
from copy import deepcopy


def INFO(msg, linebreak=True, file=sys.stderr):
    print("INFO: {0}\n".format(msg), file=file)
    if linebreak:
        print("\n", file=file)


def WARN(msg, linebreak=True, file=sys.stderr):
    print("WARN: {0}\n".format(msg), file=file)
    if linebreak:
        print("\n", file=file)


def ERROR(msg, to_be_continued=False, linebreak=True, file=sys.stderr):
    print("ERROR: {0}".format(msg), file=file)
    if linebreak:
        print("\n", file=file)
    if not to_be_continued:
        sys.exit(1)


def extend_list(lst, N):
    last = lst[-1]
    for i in range(N - len(lst)):
        lst.append(deepcopy(last))
    return lst


def get_as_list(d, name, default=None, extendto=None):
    if default is None:
        v = d[name]
    else:
        v = d.get(name, default)
    if type(v) is not list:
        v = [v]
    if extendto is not None:
        extend_list(v, extendto)
    return v


def index2coord(index, size):
    D = len(size)
    i = 0
    r = [0 for d in range(D)]
    while index > 0:
        r[i] = index % size[i]
        index //= size[i]
        i += 1
    return r


def coord2index(r, size):
    index = 0
    block = 1
    for x, L in zip(r, size):
        index += block * x
        block *= L
    return index


def tagged(tagname, values):
    if not hasattr(type(values), "__iter__") or type(values) is str:
        values = [values]
    s = "<{0}>".format(tagname)
    for v in values:
        if type(v) is float:
            s += " {0:0< 18}".format(v)
        else:
            s += " {0}".format(v)
    s += " </{0}>\n".format(tagname)
    return s


def dictkey_tolower(d):
    for k,v in d.items():
        if isinstance(v, dict):
            dictkey_tolower(v)
        lk = k.lower()
        if k == lk:
            continue
        if lk in d:
            ERROR('Both "{}" and "{}" are specified.')
        d[lk] = v
        d.pop(k)

