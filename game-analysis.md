# 文字冒险游戏分析报告

## 一、游戏引擎状态分析

### 1.1 显式状态（`self.state`）

| 状态 | 常量名 | 说明 |
|------|--------|------|
| `name_input` | `STATE_NAME_INPUT` | 名字输入界面 |
| `playing` | `STATE_PLAYING` | 游戏进行中（场景浏览） |
| `game_over` | `STATE_GAME_OVER` | 失败/普通结局界面 |
| `victory` | `STATE_VICTORY` | 胜利/良好/完美结局界面 |

### 1.2 隐式状态（附加标志）

| 隐式状态 | 相关变量 | 说明 |
|----------|----------|------|
| 空名字警告显示中 | `empty_name_warning = True` | 玩家尝试用空名字开始游戏时触发，持续 2 秒 |
| 空名字警告已过期 | `empty_name_warning = False` | 警告显示完毕后恢复 |
| 有玩家名字 | `player_name != ""` | 已完成名字输入 |
| 无玩家名字 | `player_name = ""` | 未输入名字或退出游戏后重置 |

### 1.3 状态转换图

```mermaid
stateDiagram-v2
    [*] --> NAME_INPUT : 游戏启动
    NAME_INPUT --> NAME_INPUT : 按回车但名字为空\n(触发空名字警告)
    NAME_INPUT --> PLAYING : 按回车且名字非空
    PLAYING --> PLAYING : 选择普通选项(next)
    PLAYING --> VICTORY : 选择 perfect/victory/good 结局
    PLAYING --> GAME_OVER : 选择 neutral/bad 结局
    VICTORY --> NAME_INPUT : 点击"重新开始"或"退出游戏"
    GAME_OVER --> NAME_INPUT : 点击"重新开始"或"退出游戏"
    
    note right of NAME_INPUT
        隐式子状态:
        - empty_name_warning:
          True → False (2秒后自动)
    end_note
```

### 1.4 状态转换条件详细说明

| 当前状态 | 事件 | 条件 | 目标状态 | 代码位置 |
|----------|------|------|----------|----------|
| `name_input` | 按 Enter 键 | `name == ""` | `name_input`（保持） | `engine.py:247-251` |
| `name_input` | 按 Enter 键 | `name != ""` | `playing` | `engine.py:242-246` |
| `playing` | 点击选项 | `option["next"]` 存在且非 `restart`/`quit` | `playing`（换场景） | `engine.py:288-290` |
| `playing` | 点击选项 | `option["ending"]` 为 `perfect`/`victory`/`good` | `victory` | `engine.py:269-271, 202-203` |
| `playing` | 点击选项 | `option["ending"]` 为 `neutral`/`bad` | `game_over` | `engine.py:269-271, 204-205` |
| `victory` | 点击"重新开始" | `next == "restart"` | `name_input` | `engine.py:274-279` |
| `victory` | 点击"退出游戏" | `next == "quit"` | `name_input` | `engine.py:280-287` |
| `game_over` | 点击"重新开始" | `next == "restart"` | `name_input` | `engine.py:274-279` |
| `game_over` | 点击"退出游戏" | `next == "quit"` | `name_input` | `engine.py:280-287` |

### 1.5 不可达状态与死锁分析

**结论：不存在不可达状态，也不存在死锁状态。**

**理由：**
- 所有 4 个显式状态（`name_input`、`playing`、`game_over`、`victory`）都有明确的可达路径
- `game_over` 和 `victory` 都可以通过"重新开始"或"退出游戏"回到 `name_input`，形成闭环
- `playing` 中的所有场景最终都会指向结局或其他场景，不会卡在某个状态无法退出
- 唯一的循环场景（如 `start` → `wait` → `start`）也可以通过其他分支离开，不会形成强制死锁

---

## 二、剧情有向图分析

### 2.1 场景节点清单

STORY 字典共包含 **26 个场景节点**：

```
start, village, deep_forest, wait, accept_quest, ask_info, leave_village,
get_sword, observe, escape_forest, fairy_help, light_well, jump_well,
shout_well, ask_weapon, attack_wolf, retreat_wolf, talk_wolf, help_deer,
ignore_deer, well_cleared, escape_monster, with_key, sneak_cave, wolf_ally,
ask_stone, hidden_path, village_with_orb, well_with_orb, temple, explore_temple,
read_book, take_book
```

### 2.2 可达性分析

**结论：从 `start` 节点出发，所有场景节点均可达，不存在孤岛节点。**

**验证：**
- 直接可达：`village`、`deep_forest`、`wait`（来自 `start`）
- 间接可达：所有其他节点都通过 `village`、`deep_forest` 或 `wait` 的后续分支可达
- 反向可达：部分节点通过 `next: "start"` 可以回到起点（如 `wait` → `start`、`escape_forest` → `start`、`take_book` → `start`）

