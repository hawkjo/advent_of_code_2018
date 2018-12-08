from collections import Counter

nums = map(int, next(open('input')).strip().split())
touched = Counter()

class node(object):
    def __init__(self, i, parent):
        self.i = i
        self.n_children = nums[i]
        self.n_metadata = nums[i+1]
        self.parent = parent
        self.children = []
        touched[i] += 1
        touched[i + 1] += 1

    def add_children(self):
        next_idx = self.i + 2
        for _ in range(self.n_children):
            child = node(next_idx, self)
            self.children.append(child)
            next_idx = child.add_children()
        self.metadata = nums[next_idx:next_idx + self.n_metadata]
        for i in range(next_idx, next_idx + self.n_metadata):
            touched[i] += 1
        return next_idx + self.n_metadata

    def traverse(self):
        yield self
        for child in self.children:
            for descendant in child.traverse():
                yield descendant

    def sum_sub_metadata(self):
        return sum(sum(node.metadata) for node in self.traverse())

    @property
    def node_value(self):
        if not self.children:
            return sum(self.metadata)
        else:
            return sum(self.children[i-1].node_value
                       for i in self.metadata if i-1 < len(self.children))

    @property
    def depth(self):
        if self.parent is None:
            return 0
        else:
            return self.parent.depth + 1


root = node(0, None)
root.add_children()

print 'Touched all once:', (
    set(touched.keys()) == set(range(len(nums)))
    and len(Counter(touched.values())) == 1
)
print 'Total nodes:', sum(1 for node in root.traverse())
print 'Max tree depth:', max(node.depth for node in root.traverse())
print 'Root num children:', len(root.children)
print 'Num children distribution:', Counter(len(node.children) for node in root.traverse())
print 
print 'Sum of metadata:', root.sum_sub_metadata()
print 'Root value:', root.node_value
