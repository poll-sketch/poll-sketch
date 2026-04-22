# Python AI智能体开发教学项目

## 项目概述

本项目是一个基于Python的AI智能体开发教学项目，旨在通过实践案例帮助学习者掌握AI智能体的开发技能，特别是如何与大型语言模型(LLM)进行交互。

## 目录结构

```
├── practice01/         # 实践案例目录
│   └── llm_client.py   # LLM客户端实现
├── practice02/         # 实践案例目录
│   ├── tool_client.py  # 工具调用客户端实现
│   └── tool_chat_client.py  # 工具调用客户端实现（副本）
├── practice03/         # 实践案例目录
│   └── summarize_chat_client.py  # 聊天记录总结客户端实现
├── practice04/         # 实践案例目录
│   └── search_chat_client.py  # 聊天历史5W提取与搜索客户端实现
├── practice05/         # 实践案例目录
│   └── tool_client.py  # AnythingLLM文档仓库访问客户端实现
├── requirements/       # 依赖配置
│   └── base.txt        # 基础依赖包
├── venv/               # 虚拟环境
├── .gitignore          # Git忽略文件
├── env.example         # 环境变量模板
└── README.md           # 项目说明文档
```

## 文件功能说明

### 1. practice01/llm_client.py

**功能用途：**
- 实现了一个使用Python标准http库访问OpenAI兼容协议LLM的客户端
- 支持读取项目根目录的.env文件配置
- 统计LLM调用的token消耗、响应时间和token处理速度
- 提供详细的调用结果和统计信息输出

**核心功能：**
- `load_env()`: 读取.env文件中的配置参数
- `call_llm()`: 使用标准http库调用LLM API
- 支持HTTPS和HTTP连接
- 详细的错误处理
- 完整的统计信息计算和展示

### 2. practice01/chat_client.py

**功能用途：**
- 实现了一个交互式终端聊天界面
- 支持流式输出，实时显示AI回复
- 自动管理聊天历史，保持上下文连续性
- 支持Ctrl+C退出终端

**核心功能：**
- `load_env()`: 读取.env文件中的配置参数
- `call_llm_stream()`: 使用流式方式调用LLM API
- `chat_loop()`: 实现交互式聊天循环
- 自动将历史聊天记录添加到上下文
- 支持实时流式输出AI回复
- 聊天历史长度限制（默认保留最近10条消息）

### 3. practice02/tool_client.py

**功能用途：**
- 实现了一个支持工具调用的AI智能体
- 提供6个工具：列出目录、修改文件名、删除文件、新建文件、读取文件、curl网络访问
- 支持LLM通过工具调用执行文件操作和网络访问
- 保持上下文连续性，支持多轮对话

**核心功能：**
- 工具函数：
  - `list_directory()`: 列出目录下的文件和子目录
  - `rename_file()`: 修改文件或目录的名称
  - `delete_file()`: 删除文件
  - `create_file()`: 新建文件并写入内容
  - `read_file()`: 读取文件内容
  - `curl_request()`: 通过curl访问网页并返回内容
- `call_llm_with_tools()`: 支持工具调用的LLM API调用
- `process_tool_calls()`: 处理LLM的工具调用请求
- `chat_loop()`: 实现支持工具调用的交互式聊天循环

### 4. practice02/tool_chat_client.py

**功能用途：**
- 与tool_client.py功能相同，是tool_client.py的副本
- 提供相同的6个工具调用能力
- 支持LLM通过工具调用执行文件操作和网络访问
- 保持上下文连续性，支持多轮对话

**核心功能：**
- 与tool_client.py完全相同的工具函数和核心功能
- 提供相同的交互式聊天界面
- 支持相同的工具调用能力

### 5. env.example

**功能用途：**
- 提供OpenAI兼容协议LLM的配置模板
- 用户可以复制为.env文件并填写正确的参数

**配置项：**
- BASE_URL: API基础URL
- MODEL: 模型名称
- API_KEY: API密钥
- TEMPERATURE: 温度参数
- MAX_TOKENS: 最大输出token数
- TIMEOUT: 超时时间

### 6. practice03/summarize_chat_client.py

**功能用途：**
- 实现了一个支持聊天记录自动总结的AI智能体
- 当聊天超过5轮或上下文长度超过3k时，会自动触发LLM执行聊天记录总结
- 对前70%左右的内容进行压缩，最后30%左右的内容保留原文
- 保持上下文连续性，支持多轮对话

