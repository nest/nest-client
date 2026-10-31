from random import randint

from test_100_helpers import has_ids, repeat

size = randint(2, 5)


def test_selfconnect_single_node_all_to_all(nest):
    node_ids = nest.Create("iaf_psc_alpha")

    syn_dict = nest.Connect(node_ids, node_ids, "all_to_all", return_synapsecollection=True)
    assert isinstance(syn_dict, dict)
    assert isinstance(syn_dict["source"], int)
    assert isinstance(syn_dict["target"], int)
    assert has_ids(syn_dict["source"], node_ids)
    assert has_ids(syn_dict["target"], node_ids)
    assert syn_dict["source"] == syn_dict["target"] == node_ids[0]


def test_selfconnect_single_node_one_to_one(nest):
    node_ids = nest.Create("iaf_psc_alpha")

    syn_dict = nest.Connect(node_ids, node_ids, "one_to_one", return_synapsecollection=True)
    assert isinstance(syn_dict, dict)
    assert isinstance(syn_dict["source"], int)
    assert isinstance(syn_dict["target"], int)
    assert has_ids(syn_dict["source"], node_ids)
    assert has_ids(syn_dict["target"], node_ids)
    assert syn_dict["source"] == syn_dict["target"] == node_ids[0]


def test_selfconnect_all_to_all(nest):
    node_ids = nest.Create("iaf_psc_alpha", size)

    syn_dict = nest.Connect(node_ids, node_ids, "all_to_all", return_synapsecollection=True)
    assert isinstance(syn_dict, dict)
    assert isinstance(syn_dict["source"], list)
    assert isinstance(syn_dict["target"], list)
    assert len(syn_dict["source"]) == len(syn_dict["target"]) == size**2
    assert has_ids(syn_dict["source"], node_ids)
    assert has_ids(syn_dict["target"], node_ids)

    if not nest.state["has_mpi"]:
        assert syn_dict["source"] == repeat(node_ids, size)  # [1,1,2,2]
        # assert syn_dict["target"] == tile(node_ids, size)
        # NOTE: Target ids not tiled as expected, e.g. [1,2,1,2]?


def test_selfconnect_one_to_one(nest):
    node_ids = nest.Create("iaf_psc_alpha", size)

    syn_dict = nest.Connect(node_ids, node_ids, "one_to_one", return_synapsecollection=True)
    assert isinstance(syn_dict, dict)
    assert isinstance(syn_dict["source"], list)
    assert isinstance(syn_dict["target"], list)
    assert len(syn_dict["source"]) == len(syn_dict["target"]) == size
    assert has_ids(syn_dict["source"], node_ids)
    assert has_ids(syn_dict["target"], node_ids)

    if nest.state["has_mpi"]:
        assert syn_dict["source"] == syn_dict["target"]  # NOTE: random order
    else:
        assert syn_dict["source"] == syn_dict["target"] == node_ids


def test_selfconnect_fixed_one_outdegree(nest):
    node_ids = nest.Create("iaf_psc_alpha", size)

    syn_dict = nest.Connect(
        node_ids,
        node_ids,
        {"rule": "fixed_outdegree", "outdegree": 1},
        return_synapsecollection=True,
    )
    assert isinstance(syn_dict, dict)
    assert isinstance(syn_dict["source"], list)
    assert isinstance(syn_dict["target"], list)
    assert len(syn_dict["source"]) == len(syn_dict["target"]) == size
    assert has_ids(syn_dict["source"], node_ids)
    assert has_ids(syn_dict["target"], node_ids)

    if not nest.state["has_mpi"]:
        assert syn_dict["source"] == node_ids


def test_selfconnect_fixed_outdegrees(nest):
    outdegree = 2
    node_ids = nest.Create("iaf_psc_alpha", size)

    syn_dict = nest.Connect(
        node_ids,
        node_ids,
        {"rule": "fixed_outdegree", "outdegree": outdegree},
        return_synapsecollection=True,
    )
    assert isinstance(syn_dict, dict)
    assert isinstance(syn_dict["source"], list)
    assert isinstance(syn_dict["target"], list)
    assert len(syn_dict["source"]) == len(syn_dict["target"]) == size * outdegree
    assert has_ids(syn_dict["source"], node_ids)
    assert has_ids(syn_dict["target"], node_ids)

    if not nest.state["has_mpi"]:
        assert syn_dict["source"] == repeat(node_ids, outdegree)  # fixed


