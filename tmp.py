from rtree import index

boxes = index.Index()
boxes.insert(1,[-97, 32.71, -96, 32.73])
print list(boxes.intersection((32.72,-96.68)))