### 2.3 最短路径分析（BFS 算法）

**注：** 路径长度 = 场景转移次数（从 start 到结局的边数）

#### perfect 结局

| 路径 | 场景序列 | 长度 |
|------|----------|------|
| 路径 1 | start → deep_forest → get_sword → attack_wolf → with_key → temple → perfect | **5** |
| 路径 2 | start → deep_forest → get_sword → talk_wolf → wolf_ally → village_with_orb → well_with_orb → perfect | 6 |
| 路径 3 | start → deep_forest → get_sword → attack_wolf → with_key → temple → explore_temple → perfect | 6 |

**最短路径（长度 5）：**
`start → deep_forest → get_sword → attack_wolf → with_key → temple → [取石得 perfect]`

#### victory 结局

| 路径 | 场景序列 | 长度 |
|------|----------|------|
| 路径 1 | start → village → accept_quest → light_well → victory | **3** |
| 路径 2 | start → village → ask_info → accept_quest → light_well → victory | 4 |

**最短路径（长度 3）：**
`start → village → accept_quest → light_well → [取石得 victory]`

#### good 结局

| 路径 | 场景序列 | 长度 |
|------|----------|------|
| 路径 1 | start → village → accept_quest → light_well → well_cleared → good | **4** |

**最短路径（长度 4）：**
`start → village → accept_quest → light_well → well_cleared → good`

#### neutral 结局

| 路径 | 场景序列 | 长度 |
|------|----------|------|
| 路径 1 | start → village → leave_village → neutral | **2** |
| 路径 2 | start → village → accept_quest → shout_well → escape_monster → neutral | 4 |

**最短路径（长度 2）：**
`start → village → leave_village → neutral`

#### bad 结局

| 路径 | 场景序列 | 长度 |
|------|----------|------|
| 路径 1 | start → village → accept_quest → jump_well → bad | **3** |
| 路径 2 | start → deep_forest → observe → ignore_deer → bad | **3** |

**最短路径（长度 3）：**
- `start → village → accept_quest → jump_well → bad`
- `start → deep_forest → observe → ignore_deer → bad`

### 2.4 各结局最短路径汇总表

| 结局类型 | 最短路径长度 | 最短路径数 | 最短路径示例 |
|----------|--------------|------------|--------------|
| perfect | 5 | 1 | start → deep_forest → get_sword → attack_wolf → with_key → temple → perfect |
| victory | 3 | 1 | start → village → accept_quest → light_well → victory |
| good | 4 | 1 | start → village → accept_quest → light_well → well_cleared → good |
| neutral | 2 | 1 | start → village → leave_village → neutral |
| bad | 3 | 2 | start → village → accept_quest → jump_well → bad<br>start → deep_forest → observe → ignore_deer → bad |

---

## 三、数据结构扩展方案

### 3.1 扩展需求分析

当前数据结构的局限性：
1. 场景文本固定，无法根据玩家状态动态变化
2. 选项总是全部显示，无法根据条件隐藏
3. 不支持道具/标记系统
4. 无法记录玩家的历史选择

