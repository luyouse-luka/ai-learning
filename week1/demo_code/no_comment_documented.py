def f(d, k=3, m="avg"):
    """
    对数值列表进行聚合或采样操作。

    参数:
        d (list[float|int]): 输入的数值列表。
        k (int): 当模式为 'top' 或 'bot' 时，返回前 k 个最大或最小元素，默认为 3。
        m (str): 操作模式，可选 'avg'（平均值）、'top'（前k个最大）、'bot'（前k个最小），默认为 'avg'。

    返回:
        float|list[float|int]|None: 平均值或排序后的列表；如果输入为空则返回 None。

    异常:
        ValueError: 当 m 不是有效模式时抛出。
    """
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
    """
    一个支持回退的数值状态容器类。

    可以存储当前值并记录历史，支持像'撤销'一样的操作。
    """

    def __init__(self, x):
        """
        初始化 C 实例。

        参数:
            x: 初始数值。
        """
        self._x = x  # 当前存储的数值
        self._h = []  # 用于存储历史值的栈

    def u(self, v):
        """
        更新存储的值，并将旧值推入历史栈。

        参数:
            v: 新的数值。

        返回:
            self: 支持链式调用。
        """
        self._h.append(self._x)
        self._x = v
        return self

    def r(self):
        """
        将当前值恢复为最近的历史值（类似于'撤销'）。

        如果历史栈为空，则不改变当前值。

        返回:
            self: 支持链式调用。
        """
        if not self._h:
            return self
        self._x = self._h.pop()
        return self

    @property
    def v(self):
        """
        获取当前存储的值（只读属性）。
        """
        return self._x


def g(s):
    """
    标准化字符串：只保留字母数字字符并转换为小写。

    参数:
        s (str): 待处理的字符串。

    返回:
        str: 去除非字母数字字符并转为小写后的字符串。
    """
    return "".join(c for c in s if c.isalnum()).lower()


def h(a, b):
    """
    检查两个字符串在标准化后是否相等（忽略大小写和非字母数字字符）。

    参数:
        a (str): 第一个字符串。
        b (str): 第二个字符串。

    返回:
        bool: 如果标准化后相等则返回 True，否则返回 False。
    """
    if len(a) != len(b):
        return False
    return g(a) == g(b)


if __name__ == "__main__":
    print(f([1, 2, 3, 4, 5]))
    print(f([1, 2, 3, 4, 5], k=2, m="top"))
    c = C(10).u(20).u(30).r()
    print(c.v)
    print(h("Hello, World!", "hello world"))
    result = "def broken(\n"