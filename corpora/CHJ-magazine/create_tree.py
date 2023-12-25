import re
import argparse


def main(args):

    output_file_path = "magazine_lemma.sgml"

    with open(output_file_path, "w") as wp:
        with open(args.file_path) as rf:
            wp.write(f"<root>\n")

            doc_id = None
            sent_id = None
            sentence = []

            check_next_token = False
            sahen = False

            for line in rf:
                line = line.strip().split("\t")

                try:
                    doc_id_now = line[1]
                    if doc_id != doc_id_now:
                        if len(sentence) > 0:
                            wp.write(f"{' '.join(sentence)}\n")
                        sentence = []
                        if doc_id != None:
                            wp.write("</ARTICLE>\n")
                        doc_id = doc_id_now
                        wp.write(f'<ARTICLE id="{doc_id_now}">\n')
                except:
                    continue

                try:
                    lemma = line[9]
                    word = line[-1] # 出現形は 1800年代のデータだとカタカナばかりで、分析できない → lemma

                    pos = line[11]
                    sent_id_now = line[17]

                    if sent_id != sent_id_now:
                        if len(sentence) > 0:
                            wp.write(f"{' '.join(sentence)}\n")
                        sentence = []
                        sent_id = sent_id_now

                    if args.replace_person_location:
                        if "人名" in pos:
                            lemma = "-人名-"
                        if "地名" in pos:
                            lemma = "-地名-"

                    if "名詞" in pos:
                        word = lemma
                    word += "_" + pos.split("-")[0]
                    if check_next_token:
                        if word in set(["だ_助動詞", "です_助動詞", "なり_助動詞", "たり_助動詞"]):
                            sentence[-1] = sentence[-1][:-2] + "形状詞"
                        check_next_token = False
                        if sahen:
                            if word == "為る_動詞":
                                sentence[-1] = sentence[-1][:-3] + "する_動詞"
                                sahen = False
                                # サ変動詞としてまとめる場合、「為る_動詞」は追加しない
                                continue
                            sahen = False

                    if args.check_sahen_kejoshi:
                        # if pos == '名詞-形状詞可能':
                        # if '名詞' in pos and '形状詞可能' in pos: #「サ変形状詞可能」もあり、それは動詞にもなりうるので除外。
                        if pos == "名詞-普通名詞-形状詞可能":
                            check_next_token = True
                        if pos == "名詞-普通名詞-サ変形状詞可能":
                            check_next_token = True
                            sahen = True

                        # if 次の単語 == だろ、だ_助動詞、で、に、な、な、なら、です_助動詞: pos = '形状詞'
                        # sentence[-1] = sentence[-1][:-2] + '形状詞'

                    sentence.append(lemma)

                except:
                    continue

            wp.write("</ARTICLE>\n")
            wp.write("</root>\n")


def cli_main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file_path", help="path of file")
    parser.add_argument("--replace_person_location", action="store_true", help="bool, replace named entities (person, location) into -人名-, -地名- or not")
    parser.add_argument("--check_sahen_kejoshi", action="store_true", help="bool, check sahen and kejoshi or not")
    args = parser.parse_args()
    main(args)


if __name__ == "__main__":
    cli_main()
