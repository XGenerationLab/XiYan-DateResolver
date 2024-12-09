# DateResolver
a date understanding and reasoning enhanced model
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