### 3.2 扩展后的数据结构（JSON Schema）

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Extended Text Adventure Game Schema",
  "type": "object",
  "properties": {
    "STORY": {
      "type": "object",
      "patternProperties": {
        "^[a-z_]+$": {
          "type": "object",
          "properties": {
            "text": {
              "type": [
                "string",
                "object"
              ],
              "description": "场景文本。支持字符串或条件文本对象"
            },
            "conditional_texts": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "condition": {
                    "$ref": "#/definitions/condition"
                  },
                  "text": {
                    "type": "string"
                  }
                },
                "required": ["condition", "text"]
              },
              "description": "条件文本列表，按顺序检查，第一个满足条件的文本与默认文本拼接"
            },
            "options": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "text": {
                    "type": "string",
                    "description": "选项显示文本"
                  },
                  "next": {
                    "type": "string",
                    "description": "下一个场景ID"
                  },
                  "ending": {
                    "type": "string",
                    "enum": ["perfect", "victory", "good", "neutral", "bad"],
                    "description": "结局类型"
                  },
                  "condition": {
                    "$ref": "#/definitions/condition",
                    "description": "选项显示条件，不满足则隐藏"
                  },
                  "actions": {
                    "type": "array",
                    "items": {
                      "$ref": "#/definitions/action"
                    },
                    "description": "选择此选项时执行的动作列表"
                  }
                },
                "oneOf": [
                  { "required": ["text", "next"] },
                  { "required": ["text", "ending"] }
                ]
              }
            },
            "on_enter": {
              "type": "array",
              "items": {
                "$ref": "#/definitions/action"
              },
              "description": "进入场景时执行的动作"
            }
          },
          "required": ["text", "options"]
        }
      }
    },
    "ENDINGS": {
      "type": "object",
      "patternProperties": {
        "^[a-z_]+$": {
          "type": "object",
          "properties": {
            "title": { "type": "string" },
            "text": { "type": "string" }
          },
          "required": ["title", "text"]
        }
      }
    }
  },
  "definitions": {
    "condition": {
      "type": "object",
      "oneOf": [
        {
          "properties": {
            "type": { "const": "has_flag" },
            "flag": { "type": "string" }
          },
          "required": ["type", "flag"]
        },
        {
          "properties": {
            "type": { "const": "not_flag" },
            "flag": { "type": "string" }
          },
          "required": ["type", "flag"]
        },
        {
          "properties": {
            "type": { "const": "has_item" },
            "item": { "type": "string" }
          },
          "required": ["type", "item"]
        },
        {
          "properties": {
            "type": { "const": "not_item" },
            "item": { "type": "string" }
          },
          "required": ["type", "item"]
        },
        {
          "properties": {
            "type": { "const": "choice_made" },
            "scene": { "type": "string" },
            "option": { "type": "string" }
          },
          "required": ["type", "scene", "option"]
        },
        {
          "properties": {
            "type": { "const": "and" },
            "conditions": {
              "type": "array",
              "items": { "$ref": "#/definitions/condition" }
            }
          },
          "required": ["type", "conditions"]
        },
        {
          "properties": {
            "type": { "const": "or" },
            "conditions": {
              "type": "array",
              "items": { "$ref": "#/definitions/condition" }
            }
          },
          "required": ["type", "conditions"]
        }
      ]
    },
    "action": {
      "type": "object",
      "oneOf": [
        {
          "properties": {
            "type": { "const": "set_flag" },
            "flag": { "type": "string" }
          },
          "required": ["type", "flag"]
        },
        {
          "properties": {
            "type": { "const": "clear_flag" },
            "flag": { "type": "string" }
          },
          "required": ["type", "flag"]
        },
        {
          "properties": {
            "type": { "const": "add_item" },
            "item": { "type": "string" }
          },
          "required": ["type", "item"]
        },
        {
          "properties": {
            "type": { "const": "remove_item" },
            "item": { "type": "string" }
          },
          "required": ["type", "item"]
        },
        {
          "properties": {
            "type": { "const": "record_choice" },
            "scene": { "type": "string" },
            "option": { "type": "string" }
          },
          "required": ["type", "scene", "option"]
        }
      ]
    }
  }
}
```

### 3.3 扩展场景示例

```python
STORY = {
    "forest_entrance": {
        "text": "你站在森林入口处。",
        "conditional_texts": [
            {
                "condition": {"type": "has_flag", "flag": "visited_forest"},
                "text": "\n你对这里已经很熟悉了。"
            },
            {
                "condition": {"type": "has_item", "item": "sword"},
                "text": "\n你手中的剑微微发光。"
            }
        ],
        "on_enter": [
            {"type": "set_flag", "flag": "visited_forest"}
        ],
        "options": [
            {
                "text": "进入森林",
                "next": "deep_forest",
                "actions": [
                    {"type": "record_choice", "scene": "forest_entrance", "option": "enter"}
                ]
            },
            {
                "text": "返回村庄",
                "next": "village"
            },
            {
                "text": "用剑劈开挡路的荆棘",
                "next": "secret_path",
                "condition": {"type": "has_item", "item": "sword"},
                "actions": [
                    {"type": "remove_item", "item": "old_sword"},
                    {"type": "add_item", "item": "shiny_sword"}
                ]
            },
            {
                "text": "向守卫出示通行证",
                "next": "guarded_area",
                "condition": {
                    "type": "and",
                    "conditions": [
                        {"type": "has_item", "item": "pass"},
                        {"type": "not_flag", "flag": "pass_used"}
                    ]
                },
                "actions": [
                    {"type": "set_flag", "flag": "pass_used"}
                ]
            }
        ]
    },
    "treasure_room": {
        "text": "你发现了一个宝藏房间！",
        "conditional_texts": [
            {
                "condition": {"type": "choice_made", "scene": "forest_entrance", "option": "enter"},
                "text": "\n因为你选择了直接进入森林，所以你发现了这个秘密房间！"
            }
        ],
        "options": [
            {
                "text": "拿走宝藏",
                "ending": "perfect",
                "actions": [
                    {"type": "add_item", "item": "treasure"}
                ]
            },
            {
                "text": "离开",
                "next": "forest_entrance"
            }
        ]
    }
}
```

### 3.4 引擎修改方案

需要在 `engine.py` 中进行以下修改：

#### 1. 新增状态变量（`__init__` 方法）

```python
# 在 __init__ 中添加
self.flags = set()           # 标记集合
self.inventory = set()       # 背包
self.choice_history = {}     # 选择历史: {scene_id: option_index}
```

#### 2. 新增条件评估方法

```python
def _evaluate_condition(self, condition):
    """
    评估条件表达式
    
    Args:
        condition: 条件对象
        
    Returns:
        bool: 条件是否满足
    """
    if not condition:
        return True
    
    cond_type = condition["type"]
    
    if cond_type == "has_flag":
        return condition["flag"] in self.flags
    elif cond_type == "not_flag":
        return condition["flag"] not in self.flags
    elif cond_type == "has_item":
        return condition["item"] in self.inventory
    elif cond_type == "not_item":
        return condition["item"] not in self.inventory
    elif cond_type == "choice_made":
        return self.choice_history.get(condition["scene"]) == condition["option"]
    elif cond_type == "and":
        return all(self._evaluate_condition(c) for c in condition["conditions"])
    elif cond_type == "or":
        return any(self._evaluate_condition(c) for c in condition["conditions"])
    
    return False
