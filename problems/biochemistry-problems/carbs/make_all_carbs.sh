#!/bin/bash

./D_to_L_Fischer_configuration.py
./D_to_L_Haworth_configuration.py
./classify_Fischer.py

./classify_Haworth.py -p
./classify_Haworth.py -f
cat bbq-classify_Haworth-??RAN-questions.txt > bbq-classify_Haworth-questions.txt
rm -f bbq-classify_Haworth-??RAN-questions.txt

./convert_Fischer_to_Haworth.py -p
./convert_Fischer_to_Haworth.py -f
./convert_Haworth_to_Fischer.py -p
./convert_Haworth_to_Fischer.py -f

cat bbq-convert_*RAN-questions.txt > bbq-convert_Fischer_and_Haworth-questions.txt
rm -f bbq-convert_*RAN-questions.txt

echo ""
echo ""
wc -l bbq-*-questions.txt
echo ""
echo ""
echo "done"

echo "mv -v bbq-*-questions.txt ~/nsh/biology-problems-website/docs/biochemistry/topic09/"
