好的，继续按照 SPEC 范式生成 **api.md**。这里将讲义的每个章节/模块视为可“调用”的功能单元，使用伪代码形式定义其输入、输出和处理逻辑。

---

# 提示词工程讲义 API 规格说明书

## 1. 文档说明

| 项目项 | 内容 |
|--------|------|
| 关联规格 | spec.md v1.0, requirement.md v1.0 |
| 设计范式 | 将讲义视为一个“教学系统”，每个章节/模板/练习为一个可调用的函数 |
| 伪代码风格 | 类 Python/TypeScript，侧重语义清晰而非语法严格 |

---

## 2. 全局类型定义

```typescript
// 通用类型
type Prompt = string
type TaskType = "writing" | "analysis" | "code" | "translation" | "roleplay" | "creative"
type Principle = "specific" | "unambiguous" | "role" | "example"
type Trap = "over_constraint" | "vague" | "false_premise" | "no_iteration" | "format_ignore" | "role_conflict"

// 讲义章节结构
interface Chapter {
  title: string
  target: string[]          // 本章目标
  pages: number             // 页数估算
  sections: Section[]
}

interface Section {
  title: string
  content: () => void       // 输出讲解内容
  examples: ExamplePair[]   // 正反对比
}

interface ExamplePair {
  good: Prompt
  bad: Prompt
  explanation: string
}

interface Template {
  name: string
  taskType: TaskType
  skeleton: string          // 带占位符 {placeholder}
  fillableForm: string      // 即填即用版
  example: Prompt
}

interface Project {
  name: string
  estimatedMinutes: number
  steps: {
    phase: "requirement" | "design" | "iteration" | "final"
    action: () => void
  }[]
}
```

---

## 3. 讲义核心函数

### 3.1 讲义初始化

```python
def initialize_handbook() -> Handbook:
    """
    初始化讲义系统，设置全局配置。
    
    输出:
        - 图标系统说明页
        - 两种阅读路径（课堂/自学）
        - 工具中立声明
    
    返回:
        Handbook: 讲义对象，包含所有章节和附录
    """
    handbook = Handbook()
    
    # 设置图标系统
    handbook.set_icons({
        "key_point": "🎯",
        "trap": "⚠️",
        "good_example": "✅",
        "bad_example": "❌",
        "template": "🛠️",
        "exercise": "📝",
        "project": "🚀"
    })
    
    # 设置阅读路径
    handbook.add_reading_path("classroom", ["ch0", "ch1", "ch2", "ch3", "ch4", "ch5", "ch6", "appendix"])
    handbook.add_reading_path("self_study", ["ch0", "ch1", "ch2", "ch3", "ch5", "ch6", "appendix", "ch4"])
    
    # 工具中立声明
    handbook.set_compatibility(["ChatGPT", "Kimi", "文心一言", "Claude", "通义千问"])
    
    return handbook
```

---

### 3.2 第1章：提示词基础