```

#### 3. 新增动作执行方法

```python
def _execute_action(self, action):
    """
    执行动作
    
    Args:
        action: 动作对象
    """
    action_type = action["type"]
    
    if action_type == "set_flag":
        self.flags.add(action["flag"])
    elif action_type == "clear_flag":
        self.flags.discard(action["flag"])
    elif action_type == "add_item":
        self.inventory.add(action["item"])
    elif action_type == "remove_item":
        self.inventory.discard(action["item"])
    elif action_type == "record_choice":
        self.choice_history[action["scene"]] = action["option"]
```

#### 4. 修改 `_load_scene` 方法（`engine.py:143-160`）

```python
def _load_scene(self, scene_id):
    if scene_id not in STORY:
        logger.error(f"场景不存在: {scene_id}，回退到起始场景")
        scene_id = "start"
    
    scene = STORY[scene_id]
    
    # 执行 on_enter 动作
    if "on_enter" in scene:
        for action in scene["on_enter"]:
            self._execute_action(action)
    
    # 构建场景文本
    text = scene["text"].replace("{player}", self.player_name)
    
    # 追加条件文本
    if "conditional_texts" in scene:
        for cond_text in scene["conditional_texts"]:
            if self._evaluate_condition(cond_text["condition"]):
                text += cond_text["text"]
    
    self.story_box.set_text(text)
    
    # 根据条件过滤选项
    filtered_options = []
    for option in scene["options"]:
        if self._evaluate_condition(option.get("condition")):
            filtered_options.append(option)
    
    self._create_option_boxes(filtered_options)
    self.current_scene = scene_id
    logger.info(f"玩家 [{self.player_name}] 进入场景: {scene_id}")
```

#### 5. 修改 `_handle_option_click` 方法（`engine.py:260-290`）

```python
def _handle_option_click(self, option_data):
    logger.info(f"玩家 [{self.player_name}] 选择: {option_data.get('text', option_data)}")
    
    # 执行选项动作
    if "actions" in option_data:
        for action in option_data["actions"]:
            self._execute_action(action)
    
    if "ending" in option_data:
        self._show_ending(option_data["ending"])
    elif "next" in option_data:
        next_scene = option_data["next"]
        if next_scene == "restart":
            # 重新开始时重置所有状态
            self.flags.clear()
            self.inventory.clear()
            self.choice_history.clear()
            self.state = STATE_NAME_INPUT
            self.name_input.text = ""
            self.current_scene = "start"
            self.option_boxes = []
        elif next_scene == "quit":
            self.flags.clear()
            self.inventory.clear()
            self.choice_history.clear()
            logger.info(f"玩家 [{self.player_name}] 退出游戏")
            self.state = STATE_NAME_INPUT
            self.name_input.text = ""
            self.player_name = ""
            self.current_scene = "start"
            self.option_boxes = []
        else:
            self._load_scene(next_scene)
```

### 3.5 扩展后新增能力总结

| 能力 | 实现方式 |
|------|----------|
| 条件选项显示/隐藏 | 通过 `option["condition"]` + `_evaluate_condition()` |
| 道具获取与检查 | `self.inventory` + `add_item`/`has_item` |
| 标记获取与检查 | `self.flags` + `set_flag`/`has_flag` |
| 历史选择记录 | `self.choice_history` + `record_choice`/`choice_made` |
| 动态场景文本 | `conditional_texts` 数组，按条件追加文本 |
| 进入场景自动执行 | `on_enter` 动作列表 |
| 选择选项自动执行 | `option["actions"]` 列表 |
| 复合条件 | `and`/`or` 条件组合 |
