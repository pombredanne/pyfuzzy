#!/bin/bash
# $Id: makehtml.sh,v 1.3 2003-03-20 08:47:26 rliebscher Exp $

export PYTHONPATH=../..
mkdir html
cd html

# if you want create local docs replace ../mypydoc.py 
# with the path to the pydoc in your python lib directory
#PYDOC=../mypydoc.py
PYDOC=../sfpydoc.py


python -O $PYDOC -w fuzzy
python -O $PYDOC -w fuzzy.norm
python -O $PYDOC -w fuzzy.operator
python -O $PYDOC -w fuzzy.set
python -O $PYDOC -w ./../..
#cd ..