**核心功能：**
- 继承了practice02的6个工具调用能力
- `calculate_chat_length()`: 计算聊天历史的长度（字符数）
- `calculate_chat_turns()`: 计算聊天轮数（用户和AI的交互次数）
- `summarize_chat_history()`: 总结聊天记录，压缩前70%内容，保留后30%内容
- 自动检测聊天轮数和上下文长度，触发总结
- 保持聊天的连贯性和上下文理解

### 7. practice04/search_chat_client.py

**功能用途：**
- 实现了一个支持聊天记录5W提取和搜索的AI智能体
- 每5次聊天自动提取5W关键信息（Who、What、When、Where、Why）并保存到本地
- 支持使用/search命令或关键词搜索聊天历史
- 保持上下文连续性，支持多轮对话

**核心功能：**
- 继承了practice03的所有功能
- `extract_5w_info()`: 提取聊天记录的5W关键信息并保存到D:\chat-log\log.txt
- `should_search_chat_history()`: 检测用户是否需要搜索聊天历史
- `read_chat_log()`: 读取本地聊天历史记录文件
- `append_to_file()`: 追加内容到文件（支持自动创建目录）
- 支持三种搜索触发方式：
  1. 用户输入以"/search"开头
  2. 用户表达"查找聊天历史"等意思
  3. LLM认为应该搜索聊天历史
- 5W信息提取格式：[时间戳] Who: xxx | What: xxx | When: xxx | Where: xxx | Why: xxx
- 聊天历史存储位置：D:\chat-log\log.txt（自动创建目录和文件）

### 8. practice05/tool_client.py

**功能用途：**
- 实现了一个支持AnythingLLM本地服务集成的AI智能体
- 当用户提到"文档仓库"、"文件仓库"、"仓库"等关键词时，会自动调用AnythingLLM查询
- 保持上下文连续性，支持多轮对话

**核心功能：**
- 继承了practice04的所有功能
- `anythingllm_query()`: 使用subprocess调用curl命令查询AnythingLLM文档仓库
- `fetch_webpage()`: 访问网页并返回内容
- 支持从.env文件读取AnythingLLM配置
- 正确处理中文编码问题
- 支持API密钥认证
- 当用户提到仓库相关关键词时，优先调用AnythingLLM查询工具

**配置要求：**
- 需要启动AnythingLLM本地服务（http://localhost:3001）
- 需要在.env文件中配置：
  - ANYTHINGLLM_API_KEY: AnythingLLM的API密钥
  - ANYTHINGLLM_WORKSPACE_SLUG: 工作区的Slug ID

### 9. requirements/base.txt

**功能用途：**
- 列出AI智能体开发所需的基础依赖包
- 包括数据处理、机器学习、自然语言处理等相关库

## 教学目标

1. **环境配置与管理**
   - 学习如何创建和管理Python虚拟环境
   - 掌握环境变量的配置和使用
   - 了解项目依赖管理

2. **HTTP客户端开发**
   - 学习使用Python标准http库发送API请求
   - 掌握HTTP/HTTPS连接的建立和管理
   - 理解RESTful API的调用方式

3. **LLM接口集成**
   - 了解OpenAI兼容协议的API结构
   - 掌握与LLM进行交互的方法
   - 学习如何处理API响应和错误

4. **性能统计与分析**
   - 学习如何统计和分析API调用的性能指标
   - 掌握token消耗的计算方法
   - 理解响应时间和处理速度的重要性

5. **项目结构设计**
   - 学习如何组织一个AI项目的目录结构
   - 了解配置文件的管理方式
   - 掌握Git版本控制的基本配置

6. **交互式终端开发**
   - 学习如何创建交互式终端应用
   - 掌握用户输入的处理方法
   - 了解终端界面的设计原则

7. **流式数据处理**
   - 学习如何处理流式API响应
   - 掌握实时数据输出的实现方法
   - 理解流式处理的优势和应用场景

8. **对话管理**
   - 学习如何管理聊天历史和上下文
   - 掌握对话状态的维护方法
   - 理解上下文在对话中的重要性

9. **工具调用集成**
   - 学习如何为AI智能体添加工具调用能力
   - 掌握工具函数的设计和实现方法
   - 理解工具调用的工作流程和原理

10. **文件操作处理**
    - 学习如何实现基本的文件操作功能
    - 掌握文件系统的基本操作方法
    - 理解文件操作的错误处理机制

11. **信息提取与存储**
    - 学习如何从聊天记录中提取关键信息（5W规则）
    - 掌握增量更新文件的方法
    - 理解结构化信息存储的意义

