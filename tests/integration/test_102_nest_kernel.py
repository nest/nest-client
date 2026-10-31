def test_reset_kernel(nest):
    nest.ResetKernel()


def test_get_kernel_status(nest):
    kernel_status = nest.GetKernelStatus()
    assert isinstance(kernel_status, dict)


def test_get_kernel_resolution(nest):
    resolution = nest.GetKernelStatus("resolution")
    assert isinstance(resolution, float)
    assert resolution == 0.1


def test_get_local_num_threads(nest):
    local_num_threads = nest.GetKernelStatus("local_num_threads")
    assert isinstance(local_num_threads, int)
    assert local_num_threads == 1


def test_get_rng_seed(nest):
    rng_seed = nest.GetKernelStatus("rng_seed")
    assert isinstance(rng_seed, int)
