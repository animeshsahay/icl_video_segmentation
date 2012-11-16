class SegmentRegister:
    def __init__(self, segments):
        self.segments = segments
        self.index = 0

    def last(self):
        return self.index >= len(self.segments) - 1 

    def first(self):
        return self.index <= 0

    def empty(self):
        return len(self.segments) == 0

    def length(self):
        return len(self.segments)

    def current(self):
        return self.segments[self.index]

    def next(self):
        assert(not self.last())

        self.index += 1
        return self.segments[self.index]

    def previous(self):
        assert(not self.first())

        self.index -= 1
        return self.segments[self.index]

    def select(self, index):
        assert(index >= 0 and index < len(self.segments))

        self.index = index

    def currIndex(self):
        return self.index
