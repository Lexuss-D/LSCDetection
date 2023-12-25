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


# def read_sgml(file_path, start_year, end_year, was_adding_pos):
def read_sgml(file_path, start_year, end_year):
    """read sgml file and output text from each magazine

    :return: paragraph, each one has one or more sentences
    """
    with open(file_path) as file:
        sgml_tree = ET.parse(file)
        paragraph = []
        for word in sgml_tree.findall("ARTICLE"):
            year = get_year(word.get("id"))

            if year == None:
                continue
            if start_year <= year <= end_year:
                magazine = word.text
                # 25: 終端記号「。」の語彙素ID
                magazine = magazine.split(" 25\n")
                magazine = [' '.join(sent.strip().split("\n")) for sent in magazine]
                sentences = [sent + " 25" for sent in magazine] 
                paragraph.extend(sentences)

        return paragraph


def main(args):
    output_file_path = f"magazine_{args.start_year}-{args.end_year}.txt"
    paragraph = read_sgml(
        args.file_path,
        args.start_year,
        args.end_year,
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
    args = parser.parse_args()
    main(args)


if __name__ == "__main__":
    cli_main()
