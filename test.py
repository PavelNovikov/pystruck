from pystruck import Tree
import random


def test_random_ordering(n_events, deletion_probability):

    keys = []
    t = Tree()
    for i in range(n_events):
        if random.random() < deletion_probability and len(keys) > 0:
            index = random.randint(0, len(keys) - 1)
            key = keys[index]
            print("del %f" % key)
            del t[key]
            del keys[index]
        else:
            new_key = random.random()
            keys.append(new_key)
            print("insert %f" % new_key)
            t.insert(new_key, None)
        t.output()

    assert sorted(keys) == t.get_ordering()

test_random_ordering(100, 0.8)

