---
frameworks:
- Pytorch
license: Apache License 2.0
tasks:
- nli

#model-type:
##如 gpt、phi、llama、chatglm、baichuan 等
#- gpt

#domain:
##如 nlp、cv、audio、multi-modal
#- nlp

#language:
##语言代码列表 https://help.aliyun.com/document_detail/215387.html?spm=a2c4g.11186623.0.0.9f8d7467kni6Aa
#- cn

#metrics:
##如 CIDEr、Blue、ROUGE 等
#- CIDEr

#tags:
##各种自定义，包括 pretrained、fine-tuned、instruction-tuned、RL-tuned 等训练方法和其他
#- pretrained

#tools:
##如 vllm、fastchat、llamacpp、AdaSeq 等
#- vllm
base_model:
  - Qwen/Qwen2-7B-Instruct
---
# 日期推理介绍
为了解决通用大模型在时间感知方面所面临的挑战，我们开发了一套解析处理文本中的时间和日期信息的流程，并将其转换为准确的真实时间。在覆盖的时间范围内实现了超过95%的准确率，支持包括年月日、周、季度、半年及时间段等在内的100多种时间表达方式。

Case：（假设今天为2024年12月6日，星期五）

输入：上周三的销量是多少？

输出：上周三=2024年11月27日。

输入：公司在不包含今天的近三天内处理的订单数有多少？

输出：不包含今天的近三天=2024年12月3日至2024年12月5日。

## 模型描述
模型文件中包含基于Qwen2-7B-Instruct微调的checkpoint，用于抽取日期并转化为特定格式。

Case:

输入：本年度的销量是多少？

模型输出：['今年']

输入：上周周五比周三的订单数多多少？

模型输出：['上周星期5', '上周星期3']

日期后处理脚本 "date.py"，用于将模型输出的日期转化为真实时间。

Case：（假设今天为2024年12月6日，星期五）

输入：['今年']

输出：'今年=2024年'

输入：['上周星期5', '上周星期3']

输出：'上周星期5=2024年11月29日'，'上周星期3=2024年11月27日'

## 使用方式
需要在“模型文件”中下载date.py文件
```python
from modelscope import AutoModelForCausalLM, AutoTokenizer
import ast
from date import DateTimeUtil
device = "cuda"

model = AutoModelForCausalLM.from_pretrained(
    "XGenerationLab/DateResolver-Qwen2-7B-Instruct",
    torch_dtype="auto",
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained("XGenerationLab/DateResolver-Qwen2-7B-Instruct")

prompt = "给你一个用户的问题，请你提取出该用户所提问的时间，结果以list格式输出。\n\n【用户问题】\n上周三和上周五的销量是多少？\n\n【回答】\n"
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
list_output = ast.literal_eval(response)

DateTimeUtil.run(list_output)
```


## 适用范围
| 表达式   |表达式|表达式|
|--------|--------|------|
|{%4d}年{%2d}月{%2d}日|{%4d}年{%2d}月|去年上半年
|今年{%2d}月{%2d}日|今年{%2d}月|去年下半年
|去年{%2d}月{%2d}日|去年{%2d}月|上半年
|前年{%2d}月{%2d}日|前年{%2d}月|下半年
|明年{%2d}月{%2d}日|明年{%2d}月|{%4d}年第{%d}季度
|后年{%2d}月{%2d}日|后年{%2d}月|今年第{%d}季度
|本月{%2d}日|本月|去年第{%d}季度
|上月{%2d}日|上月|前年第{%d}季度
|上上月{%2d}日|上上月|明年第{%d}季度
|下月{%2d}日|下月|后年第{%d}季度
|上月今天|去年本月|本季度
|上上月今天|{%4d}年|上季度
|今天|今年|下季度
|昨天|去年|去年本季度
|前天|前年|本周星期{%1d}
|明天|明年|上周星期{%1d}
|后天|后年|上上周星期{%1d}
|本周第{%d}天|{%4d}年上半年|下周星期{%1d}
|本月最后一天|{%4d}年下半年|下下周星期{%1d}
|上月最后一天|今年上半年|本周
|今年{%2d}月最后一天|今年下半年|上周
|上上周|下周|下下周

