class Element:
    def __init__(self, key, value, l_p=None, r_p=None):
        self.value = value
        self.key = key
        self.l_p = l_p
        self.r_p = r_p


class ICache:
    def __init__(self, capacity: int = 10) -> None:
        if capacity <= 0 or not isinstance(capacity, int):
            raise ValueError
        self.pointers = {}
        self.last = self.top = None
        self.capacity = capacity

    def _remove_element(self, elem: Element) -> None:
        if elem is self.top:
            self.top = elem.l_p
        if elem is self.last:
            self.last = elem.r_p
        if elem.l_p is not None:
            elem.l_p.r_p = elem.r_p
        if elem.r_p is not None:
            elem.r_p.l_p = elem.l_p

    def get(self, key: str) -> str:
        res = self.pointers.get(key)
        if res is None:
            return ''
        self._remove_element(res)
        if self.top is not None:
            self.top.r_p = res
            res.l_p, res.r_p = self.top, None
        self.top = res
        return res.value

    def set(self, key: str, value: str) -> None:
        if self.pointers.get(key) is not None:
            self.delete(key)
        if self.capacity < len(self.pointers)+1:
            del_key = self.last.key
            self.last = self.last.r_p
            self.delete(del_key)
        elem = Element(key, value, self.top)
        self.pointers[key] = elem
        if self.last is None:
            self.last = self.top = elem
        else:
            self.top.r_p = elem
            self.top = elem

    def delete(self, key: str) -> None:
        elem = self.pointers.pop(key)
        self._remove_element(elem)
        del elem


class Ilist(list):
    def _get(self, i):
        return self[i] if i < len(self) else 0

    def __add__(self, other):
        return list(self._get(i) + other._get(i) for i
                    in range(max(len(self), len(other))))

    def __sub__(self, other):
        return list(self._get(i) - other._get(i) for i
                    in range(max(len(self), len(other))))

    def __eq__(self, other):
        return sum(self) == sum(other)

    def __lt__(self, other):
        return sum(self) < sum(other)

    def __gt__(self, other):
        return sum(self) > sum(other)

    def __ge__(self, other):
        return sum(self) >= sum(other)

    def __le__(self, other):
        return sum(self) <= sum(other)
