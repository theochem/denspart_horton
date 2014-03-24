# -*- coding: utf-8 -*-
# Horton is a development platform for electronic structure methods.
# Copyright (C) 2011-2013 Toon Verstraelen <Toon.Verstraelen@UGent.be>
#
# This file is part of Horton.
#
# Horton is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# Horton is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>
#
#--
#pylint: skip-file


import numpy as np

from horton import *


def test_mulliken_operators_water_sto3g():
    fn_fchk = context.get_fn('test/water_sto3g_hf_g03.fchk')
    data = load_smart(fn_fchk)
    operators = get_mulliken_operators(data['obasis'], data['lf'])
    for operator in operators:
        operator.check_symmetry()
    wfn = data['wfn']
    numbers = data['numbers']
    populations = np.array([operator.expectation_value(wfn.dm_full) for operator in operators])
    charges = numbers - populations
    assert charges[0] < 0 # oxygen atom
    assert abs(charges.sum()) < 1e-3
