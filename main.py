import nodex
from nodex.nxl import has_tag, attr

ctx = nodex.core.Context((100, 100))

n = nodex.node.Node(ctx)
n2 = nodex.node.Node(ctx)
n3 = nodex.node.Node(ctx)
n4 = nodex.node.Node(ctx) 
n5 = nodex.node.Node(ctx)

n2.add_tag("tag0")
n2.add_tag("tag1")
n3.add_tag("tag0")
n4.add_tag("tag1")
n4.add_tag("tag2")
n5.add_tag("tag2")
n5.add_tag("tag3")

n.bind(n2)
n.bind(n3)
n3.bind(n4)
n4.bind(n5)

n3.bwaaaa = 3
n4.bwaaaa = 4

nodex.node.Node.register(n, "n")
nodex.node.Node.register(n2, "n2")
nodex.node.Node.register(n3, "n3")
nodex.node.Node.register(n4, "n4")
nodex.node.Node.register(n5, "n5")

print(n.search(attr("bwaaaa") == 3, 10))