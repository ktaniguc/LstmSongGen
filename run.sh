#!/bin/sh

INPUT_DIR=testInput/
OUTPUT=output
MODEL_NAME=test_model
BPM="120"

DIR=$PWD
if [ ! -d $DIR/output_txt ]; then
  echo "directory for output text is not found, create ..."
  mkdir $DIR/output_txt
fi
if [ ! -d $DIR/output_mid ]; then
  echo "directory for output midi is not found, create ..."
  mkdir $DIR/output_mid
fi
python mid2txt.py $INPUT_DIR $DIR/output_txt/$OUTPUT   # cnv inputMids to text
python main.py $DIR/output_txt/$OUTPUT $MODEL_NAME  #learning!!
python chunk2midi.py $DIR/output_txt/$OUTPUT $DIR/output_mid/$OUTPUT $BPM
