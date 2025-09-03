# XiYan-DateResolver
为了解决通用大模型在时间感知方面所面临的挑战，我们开发了一套解析处理文本中的时间和日期信息的流程XiYan-DateResolver，并将其转换为准确的真实时间。在覆盖的时间范围内实现了超过95%的准确率，支持包括年、月、日、周、季度、半年及时间段等在内的100多种时间表达方式。

示例：（假设今天为2024年12月6日，星期五）

```python
输入：上周三的销量是多少？
输出：上周星期3=2024年11月27日。

输入：公司在不包含今天的近三天内处理的订单数有多少？
输出：不包含今天的近3天=2024年12月3日至2024年12月5日。
```

## 流程介绍

XiYan-DateResolver包含以下两个步骤：

### 1、时间表达式抽取

模型文件：基于`Qwen2-7B-Instruct`微调的checkpoint，用于从输入的文本中抽取时间表达式，并将其转化成本方案定义的标准格式。

模型地址：[ModelScope](https://www.modelscope.cn/models/XGenerationLab/DateResolver-Qwen2-7B-Instruct)

示例：

```python
输入：本年度的销量是多少？
模型输出：["今年"]

输入：上周周五比周三的订单数多多少？
模型输出：["上周星期5", "上周星期3"]
```


### 2、时间表达式推理

日期后处理脚本`date_convert.py`，自动获取当前日期，完成从标准的时间表达式到真实时间的推理。

示例：（假设今天为2024年12月6日，星期五）

```python
输入：["今年"]
输出：["今年=2024年"]

输入：["上周星期5", "上周星期3"]
输出：["上周星期5=2024年11月29日", "上周星期3=2024年11月27日"]
```

## Requirements
* python>=3.9
* transformers>4.37.0
* modelscope>=1.17.0

## 使用方式
### 1、时间表达式抽取

首先从modelscope加载模型：
```python
from modelscope import AutoModelForCausalLM, AutoTokenizer
device = "cuda"

model_name = "XGenerationLab/DateResolver-Qwen2-7B-Instruct"
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained(model_name)
```

LLM从输入的文本中解析出时间表达式：
```python
question = "上周三和上周五的销量是多少？"
prompt = "给你一个用户的问题，请你提取出该用户所提问的时间，结果以list格式输出。\n\n【用户问题】\n{question}\n\n【回答】\n".format(question=question)
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": prompt}
]
text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True
)
model_inputs = tokenizer([text], return_tensors="pt").to(device)

generated_ids = model.generate(
    model_inputs.input_ids,
    max_new_tokens=512
)
generated_ids = [
    output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
]

response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
list_output = eval(response)
```

### 2、时间表达式推理
```python
from date_convert import DateTimeUtil
DateTimeUtil.run(list_output)
```

## 适用范围

+ 语言：中文为主
+ 时间表达式：一百多种常用的时间表达式，完整的时间表达式列表及对应的计算逻辑请查看：[时间表达式](https://github.com/XGenerationLab/XiYan-DateResolver/blob/main/%E6%97%B6%E9%97%B4%E8%A1%A8%E8%BE%BE%E5%BC%8F.xlsx)


## 联系我们:

如果您对我们的研究或产品感兴趣，请随时联系我们。

#### Contact Information:

刘义富, zhencang.lyf@alibaba-inc.com

#### Join Our DingTalk Group

<a href="https://github.com/XGenerationLab/XiYan-SQL/blob/main/xiyansql_dingding.png">Ding Group钉钉群</a> 




更多XiYan-SQL相关内容请访问：https://github.com/XGenerationLab/XiYan-SQL
