
class Interval:
    def __init__(self, start, end):
        self.start = min(start,end)
        self.end = max(start,end)

    def __contains__(self, value: int) -> bool:
        return self.start <= value <= self.end

    def __repr__(self):
        return f"[{self.start}, {self.end}]"

    def __len__(self):
        return self.end - self.start + 1

    def overlaps(self, other: 'Interval') -> bool:
        return self.start <= other.end and other.start <= self.end

    def intersection(self, other: 'Interval') -> 'Interval | None':
        if not self.overlaps(other):
            return None
        return Interval(max(self.start, other.start), min(self.end, other.end))

    def union(self, other: 'Interval') -> 'Interval | None':
        if not self.overlaps(other) and not (self.end + 1 == other.start or other.end + 1 == self.start):
            return None
        return Interval(min(self.start, other.start), max(self.end, other.end))

    # Operator overloads
    def __and__(self, other: 'Interval') -> 'Interval | None':
        """Intersection: interval1 & interval2"""
        return self.intersection(other)

    def __or__(self, other: 'Interval') -> 'Interval | None':
        """Union: interval1 | interval2"""
        return self.union(other)

    def __add__(self, value) -> 'Interval':
        """Shift interval to the right by value"""
        return Interval(self.start + value, self.end + value)

    def __sub__(self, value) -> 'Interval':
        """Shift interval to the left by value"""
        return Interval(self.start - value, self.end - value)

    def __mul__(self, value) -> 'Interval':
        if isinstance(value, Interval):
            candidates = [
                self.start * value.start,
                self.start * value.end,
                self.end * value.start,
                self.end * value.end,
            ]
            endpoints = [min(candidates), max(candidates)]
        else:
            endpoints = [self.start * value, self.end * value]
        return Interval(min(endpoints), max(endpoints))
    def to_number(self) -> (any,any):
        return (self.start + self.end) / 2, (self.end - self.start) / 2

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Interval) and self.start == other.start and self.end == other.end