```python
class Chapter1:
    """提示词基础：让AI听懂你的话"""
    
    def __init__(self):
        self.title = "提示词基础"
        self.target = ["理解什么是提示词", "掌握三大要素", "能写出基础提示词"]
        self.pages = "4-6"
    
    def teach_elements(self) -> dict:
        """
        讲解三大要素：指令 / 上下文 / 输出格式
        
        返回:
            dict: 包含每个要素的定义和示例
        """
        elements = {
            "instruction": {
                "definition": "告诉AI要做什么",
                "example_good": "请列出3个提高写作效率的方法",
                "example_bad": "关于效率",
                "pseudo_code": """
                def build_instruction(task):
                    return f"请{task}"
                """
            },
            "context": {
                "definition": "提供背景信息，帮助AI理解",
                "example_good": "我正在写一篇关于气候变化的科普文章，目标读者是中学生。请用比喻的方式解释温室效应。",
                "example_bad": "解释温室效应",
                "pseudo_code": """
                def build_context(audience, topic, constraint):
                    return f"目标读者是{audience}，主题是{topic}，要求{constraint}"
                """
            },
            "format": {
                "definition": "指定输出的结构",
                "example_good": "请按以下格式输出：1. 原因；2. 影响；3. 建议",
                "example_bad": "随便写写",
                "pseudo_code": """
                def build_format(structure):
                    return f"请按以下格式输出：{structure}"
                """
            }
        }
        return elements
    
    def general_formula(self, role: str, task: str, detail: str, output_format: str) -> Prompt:
        """
        通用公式：角色 + 任务 + 细节 + 输出格式
        
        参数:
            role: 角色设定，如“你是一位资深编辑”
            task: 具体任务，如“帮我润色这段文字”
            detail: 细节要求，如“保持口语化，不要改变原意”
            output_format: 输出格式，如“直接给出修改后的文字，不要解释”
        
        返回:
            Prompt: 完整的提示词字符串
        """
        prompt = f"{role}。{task}。{detail}。{output_format}"
        return prompt
    
    def compare_good_vs_bad(self, level: str = "basic") -> list[ExamplePair]:
        """
        返回正反面对比示例
        
        参数:
            level: "basic" | "intermediate"
        
        返回:
            list[ExamplePair]: 至少3组示例
        """
        if level == "basic":
            return [
                ExamplePair(
                    good="你是一位营养师。请为一位素食主义者设计一日三餐的食谱，每餐列出3个选项。",
                    bad="给我一个食谱",
                    explanation="差例没有角色、没有受众、没有输出结构"
                ),
                # ... 另外2组
            ]
```

---

### 3.3 第2章：4个核心原则

```python
class Chapter2:
    """好提示词的4个核心原则"""
    
    def __init__(self):
        self.principles = ["specific", "unambiguous", "role", "example"]
    
    def apply_principle_specific(self, vague_prompt: Prompt) -> Prompt:
        """
        原则一：具体。将模糊提示词转化为具体提示词
        
        参数:
            vague_prompt: 模糊的提示词，如“写一篇文章”
        
        返回:
            Prompt: 具体化后的提示词，如“写一篇500字关于如何在家种植薄荷的说明文，分3个步骤”
        
        算法:
            1. 识别模糊词汇（文章→什么类型？多长？）
            2. 追问5W1H（Who What When Where Why How）
            3. 生成具体约束
        """
        # 伪代码实现
        vagueness_patterns = ["文章", "总结", "分析", "帮助"]
        if any(pattern in vague_prompt for pattern in vagueness_patterns):
            # 触发细化流程
            specific_prompt = self._refine_with_5w1h(vague_prompt)
        return specific_prompt
    
    def apply_principle_unambiguous(self, ambiguous_prompt: Prompt) -> Prompt:
        """
        原则二：无歧义。消除模棱两可的表达
        
        参数:
            ambiguous_prompt: 有歧义的提示词，如“总结一下这个会议”
        
        返回:
            Prompt: 无歧义后的提示词，如“请用3个要点总结本次会议的决定项、待办事项和风险”
        """
        ambiguous_phrases = ["一下", "一些", "几个", "相关的"]
        resolved_prompt = ambiguous_prompt
        for phrase in ambiguous_phrases:
            resolved_prompt = resolved_prompt.replace(phrase, "")
        # 添加量化要求
        resolved_prompt += "请用具体数字或列表形式输出"
        return resolved_prompt
    
    def get_role_template(self, domain: str, expertise: str) -> str:
        """
        原则三：设定角色。生成角色设定模板
        
        参数:
            domain: 领域，如“医疗”、“法律”、“教育”
            expertise: 专业程度，如“资深专家”、“初级顾问”
        
        返回:
            str: 角色设定语句
        """
        return f"你是一位{expertise}，专精于{domain}领域。"
    
    def apply_principle_example(self, task: str, example_input: str, example_output: str) -> Prompt:
        """
        原则四：给出示例（Few-shot）。在提示词中嵌入示例
        
        参数:
            task: 任务描述
            example_input: 示例输入
            example_output: 示例输出
        
        返回:
            Prompt: 包含示例的提示词
        
        伪代码:
            prompt = f"{task}\n\n示例：\n输入：{example_input}\n输出：{example_output}\n\n现在请处理："
        """
        prompt = f"""{task}

示例：
输入：{example_input}
输出：{example_output}

现在请处理以下输入："""
        return prompt
```

