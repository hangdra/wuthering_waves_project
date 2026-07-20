# @Author  : liuha
# @Time    : 2026/7/20 22:21
# @File    : mark_down.py
# 读取为纯文本
with open('F:\code\hello world\什么是MCP.md', 'r', encoding='utf-8') as f:
    content = f.read()

print(content)

# 如需解析 Markdown 为 HTML
import markdown
html = markdown.markdown(content)
with open('F:\code\hello world\什么是MCP.html', 'w', encoding='utf-8') as f:
    f.write(html)
