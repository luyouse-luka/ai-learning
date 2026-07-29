from pypdf import PdfReader

reader = PdfReader("attention.pdf")
text = ""
for page in reader.pages:
    text += page.extract_text()

# 【1】字符数
chars = len(text)
print("字符数:", chars)

# 【2】估算 token 数（1 个英文字符 ≈ 0.3 token）
tokens = chars * 0.3
print("估算 token:", tokens)

# 【3】喂一次的成本（输入单价 $0.14 / 1,000,000 token）
cost = tokens / 1000000 * 0.14
print("喂一次的成本: $", cost)