---

### 3.4 第3章：模板库

```python
class Chapter3:
    """任务类型与万能模板库"""
    
    def __init__(self):
        self.templates = {}
    
    def register_template(self, task_type: TaskType, template: Template) -> None:
        """注册一个任务模板"""
        self.templates[task_type] = template
    
    def get_template(self, task_type: TaskType) -> Template:
        """获取指定任务类型的模板"""
        return self.templates.get(task_type)
    
    def writing_template(self, genre: str, topic: str, tone: str, length: str) -> Prompt:
        """
        写作类模板
        
        参数:
            genre: 体裁（报告/邮件/故事/推文）
            topic: 主题
            tone: 语气（正式/轻松/幽默/专业）
            length: 篇幅（短/中/长）
        
        返回:
            Prompt: 可直接使用的提示词
        
        伪代码:
            return f"请写一篇{genre}，主题是{topic}。语气要求：{tone}。篇幅：{length}。"
        """
        skeleton = f"请写一篇{genre}，主题是{topic}。语气要求：{tone}。篇幅：{length}。"
        fillable_form = f"""
【任务类型】写作-{genre}
【主题】____
【语气】____
【篇幅】____
【额外要求】____
"""
        return skeleton + "\n\n即填即用版：\n" + fillable_form
    
    def analysis_template(self, content: str, analysis_type: str, output_structure: str) -> Prompt:
        """
        分析类模板
        
        参数:
            content: 待分析的内容
            analysis_type: 分析类型（总结/对比/评价/拆解）
            output_structure: 输出结构
        
        返回:
            Prompt: 完整的分析类提示词
        """
        return f"""
请对以下内容进行{analysis_type}：

【内容】
{content}

【输出要求】
请按以下结构输出：
{output_structure}
"""
    
    def code_template(self, language: str, task: str, constraints: list[str]) -> Prompt:
        """
        代码类模板
        
        参数:
            language: 编程语言（Python/SQL/JavaScript等）
            task: 编程任务
            constraints: 约束条件列表
        
        返回:
            Prompt: 代码生成提示词
        """
        constraints_str = "\n".join([f"- {c}" for c in constraints])
        return f"""
请用{language}编写代码，完成以下任务：
{task}

约束条件：
{constraints_str}

请只输出代码，不要额外解释。添加必要的注释。
"""
    
    def translation_template(self, text: str, source_lang: str, target_lang: str, style: str) -> Prompt:
        """
        翻译类模板
        
        参数:
            text: 待翻译文本
            source_lang: 源语言
            target_lang: 目标语言
            style: 翻译风格（直译/意译/术语统一/文学化）
        
        返回:
            Prompt: 翻译提示词
        """
        style_map = {
            "直译": "逐字逐句翻译，保持原文结构",
            "意译": "在保持原意的前提下，使译文更符合目标语言习惯",
            "术语统一": "保持专业术语的一致性",
            "文学化": "使用优美的文学表达"
        }
        return f"""请将以下{source_lang}文本翻译成{target_lang}。
翻译风格：{style_map.get(style, style)}
文本：{text}
"""
    
    def roleplay_template(self, character: str, scenario: str, user_role: str, goal: str) -> Prompt:
        """
        角色扮演类模板
        
        参数:
            character: AI扮演的角色
            scenario: 场景描述
            user_role: 用户扮演的角色
            goal: 对话目标
        
        返回:
            Prompt: 角色扮演提示词
        """
        return f"""
【角色设定】你是一位{character}。
【场景】{scenario}
【我的角色】我是{user_role}。
【对话目标】{goal}
请开始对话，每次回复不超过3句话，保持角色一致性。
"""
    
    def creative_template(self, seed: str, count: int, constraints: list[str]) -> Prompt:
        """
        创意生成类模板
        
        参数:
            seed: 创意种子（主题/关键词）
            count: 生成数量
            constraints: 约束条件
        
        返回:
            Prompt: 创意生成提示词
        """
        constraints_str = "、".join(constraints)
        return f"""
基于“{seed}”，请生成{count}个创意想法。
要求：{constraints_str}
每个想法用一句话描述，编号列出。
"""
```

