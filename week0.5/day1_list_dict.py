# Week 0.5 · Day 1：list 与 dict 增删查改 + 嵌套
# 规则：只准填 TODO 的地方，不许问 AI 要答案。填完自己跑：python day1_list_dict.py
# 每题下面注释写了「应该打印出什么」，你跑出来对得上才算过。
# 输入法记得切英文态，别打出全角括号。

print("===== Part A：list（有编号的盒子）=====")

# A1. 创建一个 list，里面放三种水果的字符串："apple" "banana" "cherry"
fruits = ["apple","banana", "cherry"]  # TODO: 把 None 换成正确的 list
# 期望 print(fruits) → ['apple', 'banana', 'cherry']
print("A1:", fruits)

# A2. 用「位置」取出第一个水果（记住：从 0 开始数）
first = fruits[0]  # TODO: 取 fruits 的第 0 个
# 期望 → apple
print("A2:", first)

# A3. 增：往 fruits 末尾加一个 "grape"
# TODO: 用 append
fruits.append("grape")
# 期望 print(fruits) → ['apple', 'banana', 'cherry', 'grape']
print("A3:", fruits)

# A4. 改：把第二个水果（banana）改成 "orange"
# TODO: 按位置赋值
fruits[1]=  "orange"
# 期望 print(fruits) → ['apple', 'orange', 'cherry', 'grape']
print("A4:", fruits)

# A5. 删：删掉最后一个元素
# TODO: 用 pop() 或 del
fruits.pop()
# 期望 print(fruits) → ['apple', 'orange', 'cherry']
print("A5:", fruits)

# A6. 数一数现在 fruits 有几个元素
count = len(fruits)  # TODO: 用 len()
# 期望 → 3
print("A6:", count)


print("\n===== Part B：dict（贴标签的抽屉）=====")

# B1. 创建一个 dict，描述一个人：name = "ly"，age = 30
person = {'name':'ly', 'age': 30}  # TODO: 用 {} 和 键值对
# 期望 print(person) → {'name': 'ly', 'age': 30}
print("B1:", person)

# B2. 用「标签名」取出 name（注意：dict 不靠位置，靠 key）
name = person["name"]  # TODO: person[???]
# 期望 → ly
print("B2:", name)

# B3. 加一个新键：city = "shanghai"
# TODO
person["city"] = "shanghai"
# 期望 print(person) → {'name': 'ly', 'age': 30, 'city': 'shanghai'}
print("B3:", person)

# B4. 改：把 age 改成 31
# TODO
person["age"] = 31
# 期望 person['age'] → 31
print("B4:", person)

# B5. 兜底取值：取一个不存在的键 "email"，用 .get() 让它别报错、返回 "无"
email = person.get("email","none")  # TODO: 用 person.get(...) 带默认值
# 期望 → 无
print("B5:", email)


print("\n===== Part C：嵌套 —— 这就是 messages 的真身 =====")

# C1. 手搓一个 messages：list 套 dict
#     里面放两条：
#       第一条 dict：role = "system"，content = "you are a robot"
#       第二条 dict：role = "user"，  content = "who are you"
messages = [{'role':'system', 'content': 'you are a robot'},{'role' : 'user','content': 'who are you'}]  # TODO: 一个 list，里面两个 dict
# 期望 print → [{'role': 'system', 'content': 'you are a robot'},
#               {'role': 'user', 'content': 'who are you'}]
print("C1:", messages)

# C2. 追加一条 assistant 的回复到 messages 末尾
#     role = "assistant"，content = "I am a robot"
# TODO: append 一个新 dict
messages.append({'role': 'assistant', 'content':'i am a robot'})
# 期望 messages 变成 3 条
print("C2 长度:", len(messages) if messages else "还没填 C1")

# C3. 取出「第二条消息」的 content
#     想清楚：先按位置取出第 1 个 dict（list 的活），再按 key 取 content（dict 的活）
second_content = messages[1]['content']# TODO: messages[???][???]
# 期望 → who are you
print("C3:", second_content)
