# -*- coding: utf-8 -*-
#
# simple_network.py
#
# This file is part of NEST.
#
# Copyright (C) 2004 The NEST Initiative
#
# NEST is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# NEST is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with NEST.  If not, see <http://www.gnu.org/licenses/>.


# Reset kernel
nest.ResetKernel()

# Create nodes
pg = nest.Create("poisson_generator", params={"rate": 6500.})
neurons = nest.Create("iaf_psc_alpha", 100)
sd = nest.Create("spike_detector")

# Connect nodes
nest.Connect(pg, neurons, syn_spec={"weight": 10.})
nest.Connect(neurons, sd)

# Simulate
nest.Simulate(1000.0)

# Get events
n_events = sd.get("n_events")