---

### 3.5 第4章：陷阱检测

```python
class Chapter4:
    """常见陷阱与误区检测"""
    
    # 陷阱定义字典
    TRAP_DEFINITIONS = {
        "over_constraint": {
            "name": "过度约束",
            "detect": lambda p: len(p.split("。")) > 8 and "并且" in p and "同时" in p,
            "fix": lambda p: "请将约束条件精简到3条以内，去掉重复或矛盾的项。"
        },
        "vague": {
            "name": "模糊指令",
            "detect": lambda p: any(word in p for word in ["一些", "几个", "相关的", "不错的"]),
            "fix": lambda p: "请将模糊词汇替换为具体数字、例子或可衡量的标准。"
        },
        "false_premise": {
            "name": "虚假前提",
            "detect": lambda p: "你昨天" in p or "你之前说过" in p,
            "fix": lambda p: "AI没有记忆（除非对话上下文），请在每次提示词中提供完整信息。"
        },
        "no_iteration": {
            "name": "遗忘迭代",
            "detect": lambda p: len(p) > 200 and "请一步到位" in p,
            "fix": lambda p: "将复杂任务拆解为3-5步，分多次对话完成。"
        },
        "format_ignore": {
            "name": "忽视输出格式",
            "detect": lambda p: "输出" not in p and "格式" not in p,
            "fix": lambda p: p + "请指定输出格式，如列表、表格、JSON等。"
        },
        "role_conflict": {
            "name": "角色冲突",
            "detect": lambda p: "你是一位" in p and ("但同时" in p or "另外你也是" in p),
            "fix": lambda p: "请保持单一角色设定，或将不同角色拆分为两次对话。"
        }
    }
    
    def detect_traps(self, prompt: Prompt) -> list[dict]:
        """
        检测提示词中的陷阱
        
        参数:
            prompt: 待检测的提示词
        
        返回:
            list[dict]: 检测到的陷阱列表，每个陷阱包含 name, severity, fix
        
        算法:
            1. 遍历所有陷阱定义
            2. 应用 detect 函数
            3. 收集命中的陷阱
        """
        detected = []
        for trap_id, trap_info in self.TRAP_DEFINITIONS.items():
            if trap_info["detect"](prompt):
                detected.append({
                    "name": trap_info["name"],
                    "severity": "高" if trap_id in ["over_constraint", "vague"] else "中",
                    "fix": trap_info["fix"](prompt)
                })
        return detected
    
    def get_trap_examples(self, trap_id: str) -> ExamplePair:
        """
        获取指定陷阱的错误示例和修正示例
        
        参数:
            trap_id: 陷阱标识符
        
        返回:
            ExamplePair: 包含错误示例和修正示例
        """
        examples = {
            "over_constraint": ExamplePair(
                bad="请写一篇关于环保的文章，同时要幽默，同时要有数据支撑，同时要引用名人名言，同时要分5段，每段不少于200字，并且要用第一人称，还要押韵。",
                good="请写一篇关于环保的幽默短文，500字左右，分3段，每段包含一个数据。",
                explanation="好例将约束条件从8条精简到4条，去掉了矛盾项"
            ),
            # ... 其他陷阱的示例
        }
        return examples.get(trap_id)
```

---

### 3.6 第5章：进阶技巧

