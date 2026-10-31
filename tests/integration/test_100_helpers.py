# [[1,2],[3,4]] -> [1,2,3,4]
def flatten(values: list) -> list:
    return [item for row in values for item in row]


# [1,1,2,2]
def repeat(a: list, n: int) -> list:
    return flatten([n * [i] for i in a])


# [1,2,1,2]
def tile(a: list, n: int) -> list:
    return n * a


# Check synapse dictionary (exported from SynapseCollection)
def has_ids(
    ids: list | int,
    ref_ids: list,
) -> bool:
    if len(ref_ids) == 0:
        return False

    if isinstance(ids, int):
        return ids in ref_ids

    elif isinstance(ids, list):
        return all(id in ref_ids for id in ids)
