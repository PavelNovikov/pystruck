from lib import Tree, AVLTree
import random
from collections import defaultdict


def test_random_ordering(events, verbose=False):
    keys = defaultdict(lambda : 0)
    t = AVLTree()
    for i in range(len(events)):
        event_type, key = events[i]
        t.check_consistency()
        if event_type == "del":
            del t[key]

            keys[key] -= 1
            if verbose:
                print("del ", str(key))
        else:
            keys[key] += 1
            t.insert(key, None)
            if verbose:
                print("insert ", str(key))
        t.check_consistency()
        if verbose:
            t.output()

    reference_sorting = [x for key, count in keys.items() for x in [key] * count]
    # if verbose:
    #     print(t.get_ordering())
    #     print(reference_sorting)

    assert sorted(reference_sorting) == t.get_ordering()


def generate_events(n_events, deletion_probability):
    result = []
    keys = []
    for i in range(n_events):
        if random.random() < deletion_probability and len(keys) > 0:
            index = random.randint(0, len(keys) - 1)
            key = keys[index]
            result.append(("del", key))
            del keys[index]
        else:
            new_key = random.randint(0, 1000)
            keys.append(new_key)
            result.append(("insert", new_key))
    return result


for i in range(100000):
    print(i)
    events = generate_events(100, 0.3)
    try:
        test_random_ordering(events)
    except Exception as e:
        print(events)
        test_random_ordering(events, verbose=True)


# t = AVLTree()
# t.insert(229, 1)
# del t[229]
# t.insert(186, 1)
# t.insert(986, 1)
# t.insert(365, 1)
# t.insert(990, 1)
# t.insert(745, 1)
# t.insert(787, 1)
# t.output()
# del t[186]
# t.insert(787,1)

# t.insert(721,1)
# t.insert(445,1)
# t.insert(111,1)
# del t[445]
# t.output()

#t.output()
# t.insert(4, 1)
# t.insert(3, 1)
# t.insert(6, 1)
# del t[5]
# t.output()
# #
