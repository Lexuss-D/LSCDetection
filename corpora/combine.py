import pandas as pd
from tqdm import tqdm

suw_data = pd.read_table(
    "PM/PM.txt",
    
    header=None,
    index_col=False,
    names=[
        "サブコーパス名",
        "サンプルID",
        "文字開始位置",
        "文字終了位置",
        "連番",
        "出現形開始位置",
        "出現形終了位置",
        "固定長フラグ",
        "可変長フラグ",
        "文頭ラベル",
        "語彙表ID",
        "語彙素ID",
        "語彙素",
        "語彙素読み",
        "語彙素細分類",
        "語種",
        "品詞",
        "活用形",
        "語形",
        "用法",
        "書字形",
        "書字形出現形",
        "原文文字列",
        "発音出現形",
    ],
)
words = suw_data.loc[:, ["サブコーパス名", "文頭ラベル", "語彙素"]]
outPath = "BCCWJ-magazine/PM_SUW_sentences_lemma.txt"

allsentences = []
sent = ""
for index, row in tqdm(words.iterrows()):
    if row[1] == "B":
        if sent:
            allsentences.append(sent)
        sent = str(row[2])
    elif row[1] == "I":
        sent+= " " +str(row[2])
if sent:
    allsentences.append(sent)


with open(outPath, "w") as f:
    for element in allsentences:
        f.write(str(element) + "\n")