def test_selfconnect_fixed_one_indegree(nest):
    node_ids = nest.Create("iaf_psc_alpha", size)

    syn_dict = nest.Connect(
        node_ids,
        node_ids,
        {"rule": "fixed_indegree", "indegree": 1},
        return_synapsecollection=True,
    )
    assert isinstance(syn_dict, dict)
    assert isinstance(syn_dict["source"], list)
    assert isinstance(syn_dict["target"], list)
    assert len(syn_dict["source"]) == len(syn_dict["target"]) == size
    assert has_ids(syn_dict["source"], node_ids)
    assert has_ids(syn_dict["target"], node_ids)


def test_selfconnect_fixed_indegrees(nest):
    indegree = 2
    node_ids = nest.Create("iaf_psc_alpha", size)

    syn_dict = nest.Connect(
        node_ids,
        node_ids,
        {"rule": "fixed_indegree", "indegree": indegree},
        return_synapsecollection=True,
    )
    assert isinstance(syn_dict, dict)
    assert isinstance(syn_dict["source"], list)
    assert isinstance(syn_dict["target"], list)
    assert len(syn_dict["source"]) == len(syn_dict["target"]) == size * indegree
    assert has_ids(syn_dict["source"], node_ids)
    assert has_ids(syn_dict["target"], node_ids)
    # assert syn_dict["target"] == repeat(node_ids, indegree)  # fixed
    # NOTE: Target ids are not repeated as expected,
    #       e.g. [2, 2, 3, 1, 1, 3] == [1, 1, 2, 2, 3, 3]


def test_selfconnect_fixed_total_number(nest):
    node_ids = nest.Create("iaf_psc_alpha", size)

    syn_dict = nest.Connect(
        node_ids,
        node_ids,
        {"rule": "fixed_total_number", "N": 1},
        return_synapsecollection=True,
    )
    assert isinstance(syn_dict, dict)
    assert isinstance(syn_dict["source"], int)
    assert isinstance(syn_dict["target"], int)
    assert has_ids(syn_dict["source"], node_ids)
    assert has_ids(syn_dict["target"], node_ids)


def test_selfconnect_fixed_total_numbers(nest):
    N = randint(2, size)
    node_ids = nest.Create("iaf_psc_alpha", size)

    syn_dict = nest.Connect(
        node_ids,
        node_ids,
        {"rule": "fixed_total_number", "N": N},
        return_synapsecollection=True,
    )
    assert isinstance(syn_dict, dict)
    assert isinstance(syn_dict["source"], list)
    assert isinstance(syn_dict["target"], list)
    assert len(syn_dict["source"]) == len(syn_dict["target"]) == N
    assert has_ids(syn_dict["source"], node_ids)
    assert has_ids(syn_dict["target"], node_ids)


def test_selfconnect_pairwise_bernoulli(nest):
    node_ids = nest.Create("iaf_psc_alpha", size)

    syn_dict = nest.Connect(
        node_ids,
        node_ids,
        {"rule": "pairwise_bernoulli", "p": 0.5},
        return_synapsecollection=True,
    )
    assert isinstance(syn_dict, dict)
    if "source" in syn_dict:
        assert isinstance(syn_dict["source"], list)


def test_selfconnect_pairwise_bernoulli_no_autoapses_no_multapses(nest):
    node_ids = nest.Create("iaf_psc_alpha", size)

    syn_dict = nest.Connect(
        node_ids,
        node_ids,
        {
            "rule": "pairwise_bernoulli",
            "p": 0.5,
            "allow_autapses": False,
            "allow_multapses": False,
        },
        return_synapsecollection=True,
    )
    assert isinstance(syn_dict, dict)
    if syn_dict:
        assert isinstance(syn_dict["source"], (int, list))
        assert isinstance(syn_dict["target"], (int, list))


def test_selfconnect_symmetric_pairwise_bernoulli(nest):
    node_ids = nest.Create("iaf_psc_alpha", size)

    syn_dict = nest.Connect(
        node_ids,
        node_ids,
        {
            "rule": "symmetric_pairwise_bernoulli",
            "p": 0.5,
            "allow_autapses": False,
            "make_symmetric": True,
        },
        return_synapsecollection=True,
    )
    assert isinstance(syn_dict, dict)
    if syn_dict:
        assert isinstance(syn_dict["source"], (int, list))
        assert isinstance(syn_dict["target"], (int, list))


def test_selfconnect_pairwise_poisson(nest):
    node_ids = nest.Create("iaf_psc_alpha", size)

    syn_dict = nest.Connect(
        node_ids,
        node_ids,
        {"rule": "pairwise_poisson", "pairwise_avg_num_conns": 0.5},
        return_synapsecollection=True,
    )
    assert isinstance(syn_dict, dict)
    if syn_dict:
        assert isinstance(syn_dict["source"], (int, list))
        assert isinstance(syn_dict["target"], (int, list))
