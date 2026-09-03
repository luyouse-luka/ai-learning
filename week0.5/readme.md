### Week 0.5 复盘
### Day 1 （list/dict）
-学习对于list和dict的创建，增删改查。
-比如messages 本身的结构一个list，其中嵌套了dict，每个 dict 有两个键：role（值为 system/user/assistant）和 content（内容）

### Day 2 （文件读写 + try/except）
-with open(文件名，模式，编码） as f: 
-读取文件内容：f.read()
-写入文件内容：f.write()
-r,w,a 分别使读,写,添加 
-try/except 用于捕获异常，防止程序崩溃。
-毕业脚本三步链路分别是 读 api调用 写


json.dump 存字典进文件,json.load 读回字典, 并且json.load(f) 源是文件， 和json.loads(s)源是字符串