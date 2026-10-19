import pytest


def test_api_create_node_then_set_param(nest):
    I_e = 376

    node_ids = nest.Create("iaf_psc_alpha")

    nest.SetStatus(node_ids, {"I_e": I_e})
    node_I_e = nest.GetStatus(node_ids, "I_e")
    assert isinstance(node_I_e, float)
    assert node_I_e == I_e


def test_api_create_multiple_nodes_then_set_params(nest):
    I_e = 376

    node_ids = nest.Create("iaf_psc_alpha", n=2)

    nest.SetStatus(node_ids, {"I_e": I_e})
    node_I_e = nest.GetStatus(node_ids, "I_e")
    assert isinstance(node_I_e, list)
    assert len(node_I_e) == 2
    assert node_I_e == [I_e, I_e]


@pytest.mark.not_mpi
def test_api_create_multiple_nodes_then_set_various_params(nest):
    """
    BUG: Testing on NEST Server MPI shows error:
    Failed to execute call: Expected datatype: Failed to cast '<param_id>' from
    std::vector<long, std::allocator<long> > to type double.
    """
    I_e = [375, 376]

    node_ids = nest.Create("iaf_psc_alpha", n=2)

    nest.SetStatus(node_ids, {"I_e": I_e})
    node_I_e = nest.GetStatus(node_ids, "I_e")
    assert isinstance(node_I_e, list)
    assert len(node_I_e) == 2
    assert node_I_e == I_e