```python
class Chapter5:
    """进阶技巧速通"""
    
    def chain_of_thought(self, problem: str, steps: list[str]) -> Prompt:
        """
        思维链（Chain of Thought）：让AI展示推理过程
        
        参数:
            problem: 需要推理的问题
            steps: 预期的推理步骤（可选，用于引导）
        
        返回:
            Prompt: 包含思维链引导的提示词
        
        伪代码:
            return f"{problem}\n\n请一步步思考。首先，{steps[0]}；然后，{steps[1]}；最后给出答案。"
        """
        if steps:
            step_guide = "请一步步思考。首先，{}；然后，{}；最后给出答案。".format(steps[0], steps[1] if len(steps) > 1 else "得出结论")
        else:
            step_guide = "请一步步思考，并展示你的推理过程。"
        return f"{problem}\n\n{step_guide}"
    
    def few_shot(self, task: str, examples: list[tuple[str, str]], query: str) -> Prompt:
        """
        Few-shot：用示例教会AI格式和逻辑
        
        参数:
            task: 任务描述
            examples: 示例列表，每个是 (输入, 输出)
            query: 实际要处理的输入
        
        返回:
            Prompt: 包含多个示例的提示词
        """
        prompt = task + "\n\n示例：\n"
        for inp, out in examples:
            prompt += f"输入：{inp}\n输出：{out}\n\n"
        prompt += f"现在请处理：\n输入：{query}\n输出："
        return prompt
    
    def self_correction(self, initial_prompt: Prompt, evaluation_criteria: list[str]) -> Prompt:
        """
        自我纠错：让AI检查自己的答案
        
        参数:
            initial_prompt: 初始提示词
            evaluation_criteria: 评价标准列表
        
        返回:
            Prompt: 包含自我纠错指令的增强提示词
        
        伪代码:
            return initial_prompt + f"\n\n生成答案后，请根据以下标准检查：{evaluation_criteria}。如有不符合之处，请修正后再输出最终答案。"
        """
        criteria_str = "、".join(evaluation_criteria)
        correction_instruction = f"\n\n生成答案后，请根据以下标准检查：{criteria_str}。如有不符合之处，请修正后再输出最终答案。"
        return initial_prompt + correction_instruction
    
    def understand_temperature(self, creativity_level: str) -> dict:
        """
        理解温度参数（概念层，不涉及实际API调用）
        
        参数:
            creativity_level: "低" | "中" | "高"
        
        返回:
            dict: 温度参数的概念解释和适用场景
        
        伪代码:
            mapping = {
                "低": {"value": "0.1-0.3", "scenario": "事实问答、代码生成、翻译"},
                "中": {"value": "0.4-0.7", "scenario": "一般对话、写作、摘要"},
                "高": {"value": "0.8-1.0", "scenario": "创意写作、头脑风暴、角色扮演"}
            }
        """
        mapping = {
            "低": {"value": "0.1-0.3", "scenario": "事实问答、代码生成、翻译", "effect": "输出更确定、保守"},
            "中": {"value": "0.4-0.7", "scenario": "一般对话、写作、摘要", "effect": "平衡创造性和准确性"},
            "高": {"value": "0.8-1.0", "scenario": "创意写作、头脑风暴、角色扮演", "effect": "输出更多样、有惊喜感"}
        }
        return mapping.get(creativity_level, mapping["中"])
```

---

### 3.7 第6章：实战项目

```python
class Chapter6:
    """实战项目：从提示词到作品"""
    
    def __init__(self):
        self.projects = []
    
    def project_weekly_report(self) -> Project:
        """
        项目一：用AI写一份高质量工作周报
        
        预估时间：15分钟
        
        返回:
            Project: 包含完整四步流程的项目对象
        """
        def step1_requirement():
            return """
【需求】
- 收集本周完成的任务（用户提供关键词或简单列表）
- 生成结构化的周报
- 包含：完成事项、进行中事项、下周计划、风险与建议
"""
        
        def step2_design():
            return """
【设计提示词（初版）】
你是一位专业的项目经理。请根据以下工作记录，帮我写一份周报。

工作记录：[用户输入]

请按以下格式输出：
【本周完成】
【进行中】
【下周计划】
【风险与建议】
"""
        
        def step3_iteration(initial_output: str, feedback: str) -> str:
            """
            迭代优化：根据反馈修改提示词
            
            参数:
                initial_output: AI的初始输出
                feedback: 用户反馈（如“太啰嗦”、“缺少量化成果”）
            
            返回:
                str: 优化后的提示词
            """
            return f"""
在之前的回答基础上，请根据以下反馈进行修改：
{feedback}

修改后的提示词版本：
"""
        
        def step4_final():
            return """
【成品提示词（优化版）】
你是一位专业的项目经理。请根据以下工作记录，写一份周报。

要求：
1. 【本周完成】每项用一句话概括，并标注成果（如“完成XX报告（已交付）”）
2. 【进行中】标注预计完成时间
3. 【下周计划】列出3-5项，按优先级排序
4. 【风险与建议】如有风险，给出具体应对建议

工作记录：
[用户输入]

请直接输出周报，不要额外说明。
"""
        
        return Project(
            name="工作周报生成器",
            estimatedMinutes=15,
            steps=[
                {"phase": "requirement", "action": step1_requirement},
                {"phase": "design", "action": step2_design},
                {"phase": "iteration", "action": step3_iteration},
                {"phase": "final", "action": step4_final}
            ]
        )
    
    def project_sql_generator(self) -> Project:
        """
        项目二：生成可执行的SQL查询语句
        
        预估时间：20分钟
        """
        # 类似结构，此处省略详细伪代码
        pass
    
    def project_roleplay_game(self) -> Project:
        """
        项目三：设计一个角色对话小游戏
        
        预估时间：25分钟
        """
        # 类似结构，此处省略详细伪代码
        pass
    
    def run_project(self, project_name: str) -> dict:
        """
        执行指定项目
        
        参数:
            project_name: "weekly_report" | "sql_generator" | "roleplay_game"
        
        返回:
            dict: 包含各步骤的输出和最终成品
        """
        projects_map = {
            "weekly_report": self.project_weekly_report,
            "sql_generator": self.project_sql_generator,
            "roleplay_game": self.project_roleplay_game
        }
        project = projects_map[project_name]()
        return {
            "name": project.name,
            "steps": [step["phase"] for step in project.steps],
            "final_output": project.steps[-1]["action"]()
        }
```