12. **历史记录搜索**
    - 学习如何实现聊天历史的搜索功能
    - 掌握多种搜索触发方式的实现
    - 理解上下文感知搜索的重要性

## 使用方法

### 1. 配置环境

1. 复制`env.example`为`.env`文件
2. 填写正确的LLM配置参数

### 2. 运行示例

**运行基础LLM客户端：**
```bash
# 激活虚拟环境（Windows）
venv\Scripts\Activate.ps1

# 运行LLM客户端
python practice01/llm_client.py
```

**运行交互式聊天终端：**
```bash
# 激活虚拟环境（Windows）
venv\Scripts\Activate.ps1

# 运行聊天终端
python practice01/chat_client.py
```

**运行工具调用终端：**
```bash
# 激活虚拟环境（Windows）
venv\Scripts\Activate.ps1

# 运行工具调用终端
python practice02/tool_client.py
```

**运行tool_chat_client.py：**
```bash
# 激活虚拟环境（Windows）
venv\Scripts\Activate.ps1

# 运行tool_chat_client.py
python practice02/tool_chat_client.py
```

**运行聊天记录总结终端：**
```bash
# 激活虚拟环境（Windows）
venv\Scripts\Activate.ps1

# 运行聊天记录总结终端
python practice03/summarize_chat_client.py
```

**运行聊天历史5W提取与搜索终端：**
```bash
# 激活虚拟环境（Windows）
venv\Scripts\Activate.ps1

# 运行聊天历史5W提取与搜索终端
python practice04/search_chat_client.py
```

**运行AnythingLLM文档仓库访问终端：**
```bash
# 激活虚拟环境（Windows）
venv\Scripts\Activate.ps1

# 运行AnythingLLM文档仓库访问终端
python practice05/tool_client.py
```

### 3. 5W聊天历史功能说明

**聊天历史存储位置：** D:\chat-log\log.txt

**自动提取触发条件：** 每5次聊天自动提取一次

**5W信息格式：**
```
[时间戳] Who: xxx | What: xxx | When: xxx | Where: xxx | Why: xxx
```

**搜索聊天历史的方式：**
1. 使用`/search`命令开头，如：`/search 张三`
2. 表达查找意图，如：`查找聊天历史`、`搜索聊天记录`
3. LLM根据上下文自动判断需要搜索历史

### 4. 自定义提示词

- **基础客户端**：修改`llm_client.py`中的`prompt`变量
- **聊天终端**：直接在终端中输入消息即可

## 技术特点

- **无额外依赖**：使用Python标准库实现，无需安装额外依赖
- **兼容性强**：支持任何OpenAI兼容协议的LLM
- **详细统计**：提供完整的性能统计信息
- **清晰结构**：代码结构清晰，注释完善
- **错误处理**：包含完整的错误处理机制
- **流式输出**：支持实时流式显示AI回复
- **交互式界面**：提供友好的终端聊天界面
- **上下文管理**：自动维护聊天历史和上下文
- **用户友好**：支持Ctrl+C优雅退出
- **可扩展性**：易于扩展和定制功能
- **工具调用**：支持LLM调用外部工具执行文件操作
- **文件操作**：提供完整的文件系统操作功能
- **智能决策**：LLM可以根据需求自动选择合适的工具
- **信息提取**：支持5W规则提取关键信息
- **历史搜索**：支持多种方式搜索聊天历史
- **增量存储**：聊天历史支持增量更新
- **AnythingLLM集成**：支持与本地AnythingLLM服务集成，查询文档仓库
- **仓库感知**：当提到仓库相关关键词时自动调用AnythingLLM查询

## 后续扩展

本项目可以作为基础框架，进一步扩展以下功能：

1. 添加更多LLM提供商的支持
2. 实现批量请求和并发处理
3. 添加缓存机制减少重复请求
4. 实现更复杂的对话管理
5. 集成其他AI服务和工具
6. 支持更多格式的信息提取
7. 实现跨会话的聊天历史管理

## 教学建议

1. **循序渐进**：从环境配置开始，逐步掌握HTTP客户端开发和LLM集成
2. **实践为主**：通过修改代码和配置，实际体验LLM的调用过程
3. **性能分析**：分析不同模型和参数对性能的影响
4. **扩展应用**：鼓励学习者基于此框架开发更复杂的AI应用

---

本项目旨在为AI智能体开发提供一个基础教学框架，帮助学习者快速掌握与LLM交互的核心技能。