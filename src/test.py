from ckiptagger import data_utils, construct_dictionary, WS, POS, NER

# Downloads to ./data.zip (2GB) and extracts to ./data/
# data_utils.download_data_url("./") # iis-ckip
# data_utils.download_data_gdown("./model/") # gdrive-ckip

# To use GPU:
#    1. Install tensorflow-gpu (see Installation)
#    2. Set CUDA_VISIBLE_DEVICES environment variable, e.g. os.environ["CUDA_VISIBLE_DEVICES"] = "0"
#    3. Set disable_cuda=False, e.g. ws = WS("./data", disable_cuda=False)
# To use CPU:
ws = WS("./model/data")
# pos = POS("./model/data")
# ner = NER("./model/data")

sentence_list = [
    "傅達仁今將執行安樂死，卻突然爆出自己20年前遭緯來體育台封殺，他不懂自己哪裡得罪到電視台。",
    "美國參議院針對今天總統布什所提名的勞工部長趙小蘭展開認可聽證會，預料她將會很順利通過參議院支持，成為該國有史以來第一位的華裔女性內閣成員。",
    "",
    "土地公有政策?？還是土地婆有政策。.",
    "… 你確定嗎… 不要再騙了……",
    "最多容納59,000個人,或5.9萬人,再多就不行了.這是環評的結論.",
    "科長說:1,坪數對人數為1:3。2,可以再增加。",
]
search_str = [
    "法律概論",
]

word_sentence_list = ws(
    # sentence_list,
    search_str,
    # sentence_segmentation = True, # To consider delimiters
    # segment_delimiter_set = {",", "。", ":", "?", "!", ";"}), # This is the defualt set of delimiters
    # recommend_dictionary = dictionary1, # words in this dictionary are encouraged
    # coerce_dictionary = dictionary2, # words in this dictionary are forced
)

# pos_sentence_list = pos(word_sentence_list)

# entity_sentence_list = ner(word_sentence_list, pos_sentence_list)

del ws
# del pos
# del ner

print(word_sentence_list)

print("done")