from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer


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
paragraphs = extract_text_from_pdf(
    "zhihu_ai_homework/RAG/llama2-test-1-4.pdf", min_line_length=10
)

# for para in paragraphs[0:3]:
#     print(para + "\n")
