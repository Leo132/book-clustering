print("Importing ckiptagger...")
from ckiptagger import data_utils, WS

# Downloads to ./data.zip (2GB) and extracts to ./data/
print("Downloading model...")
data_utils.download_data_url("./") # iis-ckip
data_utils.download_data_gdown("./model/") # gdrive-ckip

# To use GPU:
#    1. Install tensorflow-gpu (see Installation)
#    2. Set CUDA_VISIBLE_DEVICES environment variable, e.g. os.environ["CUDA_VISIBLE_DEVICES"] = "0"
#    3. Set disable_cuda=False, e.g. ws = WS("./data", disable_cuda=False)
# To use CPU:
print("Loading model...")
ws = WS("./model/data")

search_str = [
    "法律概論",
]

word_list = ws(
    search_str,
    # sentence_segmentation = True, # To consider delimiters
    # segment_delimiter_set = {",", "。", ":", "?", "!", ";"}), # This is the defualt set of delimiters
    # recommend_dictionary = dictionary1, # words in this dictionary are encouraged
    # coerce_dictionary = dictionary2, # words in this dictionary are forced
)[0]
del ws

print(f"{search_str=}, {word_list=}")