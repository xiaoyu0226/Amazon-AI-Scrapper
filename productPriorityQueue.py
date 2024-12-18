import heapq

# Create a min-heap
class ProductPriorityQueue:
    def __init__(self):
        self.heap = []

    def insert(self, product):
        heapq.heappush(self.heap, product)

    def pop_min(self):
        if self.heap:
            return heapq.heappop(self.heap)
        else:
            return None

    def peek_min(self):
        if self.heap:
            return self.heap[0]
        else:
            return None

    def size(self):
        return len(self.heap)

    def is_empty(self):
        return len(self.heap) == 0

