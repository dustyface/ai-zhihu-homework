from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer


def build_prompt(prompt_template, **kwargs):
    """根据kwargs key-value pair, 替换prompt_template的占位符"""
    prompt = prompt_template
    for k, v in kwargs.items():
        if isinstance(v, str):
            val = v
        elif isinstance(v, list) and all(isinstance(item, str) for item in v):
            val = "\n".join(v)
        else:
            val = str(v)
        prompt = prompt.replace(f"__{k.upper()}__", val)
    print("built prompt=", prompt)
    return prompt


prompt_template = """
你是一个问答机器人。
你的任务是根据下述给定的已知信息回答用户问题。
确保你的回复完全依据下述已知信息。不要编造答案。
如果下述已知信息不足以回答用户的问题，请直接回复"我无法回答您的问题"。

已知信息:
__INFO__

用户问：
__QUERY__

请用中文回答用户问题。
"""


# python知识点和pdfminer相关，参考: https://f7dmbpckkt.feishu.cn/wiki/Y93Iw7ljfibZmlkRdoDcZ8oEnPb#part-X2P7dYlaQodcb9xzikCcZ5tJn5f
def extract_text_from_pdf(filename, page_numbers=None, min_line_length=1):
    paragraphs = []
    buffer = ""
    full_text = ""
    for i, page_layout in enumerate(extract_pages(filename)):
        if page_numbers is not None and i not in page_numbers:
            continue
        for element in page_layout:
            # 如果element是LTTextContainer的实例，即element是一个段落
            if isinstance(element, LTTextContainer):
                full_text += element.get_text() + "\n"
    lines = full_text.split("\n")
    for text in lines:
        # 区分段落的逻辑如下:
        # 1. 形成一段: 当line的内容大于min_line_length时，认为这是一段中的内容，不断的加到buffer中;
        # 2. 一段的结束: 当line的内容，小于min_line_length时，认为这段是上一段最后一line，将line加到buffer，添加一个paragraph
        # bug: 依据min_line_length来分段，是可能存在问题的，
        # e.g. 当一段的最后一行，其文字长度超过min_line_length时，会导致2段的合并;
        if len(text) >= min_line_length:
            buffer += (" " + text) if not text.endswith("-") else text.strip("-")
        elif buffer:
            paragraphs.append(buffer)
            buffer = ""
        else:  # bugfix: 当text < min_line_length, 且buffer为空，说明这是一段的开始，直接将text加到buffer中
            paragraphs.append(text)
    if buffer:
        paragraphs.append(buffer)
    return paragraphs


# filename的默认路径是从python -m认为的cwd路径开始;
# paragraphs = extract_text_from_pdf(
#     "zhihu_ai_homework/RAG/llama2-test-1-4.pdf", min_line_length=10
# )

# for para in paragraphs[0:3]:
#     print(para + "\n")
