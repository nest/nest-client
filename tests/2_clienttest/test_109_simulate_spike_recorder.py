from random import shuffle


def test_simulate_single_spike_recorder_no_event(nest):
    sr_ids = nest.Create("spike_recorder")
    nest.Simulate(100)

    n_events = nest.GetStatus(sr_ids, "n_events")
    assert isinstance(n_events, int)
    assert n_events == 0


def test_simulate_single_spike_recorder_one_event(nest):
    spike_times = [10]
    sg_ids = nest.Create("spike_generator", params={"spike_times": spike_times})
    sr_ids = nest.Create("spike_recorder")

    nest.Connect(sg_ids, sr_ids)
    nest.Simulate(100)
    sr_status = nest.GetStatus(sr_ids)

    n_events = sr_status["n_events"]
    assert isinstance(n_events, int)
    assert n_events == len(spike_times)

    times = sr_status["events"]["times"]
    assert isinstance(times, list)
    assert len(times) == len(spike_times)
    assert times == spike_times


def test_simulate_single_spike_recorder_ranged_events(nest):
    spike_times = list(range(10, 100, 10))
    sg_ids = nest.Create("spike_generator", params={"spike_times": spike_times})
    sr_ids = nest.Create("spike_recorder")

    nest.Connect(sg_ids, sr_ids)
    nest.Simulate(100)
    sr_status = nest.GetStatus(sr_ids)

    n_events = sr_status["n_events"]
    assert isinstance(n_events, int)
    assert n_events == len(spike_times)

    times = sr_status["events"]["times"]
    assert isinstance(times, list)
    assert len(times) == len(spike_times)
    assert times == spike_times


def test_simulate_single_spike_recorder_random_events(nest):
    times = list(range(1, 100))
    shuffle(times)
    spike_times = times[:10]
    spike_times.sort()

    sg_ids = nest.Create("spike_generator", params={"spike_times": spike_times})
    sr_ids = nest.Create("spike_recorder")

    nest.Connect(sg_ids, sr_ids)
    nest.Simulate(100)
    sr_status = nest.GetStatus(sr_ids)

    n_events = sr_status["n_events"]
    assert isinstance(n_events, int)
    assert n_events == len(spike_times)

    times = sr_status["events"]["times"]
    assert isinstance(times, list)
    assert len(times) == len(spike_times)
    assert times == spike_times


def test_simulate_multiple_spike_recorders_no_events(nest):
    sr_ids = nest.Create("spike_recorder", 2)
    nest.Simulate(100)

    n_events = nest.GetStatus(sr_ids, "n_events")
    assert isinstance(n_events, list)
    assert all(n == 0 for n in n_events)


def test_simulate_multiple_spike_recorders_one_event(nest):
    spike_times = [10]
    sg_ids = nest.Create("spike_generator", 2, params={"spike_times": spike_times})
    sr_ids = nest.Create("spike_recorder", 2)

    nest.Connect(sg_ids, sr_ids, "one_to_one")
    nest.Simulate(100)
    sr_status = nest.GetStatus(sr_ids)

    n_events = sr_status["n_events"]
    assert isinstance(n_events, list)
    assert all(n == len(spike_times) for n in n_events)

    events = sr_status["events"]
    assert isinstance(events, list)
    assert all(len(event["times"]) == len(spike_times) for event in events)
    assert all(event["times"] == spike_times for event in events)


def test_simulate_multiple_spike_recorders_ranged_events(nest):
    spike_times = list(range(10, 100, 10))
    sg_ids = nest.Create("spike_generator", 2, params={"spike_times": spike_times})
    sr_ids = nest.Create("spike_recorder", 2)

    nest.Connect(sg_ids, sr_ids, "one_to_one")
    nest.Simulate(100)
    sr_status = nest.GetStatus(sr_ids)

    n_events = sr_status["n_events"]
    assert isinstance(n_events, list)
    assert all(n == len(spike_times) for n in n_events)

    events = sr_status["events"]
    assert isinstance(events, list)
    assert all(len(event["times"]) == len(spike_times) for event in events)
    assert all(event["times"] == spike_times for event in events)
