import array
from unittest import TestCase

from textide.panels.interval import Interval
from textide.utils import divide_list


class TestInterval(TestCase):
    def test_clone(self):
        self.fail()
    def test_add(self):
        ia=Interval(0,10)
        ib=Interval(6,17)
        ic=Interval(18,17)
        id=Interval(44.536,46.12)

        print(f"ia :: {ia}")
        print(f"ib :: {ib}")
        print(f"{ia} & {ib} :: {ia & ib}")
        print(f"{ia} | {ib} :: {ia | ib}")
        print(f"{ia} + 5 :: {ia + 5}")
        print(f"{ia} + 5 :: {ia - 5}")
        print(f"{ia} * {ib} :: {ia * ib}")
        print(f"{ia} and {ib} :: {ia and ib}")
        print(f"{ia} or {ib} :: {ia or ib}")
        print(f"5 in {ia} :: {5 in ia}")
        print(f"10 in {ia} :: {10 in ia}")
        print(f"0 in {ia} :: {0 in ia}")
        print(f"20 in {ia} :: {20 in ia}")
        num,tolerance = ia.to_number()
        print(f"{ia} :: {num}((+/-){tolerance})")
        num,tolerance = ic.to_number()
        print(f"{ic} :: {num}((+/-){tolerance})")
        num,tolerance = id.to_number()
        print(f"{id} + 4.33 :: {id + 4.33})")
        print(f"{ic} * 2.56 :: {ic * 2.56})")
        print(f"{id} & {ic * 2.56} :: {id & (ic * 2.56)})")
        print(f"{id} | {ic * 2.56} :: {id | (ic * 2.56)})")
        print(f"{id} :: {num}((+/-){tolerance})")

    def test_slices(self):
        indexes = [k for k in range(0, 100)]
        l = len(indexes)
        for by in indexes:
            chunk, pos = divmod(by, 4)
            before,visible,after = divide_list(indexes,by,7)
            print(by,chunk, pos,before,visible,after)

