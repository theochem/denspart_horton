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


import numpy as np

from horton import *
from horton.part.test.common import check_names, check_proatom_splines, \
    get_proatomdb_hf_sto3g, get_proatomdb_hf_lan


def check_water_hf_sto3g(scheme, expecting, needs_padb=True, **kwargs):
    if needs_padb:
        proatomdb = get_proatomdb_hf_sto3g()
        kwargs['proatomdb'] = proatomdb

    # Get the molecule
    fn_fchk = context.get_fn('test/water_sto3g_hf_g03.fchk')
    sys = System.from_file(fn_fchk)
    sys.wfn.update_dm('alpha')

    # Create a grid for the partitioning
    rtf = ExpRTransform(5e-4, 2e1, 120)
    rgrid = RadialGrid(rtf)

    # Do the partitioning
    grid = BeckeMolGrid(sys, (rgrid, 110), random_rotate=False, keep_subgrids=kwargs.get('greedy', True))
    WPartClass = wpart_schemes[scheme]
    wpart = WPartClass(sys, grid,  **kwargs)
    names = wpart.do_all()
    check_names(names, wpart)
    assert abs(wpart['charges'] - expecting).max() < 2e-3
    assert abs(wpart['charges'] - wpart['cartesian_multipoles'][:,0]).max() < 1e-3
    assert abs(wpart['charges'] - wpart['pure_multipoles'][:,0]).max() < 1e-3

    if kwargs.get('greedy', False):
        check_proatom_splines(wpart)


def test_hirshfeld_water_hf_sto3g_local():
    expecting = np.array([-0.246171541212, 0.123092011074, 0.123079530138]) # from HiPart
    check_water_hf_sto3g('h', expecting, local=True)


def test_hirshfeld_water_hf_sto3g_global():
    expecting = np.array([-0.246171541212, 0.123092011074, 0.123079530138]) # from HiPart
    check_water_hf_sto3g('h', expecting, local=False)


def test_hirshfeld_i_water_hf_sto3g_local():
    expecting = np.array([-0.4214, 0.2107, 0.2107]) # From HiPart
    check_water_hf_sto3g('hi', expecting, local=True)


def test_hirshfeld_i_water_hf_sto3g_global():
    expecting = np.array([-0.4214, 0.2107, 0.2107]) # From HiPart
    check_water_hf_sto3g('hi', expecting, local=False)


def test_hirshfeld_i_water_hf_sto3g_local_greedy():
    expecting = np.array([-0.4214, 0.2107, 0.2107]) # From HiPart
    check_water_hf_sto3g('hi', expecting, local=True, greedy=True)


def test_hirshfeld_i_water_hf_sto3g_global_greedy():
    expecting = np.array([-0.4214, 0.2107, 0.2107]) # From HiPart
    check_water_hf_sto3g('hi', expecting, local=False, greedy=True)


def test_hirshfeld_e_water_hf_sto3g_local():
    expecting = np.array([-0.422794483125, 0.211390419810, 0.211404063315]) # From HiPart
    check_water_hf_sto3g('he', expecting, local=True)


def test_hirshfeld_e_water_hf_sto3g_global():
    expecting = np.array([-0.422794483125, 0.211390419810, 0.211404063315]) # From HiPart
    check_water_hf_sto3g('he', expecting, local=False)


def test_hirshfeld_e_water_hf_sto3g_local_greedy():
    expecting = np.array([-0.422794483125, 0.211390419810, 0.211404063315]) # From HiPart
    check_water_hf_sto3g('he', expecting, local=True, greedy=True)


def test_hirshfeld_e_water_hf_sto3g_global_greedy():
    expecting = np.array([-0.422794483125, 0.211390419810, 0.211404063315]) # From HiPart
    check_water_hf_sto3g('he', expecting, local=False, greedy=True)


def test_is_water_hf_sto3g():
    expecting = np.array([-0.490017586929, 0.245018706885, 0.244998880045]) # From HiPart
    check_water_hf_sto3g('is', expecting, needs_padb=False)


