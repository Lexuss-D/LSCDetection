import re
import argparse
import xml.etree.ElementTree as ET


def get_year(id):
    """obtain its published year

    :param num: number of units splited
    :param id: id of magazine
    :param year: published year
    :return year: published year
    """
    num = len(id.split("_"))
    if num == 2:
        # 60M(雑誌名)(年)_(その他)_
        year = id.split("_")[0][-4:]
    elif num == 4:
        # (文芸春秋|国民之友|太陽etc)-(年)(月)_(タイトル)__b
        year = id.split("_")[0].split("-")[1][:4]
    else:
        return None
    return int(year)


def read_sgml(file_path, start_year, end_year, is_removed_pos):
    """read sgml file and output text from each magazine

    :return: paragraph, each one has one or more sentences
    """
    with open(file_path) as file:
        sgml_tree = ET.parse(file)
        paragraph = []
        for word in sgml_tree.findall("ARTICLE"):
            # print(word.attrib)
            year = get_year(word.get("id"))

            if year == None:
                continue
            # 取り出したい年
            # if 1894<=year<1927: #phase1
            # if 1927<=year<1945: #phase2
            # if 1945<=year<1970: #phase3
            # if 1970<=year<1997: #phase4
            # if 1894<=year<1945: #pre-war
            # if 1945<=year<1997:  # post-war
            if start_year <= year <= end_year:
                magazine = word.text
                magazine = magazine.split("\n")
                # magazine の文を全て結合し、句読点のみで分割
                magazine = " ".join(magazine)
                lines = magazine.split(" 。_補助記号")
                lines = [line + " 。_補助記号" for line in lines]
                if is_removed_pos:
                    fixed_lines = []
                    for line in lines:
                        token_poses = [
                            token_pos
                            for token_pos in line.split()
                            if len(token_pos) > 0
                        ]
                        tokens = [token_pos.split("_")[0] for token_pos in token_poses]
                        fixed_line = " ".join(tokens)
                        fixed_lines.append(fixed_line)
                    lines = fixed_lines
                
                # extend が悪さをしていた
                paragraph.extend(lines)

        return paragraph


def main(args):
    output_file_path = f"magazine_{args.start_year}-{args.end_year}.txt"
    paragraph = read_sgml(
        args.file_path,
        args.start_year,
        args.end_year,
        args.is_removed_pos,
    )
    with open(output_file_path, "w") as fp:
        for sentence in paragraph:
            if len(sentence) > 0:
                fp.write(f"{sentence}\n")


def cli_main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file_path", help="path of the sgml file")
    parser.add_argument("-s", "--start_year", type=int, help="start of year")
    parser.add_argument("-e", "--end_year", type=int, help="end of year")
    parser.add_argument(
        "-r", "--is_removed_pos", action="store_true", help="bool, remove pos or not"
    )
    args = parser.parse_args()
    main(args)


if __name__ == "__main__":
    cli_main()
