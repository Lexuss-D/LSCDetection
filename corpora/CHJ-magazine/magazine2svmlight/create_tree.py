import re
import argparse


def main(args):

    output_file_path = "magazine.sgml"

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

                # """
                try:
                    morph_id = line[16]
                    sent_id_now = line[17]

                    if sent_id != sent_id_now:
                        if len(sentence) > 0:
                            wp.write(f"{' '.join(sentence)}\n")
                        sentence = []
                        sent_id = sent_id_now

                    # print(word)
                    sentence.append(morph_id)

                except:
                    continue

            wp.write("</ARTICLE>\n")
            wp.write("</root>\n")


def cli_main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file_path", help="path of file")
    args = parser.parse_args()
    main(args)


if __name__ == "__main__":
    cli_main()
