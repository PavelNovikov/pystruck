from lib import Tree, AVLTree
import random
from collections import defaultdict


def test_random_ordering(events, verbose=False):
    keys = set()
    t = AVLTree()
    for i in range(len(events)):
        event_type, key = events[i]
        t.check_consistency()
        t.check_balance_invariant()
        if event_type == "del":
            del t[key]

            keys.remove(key)
            if verbose:
                print("del ", str(key))
        else:
            keys.add(key)
            t.insert(key, None)
            if verbose:
                print("insert ", str(key))
        t.check_consistency()
        t.check_balance_invariant()
        if verbose:
            t.output()

    if verbose:
        print(t.get_ordering())
        print(sorted(list(keys)))

    assert sorted(list(keys)) == t.get_ordering()


def generate_events(n_events, deletion_probability):
    result = []
    keys = []
    generated = set()
    for i in range(n_events):
        if random.random() < deletion_probability and len(keys) > 0:
            index = random.randint(0, len(keys) - 1)
            key = keys[index]
            result.append(("del", key))
            del keys[index]
            generated.remove(key)
        else:
            new_key = random.randint(0, 10 * n_events)
            while new_key in generated:
                new_key = random.randint(0, 10 * n_events)
            keys.append(new_key)
            generated.add(new_key)
            result.append(("insert", new_key))
    return result


for i in range(1000000):
    print(i)
    events = generate_events(10, 0.3)
    try:
        test_random_ordering(events)
    except Exception as e:
        print(events)
        test_random_ordering(events, verbose=True)