---

### 3.8 附录：速查卡

```python
class Appendix:
    """速查卡生成器"""
    
    def generate_cheat_sheet(self) -> str:
        """
        生成一页式速查卡
        
        返回:
            str: 格式化的速查卡文本，可直接打印或截图
        
        内容结构:
            +--------------------------------------------------+
            |              提示词工程速查卡 v1.0               |
            +--------------------------------------------------+
            |                                                  |
            | 【通用公式】                                      |
            | 角色 + 任务 + 细节 + 输出格式                     |
            |                                                  |
            | 【4个核心原则】                                   |
            | 1. 具体  | 2. 无歧义 | 3. 设定角色 | 4. 给出示例  |
            |                                                  |
            | 【6大模板】                                       |
            | 写作 | 分析 | 代码 | 翻译 | 角色扮演 | 创意生成    |
            |                                                  |
            | 【6个陷阱】                                       |
            | ⚠️过度约束 ⚠️模糊指令 ⚠️虚假前提                   |
            | ⚠️遗忘迭代 ⚠️忽视格式 ⚠️角色冲突                    |
            |                                                  |
            | 【快速修正】                                      |
            | 模糊→加数字 | 无角色→加身份 | 无格式→指定结构      |
            +--------------------------------------------------+
        """
        cheat_sheet = """
+--------------------------------------------------+
|              提示词工程速查卡 v1.0               |
+--------------------------------------------------+
|                                                  |
| 【通用公式】                                      |
| 角色 + 任务 + 细节 + 输出格式                     |
|                                                  |
| 示例：你是一位[角色]。请[任务]，要求[细节]，       |
|       按[输出格式]输出。                          |
|                                                  |
| 【4个核心原则】                                   |
| ①具体 → 避免“写一篇文章”                          |
| ②无歧义 → 避免“总结一下”                          |
| ③设定角色 → “你是一位…”                          |
| ④给出示例 → 教AI格式                             |
|                                                  |
| 【6大模板】                                       |
| 📝写作 | 🔍分析 | 💻代码 | 🌐翻译 | 🎭角色扮演 | 💡创意 |
|                                                  |
| 【6个陷阱】                                       |
| ⚠️过度约束 ⚠️模糊指令 ⚠️虚假前提                   |
| ⚠️遗忘迭代 ⚠️忽视格式 ⚠️角色冲突                    |
|                                                  |
| 【快速修正口诀】                                  |
| 模糊加数字，无角加身份，                          |
| 无格加结构，多步要拆分。                          |
+--------------------------------------------------+
"""
        return cheat_sheet
```

---

### 3.9 练习与参考答案模块

