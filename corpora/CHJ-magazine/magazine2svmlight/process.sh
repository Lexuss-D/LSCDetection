echo "00: unzip"

unzip 20200106_magazine_new_dump.zip

echo "done"

echo "01: create_tree"

python3 create_tree.py --file_path magazine_new_dump.rpt

echo "02: split_magazine_by_year"

python3 split_magazine_by_year.py --file_path magazine.sgml --start_year 1965 --end_year 1965

echo "done"

echo "03: write_svmlight"

python3 write_svmlight.py --file_path magazine_1965-1965.txt --window_size 4 --threshold 20

echo "done"
