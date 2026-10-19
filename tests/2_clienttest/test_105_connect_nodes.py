from random import randint

from test_100_helpers import has_ids, repeat

size = randint(2, 5)


def test_selfconnect_node(nest):
    node_ids = nest.Create("iaf_psc_alpha")

    syn_dict = nest.Connect(node_ids, node_ids, return_synapsecollection=True)
    assert isinstance(syn_dict, dict)
    assert isinstance(syn_dict["source"], int)
    assert isinstance(syn_dict["target"], int)
    assert has_ids(syn_dict["source"], node_ids)
    assert has_ids(syn_dict["target"], node_ids)
    assert syn_dict["source"] == syn_dict["target"] == node_ids[0]


def test_selfconnect_nodes(nest):
    node_ids = nest.Create("iaf_psc_alpha", n=size)

    syn_dict = nest.Connect(node_ids, node_ids, return_synapsecollection=True)
    assert isinstance(syn_dict, dict)
    assert isinstance(syn_dict["source"], list)
    assert isinstance(syn_dict["target"], list)
    assert len(syn_dict["source"]) == len(syn_dict["target"]) == size**2
    assert has_ids(syn_dict["source"], node_ids)
    assert has_ids(syn_dict["target"], node_ids)

    if not nest.state["has_mpi"]:
        assert syn_dict["source"] == repeat(node_ids, size)
        # assert syn_dict["target"] == tile(node_ids, size)
        # NOTE: Target ids are not tiled as expected,
        #       e.g. [3, 4, 2, 1, 3, 2, ...] == [1, 2, 3, 4, 1, 2, ...]


def test_connect_multiple_nodes(nest):
    node_ids = nest.Create("iaf_psc_alpha", n=2)

    syn_dict = nest.Connect([node_ids[0]], [node_ids[1]], return_synapsecollection=True)
    assert isinstance(syn_dict, dict)
    assert isinstance(syn_dict["source"], int)
    assert isinstance(syn_dict["target"], int)
    assert has_ids(syn_dict["source"], node_ids)
    assert has_ids(syn_dict["target"], node_ids)
    assert syn_dict["source"] == node_ids[0]
    assert syn_dict["target"] == node_ids[1]


def test_connect_distinct_source_target(nest):
    source_ids = nest.Create("iaf_psc_alpha")
    target_ids = nest.Create("iaf_psc_alpha")

    syn_dict = nest.Connect(source_ids, target_ids, return_synapsecollection=True)
    assert isinstance(syn_dict, dict)
    assert isinstance(syn_dict["source"], int)
    assert isinstance(syn_dict["target"], int)
    assert has_ids(syn_dict["source"], source_ids)
    assert has_ids(syn_dict["target"], target_ids)
    assert syn_dict["source"] == source_ids[0]
    assert syn_dict["target"] == target_ids[0]


def test_connect_distinct_multiple_nodes(nest):
    source_size = randint(2, 5)
    target_size = randint(2, 5)

    source_ids = nest.Create("iaf_psc_alpha", source_size)
    target_ids = nest.Create("iaf_psc_alpha", target_size)

    syn_dict = nest.Connect(source_ids, target_ids, return_synapsecollection=True)
    assert isinstance(syn_dict, dict)
    assert isinstance(syn_dict["source"], list)
    assert isinstance(syn_dict["target"], list)
    assert len(syn_dict["source"]) == len(syn_dict["target"]) == source_size * target_size
    assert has_ids(syn_dict["source"], source_ids)
    assert has_ids(syn_dict["target"], target_ids)

    if not nest.state["has_mpi"]:
        assert syn_dict["source"] == repeat(source_ids, target_size)
        # assert syn_dict["target"] == tile(target_ids, source_size)
        # NOTE: Target ids are not tiled as expected,
        #       e.g. [9, 6, 8, 7, 5, 6, ...] == [5, 6, 7, 8, 9, 5, ...]
