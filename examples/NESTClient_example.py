# -*- coding: utf-8 -*-
#
# NESTClient_example.py
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

from nest_client import NESTClient

print("Running client examples using NEST via NEST Server")

# Load NEST client
nestc = NESTClient()

#
# Use NEST Server API
#
print("\n")
print("Execute script code with NEST Server API")
print("-" * 20)

# Reset kernel
nestc.ResetKernel()

# Create nodes
pg = nestc.Create("poisson_generator", params={"rate": 6500.0})
neurons = nestc.Create("iaf_psc_alpha", 100)
sr = nestc.Create("spike_recorder")

# Connect nodes
nestc.Connect(pg, neurons, syn_spec={"weight": 10.0})
nestc.Connect(neurons[::10], sr)

# Simulate
nestc.Simulate(1000.0)

# Get events
n_events = nestc.GetStatus(sr, "n_events")[0]
print("Number of events:", n_events)


#
# Use NEST Server exec
#
print("\n")
print("Execute script code from file")
print("-" * 20)

n_events = nestc.from_file("NESTClient_script.py", "n_events")["data"]
print("Number of events:", n_events)
