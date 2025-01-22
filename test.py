# from transformers import LayoutLMTokenizer, LayoutLMForTokenClassification
# from pdfminer.high_level import extract_text
# from transformers import LayoutLMv3TokenizerFast
# from api.json_helper import gen_input
# text = extract_text('sample.pdf')
# model_name = "microsoft/layoutlmv2-base-uncased"
# # model_name = "microsoft/layoutlmv3-base"
# tokenizer = LayoutLMTokenizer.from_pretrained(model_name)
# # tokenizer = LayoutLMv3TokenizerFast.from_pretrained(model_name)
# model = LayoutLMForTokenClassification.from_pretrained(model_name, num_labels=10)  # Adjust num_labels for your task
# # tokens = tokenizer.tokenize(text)
# # char_offsets = []
# # current_pos = 0
# # for token in tokens:
# #     start_pos = text.find(token.replace("##", ""), current_pos)
# #     end_pos = start_pos + len(token.replace("##", ""))
# #     char_offsets.append((start_pos, end_pos))
# #     current_pos = end_pos
# encoding = tokenizer(
#     text.split(),  # Split text into tokens
#     return_offsets_mapping=True,  # Get token offset mapping
#     truncation=True,
#     padding = True,
#     max_length=512,  # Adjust if needed
#     return_tensors="pt"
# )
# dummy_bboxes = [[0, 0, 100, 100]] * len(encoding["input_ids"][0])
# encoding["bbox"] = dummy_bboxes
# # encoding["offset_mapping"] = char_offsets 
# outputs = model(**encoding)
# # Get predictions (logits) and convert to labels
# logits = outputs.logits
# predicted_classes = logits.argmax(dim=-1).squeeze().tolist()
# #map prediction to class

from extractor_core.main import parse_data
from helper import process_parsed_data

cur = parse_data("sample_2.pdf")
data = process_parsed_data(cur)
print(data)
print(type(data))