| 表达式   |解释|
|--------|--------|
|{%4d}年第{%2d}周|	每年的第一周都是1月1日-1月7日，不论1月1日是周几，如果想从周一开始算输入完整周。2023年第01周是2023年1月1日至2023年1月7日
|今年第{%2d}周|	今年第02周
|去年第{%2d}周|	去年第02周
|前年第{%2d}周|	前年第02周
|本月第{%1d}周|	每月的第一周都是本月1日-本月7日，不论本月1日是周几，如果想从周一开始算输入完整周。例如今天是2024年8月10日，本月第1周是2024年8月1日至2024年8月7日
|上月第{%1d}周|	上月第1周
|{%4d}年{%2d}月最后一周	|计算某年某月最后一周时从这个月的最后一个星期一开始算，不超过本月的范围，2024年8月最后一周是2024年8月26日至2024年8月31日
|本月最后一周|	本月最后一周
|上月最后一周|	上月最后一周
|上上月最后一周|	上上月最后一周
|{%4d}年{%2d}月第{%1d}周|	2024年08月第1周是2024年8月1日至2024年8月7日
|今年{%2d}月第{%1d}周|	今年08月第1周
|去年{%2d}月第{%1d}周|	去年08月第1周
|前年{%2d}月第{%1d}周|	前年08月第1周
|{%4d}年{%2d}月第{%1d}个完整周|某年某月第某个完整周是从周一开始计算到周日，2024年08月第1个完整周是2024年8月5日至8月11日
|今年{%2d}月第{%1d}个完整周	|今年08月第1个完整周
|去年{%2d}月第{%1d}个完整周|	去年08月第1个完整周
|前年{%2d}月第{%1d}个完整周|	前年08月第1个完整周
|{%4d}年第{%1d}个完整周	|某年第某个完整周是从周一开始计算到周日，2023年第01个完整周是指2023年1月2日至2023年1月8日
|今年第{%2d}个完整周|	今年第01个完整周
|去年第{%2d}个完整周|	去年第01个完整周
|前年第{%2d}个完整周|	前年第01个完整周
|本月第{%1d}个完整周|	本月第1个完整周
|上月第{%1d}个完整周|	上月第1个完整周
|本月最后一个完整周|	假设今天是2024年8月10日，本月最后一个完整周是2024年8月19日至2024年8月25日
|上月最后一个完整周|	上月最后一个完整周
|上上月最后一个完整周|	上上月最后一个完整周
|近{\d+}年|	近1年是指2023年7月19日至2024年7月19日
|近{\d+}个月|	近2个月是指2024年5月19日至2024年7月19日
|近{\d+}周|	近1周是指2024年7月12日至2024年7月19日
|近{\d+}天|	近3天是指2024年7月16日至2024年7月19日，其实是三天半，因为今天还没有过完，但是由于数据只到Date级别，没有Time，所以只能多取，如果不想包含今天，可以使用“不包含今天的近{\d+}天”
|近{\d+}个完整年	|近2个完整年是指2022年1月1日至2023年12月31日
|近{\d+}个完整季度|	近2个完整季度是指2024年1月1日至2024年6月30日
|近{\d+}个完整月|	近1个完整月是指2024年6月1日至2024年6月30日
|近{\d+}个完整周|	近1个完整周是指2024年7月8日至2024年7月14日，从周一开始计算
|不包含今天的近{\d+}天|	不包含今天的近3天是指2024年7月16日至2024年7月18日
|包含当前季度的近{\d+}个季度|	包含当前季度的近3个季度是指2024年1月1日至2024年9月30日