```python
class ExerciseSystem:
    """练习系统"""
    
    def get_exercises(self, chapter: int, level: str = "mixed") -> list[dict]:
        """
        获取指定章节的练习题
        
        参数:
            chapter: 章节编号（0-6）
            level: "basic" | "mixed" | "advanced"
        
        返回:
            list[dict]: 练习题列表，每题包含 id, question, type, hint
        """
        exercises_db = {
            1: [
                {"id": "1.1", "question": "请将以下模糊提示词改写为符合通用公式的清晰提示词：'写一个菜谱'", "type": "rewrite", "hint": "缺少角色、细节、格式"},
                {"id": "1.2", "question": "提示词的三要素是什么？", "type": "recall", "hint": "指令、上下文、格式"},
                # ...
            ],
            # 其他章节
        }
        return exercises_db.get(chapter, [])
    
    def get_answer(self, exercise_id: str) -> str:
        """
        获取指定练习题的参考答案
        
        参数:
            exercise_id: 练习题编号，如 "1.1"
        
        返回:
            str: 参考答案
        """
        answers = {
            "1.1": "你是一位专业厨师。请提供一份番茄炒蛋的菜谱，列出食材清单和详细步骤，每步不超过20字。",
            "1.2": "提示词三大要素：1) 指令（告诉AI做什么）；2) 上下文（提供背景信息）；3) 输出格式（指定返回结构）。",
            # ...
        }
        return answers.get(exercise_id, "参考答案待补充")
    
    def self_check(self, chapter: int) -> list[str]:
        """
        生成章节自查清单
        
        参数:
            chapter: 章节编号
        
        返回:
            list[str]: 自查问题列表
        """
        checklists = {
            1: [
                "□ 我能说出提示词的三大要素",
                "□ 我能写出一个包含角色+任务+细节+格式的提示词",
                "□ 我能区分好提示词和差提示词的区别"
            ],
            2: [
                "□ 我能把'写一篇文章'改写成具体的要求",
                "□ 我知道什么时候该设定角色",
                "□ 我能用示例教会AI输出格式"
            ],
            # ...
        }
        return checklists.get(chapter, ["□ 请复习本章内容"])
```

---

## 4. 讲义主入口

```python
class PromptEngineeringHandbook:
    """提示词工程讲义主入口"""
    
    def __init__(self):
        self.ch1 = Chapter1()
        self.ch2 = Chapter2()
        self.ch3 = Chapter3()
        self.ch4 = Chapter4()
        self.ch5 = Chapter5()
        self.ch6 = Chapter6()
        self.appendix = Appendix()
        self.exercises = ExerciseSystem()
    
    def render_chapter(self, chapter_num: int) -> str:
        """
        渲染指定章节为可读文本
        
        参数:
            chapter_num: 0-6
        
        返回:
            str: 章节的完整内容
        """
        chapters = {
            0: "使用指南 + 图标系统",
            1: self.ch1,
            2: self.ch2,
            3: self.ch3,
            4: self.ch4,
            5: self.ch5,
            6: self.ch6
        }
        return f"正在生成第{chapter_num}章内容..."
    
    def export_full_handbook(self, format: str = "markdown") -> str:
        """
        导出完整讲义
        
        参数:
            format: "markdown" | "pdf" | "word"
        
        返回:
            str: 讲义完整内容
        """
        output = []
        output.append("# 提示词工程讲义 v1.0\n")
        output.append(self.render_chapter(0))
        for i in range(1, 7):
            output.append(self.render_chapter(i))
        output.append(self.appendix.generate_cheat_sheet())
        output.append("\n# 参考答案\n")
        # 添加所有参考答案
        return "\n\n".join(output)


# 使用示例
if __name__ == "__main__":
    handbook = PromptEngineeringHandbook()
    
    # 获取一个模板
    template = handbook.ch3.writing_template("邮件", "项目进度汇报", "正式", "短")
    print(template)
    
    # 检测陷阱
    bad_prompt = "帮我写一些关于AI的东西"
    traps = handbook.ch4.detect_traps(bad_prompt)
    print(traps)
    
    # 生成速查卡
    cheat_sheet = handbook.appendix.generate_cheat_sheet()
    print(cheat_sheet)