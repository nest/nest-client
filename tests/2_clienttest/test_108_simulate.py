def test_simulate(nest):
    biological_time = nest.GetKernelStatus("biological_time")
    assert isinstance(biological_time, float)
    assert biological_time == 0

    nest.Simulate(100)

    biological_time = nest.GetKernelStatus("biological_time")
    assert isinstance(biological_time, float)
    assert biological_time == 100