def check_msa_hf_lan(scheme, expecting, needs_padb=True, **kwargs):
    if needs_padb:
        proatomdb = get_proatomdb_hf_lan()
        kwargs['proatomdb'] = proatomdb

    # Get the molecule
    fn_fchk = context.get_fn('test/monosilicic_acid_hf_lan.fchk')
    sys = System.from_file(fn_fchk)

    # Create a grid for the partitioning
    rtf = ExpRTransform(5e-4, 2e1, 120)
    rgrid = RadialGrid(rtf)

    # Do the partitioning, both with local and global grids
    grid = BeckeMolGrid(sys, (rgrid, 110), random_rotate=False, keep_subgrids=kwargs.get('greedy', True))
    WPartClass = wpart_schemes[scheme]
    wpart = WPartClass(sys, grid, **kwargs)
    wpart.do_charges()
    assert abs(wpart['charges'] - expecting).max() < 3e-3

    if kwargs.get('greedy', False):
        check_proatom_splines(wpart)


def test_hirshfeld_msa_hf_lan_local():
    expecting = np.array([0.56175431, -0.30002709, -0.28602105, -0.28335086, -0.26832878,  0.13681904,  0.14535691,  0.14206876,  0.15097682])
    check_msa_hf_lan('h', expecting, local=True)


def test_hirshfeld_msa_hf_lan_global():
    expecting = np.array([0.56175431, -0.30002709, -0.28602105, -0.28335086, -0.26832878,  0.13681904,  0.14535691,  0.14206876,  0.15097682])
    check_msa_hf_lan('h', expecting, local=False)


def test_hirshfeld_i_msa_hf_lan_local():
    expecting = np.array([1.14305602, -0.52958298, -0.51787452, -0.51302759, -0.50033981, 0.21958586, 0.23189187, 0.22657354, 0.23938904])
    check_msa_hf_lan('hi', expecting, local=True)


def test_hirshfeld_i_msa_hf_lan_global():
    expecting = np.array([1.14305602, -0.52958298, -0.51787452, -0.51302759, -0.50033981, 0.21958586, 0.23189187, 0.22657354, 0.23938904])
    check_msa_hf_lan('hi', expecting, local=False)


def test_hirshfeld_i_msa_hf_lan_local_greedy():
    expecting = np.array([1.14305602, -0.52958298, -0.51787452, -0.51302759, -0.50033981, 0.21958586, 0.23189187, 0.22657354, 0.23938904])
    check_msa_hf_lan('hi', expecting, local=True, greedy=True)


def test_hirshfeld_i_msa_hf_lan_global_greedy():
    expecting = np.array([1.14305602, -0.52958298, -0.51787452, -0.51302759, -0.50033981, 0.21958586, 0.23189187, 0.22657354, 0.23938904])
    check_msa_hf_lan('hi', expecting, local=False, greedy=True)


def test_hirshfeld_e_msa_hf_lan_local():
    expecting = np.array([1.06135407, -0.51795437, -0.50626239, -0.50136175, -0.48867641, 0.22835963, 0.240736, 0.23528162, 0.24816043])
    check_msa_hf_lan('he', expecting, local=True)


def test_hirshfeld_e_msa_hf_lan_global():
    expecting = np.array([1.06135407, -0.51795437, -0.50626239, -0.50136175, -0.48867641, 0.22835963, 0.240736, 0.23528162, 0.24816043])
    check_msa_hf_lan('he', expecting, local=False)


def test_hirshfeld_e_msa_hf_lan_local_greedy():
    expecting = np.array([1.06135407, -0.51795437, -0.50626239, -0.50136175, -0.48867641, 0.22835963, 0.240736, 0.23528162, 0.24816043])
    check_msa_hf_lan('he', expecting, local=True, greedy=True)


def test_hirshfeld_e_msa_hf_lan_global_greedy():
    expecting = np.array([1.06135407, -0.51795437, -0.50626239, -0.50136175, -0.48867641, 0.22835963, 0.240736, 0.23528162, 0.24816043])
    check_msa_hf_lan('he', expecting, local=False, greedy=True)


def test_is_msa_hf_lan():
    expecting = np.array([1.1721364, -0.5799622, -0.5654549, -0.5599638, -0.5444145, 0.2606699, 0.2721848, 0.2664377, 0.2783666]) # from HiPart
    check_msa_hf_lan('is', expecting, needs_padb=False)
