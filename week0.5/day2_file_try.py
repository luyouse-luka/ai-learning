# Week 0.5 · Day 2：with open 文件读写 + try/except 异常处理
# 规则：只填 TODO，不许问 AI 要答案。填完自己跑：python3 day2_file_try.py
# 每题注释写了「应该发生什么」，跑出来对得上才算过。
# 输入法切英文态，别打全角括号。

print("===== Part A：写文件（'w' 覆盖写）=====")

# A1. 用 with open 以 'w' 模式打开 "note.txt"，把字符串 "hello python\n" 写进去
#     提示：with open(文件名, 模式, encoding="utf-8") as f:  然后 f.write(...)
#     （encoding="utf-8" 是防中文乱码的好习惯，你 Day5 踩过编码坑）
# TODO: 在下面写这个 with 块

with open("note.txt","w",encoding="utf-8") as f:
    f.write("hello python\n")
# 期望：当前目录多出一个 note.txt，里面是 hello python
print("A1: 写完了，去看看 note.txt")


print("\n===== Part B：读文件（'r' 只读）=====")

# B1. 用 with open 以 'r' 模式打开 "note.txt"，把全部内容读进变量 content
content = None
with open("note.txt", "r", encoding="utf-8") as f: 
     content = f.read()
# TODO: 用 with open + f.read()，把结果赋给 content
# 期望 print → hello python
print("B1:", content)


print("\n===== Part C：追加（'a' 接着写）=====")

# C1. 用 'a' 模式打开 "note.txt"，再追加一行 "second line\n"
# TODO: with 块
# 期望：note.txt 现在有两行

# C2. 再用 'r' 读一遍，确认变成了两行
content2 = None  # TODO
with open("note.txt", "a", encoding ="utf-8") as f: 
    f.write("second line\n")
with open("note.txt", "r", encoding="utf-8") as f:
    content2 = f.read()
# 期望 print → hello python
#              second line
print(f"C2:\n{content2 if content2 else '还没填'}")


print("\n===== Part D：try/except（接住错误）=====")

# D1. 故意去读一个不存在的文件 "not_exist.txt"，会抛 FileNotFoundError
#     用 try/except 接住它，别让程序崩溃，except 里打印 "文件不存在，已兜底"
# TODO: 写 try/except 块
#   try:
#       用 with open 读 "not_exist.txt"
#   except FileNotFoundError:
#       print("文件不存在，已兜底")
# 期望：程序不崩溃，打印出「文件不存在，已兜底」，然后继续往下跑

try: 
    with open("not_exist.txt", "r", encoding="utf-8") as f:
        content3 = f.read()
except FileNotFoundError:
    print("文件不存在，已兜底")
print("D1: 上面这行如果打印了兜底信息，说明你接住了错误")


print("\n===== Part E：桥梁 —— 这就是毕业脚本的雏形 =====")
# 不用填代码，只回答问题（写在你给我的回复里，不用写进文件）：
# 想一下「读文件 → 调 API → 存结果」这个毕业脚本：
#   Q1. 读用户输入的文件，该用 'r' 'w' 'a' 哪个模式？
#   Q2. 把 API 返回的结果存进一个新文件，该用哪个模式？
#   Q3. 如果用户给的文件路径不存在，用什么机制让程序别崩？
print("E: 回答 Q1/Q2/Q3 给教练")
