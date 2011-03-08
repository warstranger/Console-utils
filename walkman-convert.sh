#!/bin/bash

declare usage="Usage: `filename $0` <input_file> <output_file>\n
	<output_file> should have .mp4 extension. If it is not then it will be added automatically."

if [[ ! -f "$1" ]]; then
	echo No input file.
	echo -e $usage
	exit
elif [[ -z "$2" || `filename "$2"` == "" ]]; then
	echo No output file.
	echo -e $usage
	exit
fi

declare ifile="$1"
declare ofile="$2"
declare ofile_mp4added=0

if [[ ${ofile: -4} != '.mp4' ]]; then
	ofile+=".mp4"
	ofile_mp4added=1
fi

echo -ne "Input file: $ifile\nOutput file: $ofile"
if [[ $ofile_mp4added == "1" ]]; then
	echo -e " (extension added automatically)"
else
	echo
fi

if [[ -f "$ofile" ]]; then
	echo Output file is already present. Specify another location.
else
	echo Converting ...
	ffmpeg -i "$ifile" -acodec libfaac -ab 96k -vcodec mpeg4 -s 320x240 "$ofile"
fi
