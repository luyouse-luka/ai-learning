# 故意写得乱、没注释的样本代码
# Day 6 用它来测试你的"代码注释生成器"
# 不要修改这个文件 — 让它一直保持难懂


def f(d, k=3, m="avg"):
    if not d:
        return None
    if m == "avg":
        return sum(d) / len(d)
    elif m == "top":
        return sorted(d, reverse=True)[:k]
    elif m == "bot":
        return sorted(d)[:k]
    else:
        raise ValueError(m)


class C:
    def __init__(self, x):
        self._x = x
        self._h = []

    def u(self, v):
        self._h.append(self._x)
        self._x = v
        return self

    def r(self):
        if not self._h:
            return self
        self._x = self._h.pop()
        return self

    @property
    def v(self):
        return self._x


def g(s):
    return "".join(c for c in s if c.isalnum()).lower()


def h(a, b):
    if len(a) != len(b):
        return False
    return g(a) == g(b)


if __name__ == "__main__":
    print(f([1, 2, 3, 4, 5]))
    print(f([1, 2, 3, 4, 5], k=2, m="top"))
    c = C(10).u(20).u(30).r()
    print(c.v)
    print(h("Hello, World!", "hello world"))
