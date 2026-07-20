# AI胜任一切

>一个由AI辅助开发完成的自动化   **[鸣潮](https://mc.kurogames.com)** 项目.

---

核心模块（必备）：
## 1.Client 接口 — 截图、触摸/点击 
## 2.Perception 感知 — OCR、图像模板匹配、像素检测、HP/能量条识别  
## 3.State 管理 — 游戏状态模型、事件与回合追踪、实体列表  
## 4.Planner 策略 — 战术决策、技能优先级、目标选择  
## 5.Executor 执行 — 将决策转换为输入序列、延时与重试  
## 6.Scheduler 调度 — 周期任务、冷却管理、异步队列  
## 7.Config 配置 — 策略参数、按键映射、环境差异  
## 8.Logging/Telemetry — 行为记录、性能与异常上报  
## 9.Safety/Throttle — 随机化、反检测、速率限制  
## 10.Tests & Tools — 回放器、录制/回放、单元测试
>开发优先级建议：
>### 1)搭建 Client + 截图 + 简单 OCR（可验证感知）  
>### 2)实现 game_state 与简单策略（单目标技能循环）  
>### 3)完善执行、调度与安全策略；加入回放与测试

### pip 安装目录：
```bash 
pip install pywin32
```
