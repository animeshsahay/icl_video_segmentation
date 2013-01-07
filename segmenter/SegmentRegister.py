import os
import os.path
import shutil
import csv

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
        return self.segments[self.index][0]

    def next(self):
        assert(not self.last())

        self.index += 1
        return self.current()

    def previous(self):
        assert(not self.first())

        self.index -= 1
        return self.current()

    def select(self, index):
        assert(index >= 0 and index < len(self.segments))

        self.index = index

    def getIndexFromStartEnd(self, start, end):
        for i, (_, s, e) in enumerate(self.segments):
            if s == start and e == end:
                return i

        return None

    def currIndex(self):
        return self.index

    def save(self, fileName):
        os.mkdir(fileName)
        with open(os.path.join(fileName, "segments.csv"), 'wb') as raw:
            f = csv.writer(raw)
            for (name, s, e) in self.segments:
                f.writerow([s, e, os.path.split(name)[1]])
                shutil.copy(name, fileName)
    
            raw.close()
