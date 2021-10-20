#!/bin/sh

rm -f */macro*.jpg

j=9
#settings=" -background white -alpha remove -trim -resize 1024x1024\\> -quality 95 "
settings=" -background white -alpha remove -trim -quality 95 "
echo $settings

for i in oldpng/carb*.png;
do 
	let j=$j+1; 
	convert $i $settings -resize 640x640\> CARBOHYDRATES/macro$j.jpg; 
	echo -n $j " "; 
done; 
echo ""

for i in oldpng/lipid*.png;
do 
	let j=$j+1; 
	convert $i $settings -resize 640x640\> LIPIDS/macro$j.jpg; 
	echo -n $j " "; 
done; 
echo ""

for i in oldpng/nucleic*.png;
do 
	let j=$j+1; 
	convert $i $settings -resize 640x640\> NUCLEOTIDES/macro$j.jpg; 
	echo -n $j " "; 
done; 
echo ""

for i in oldpng/protein*.png;
do 
	let j=$j+1; 
	convert $i $settings -resize 640x640\> PROTEINS/macro$j.jpg; 
	echo -n $j " "; 
done; 
echo ""

