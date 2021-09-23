base=data/713-9.26

clear

set -e  # exit on error

echo Processing \'$base\'

# echo 
# echo "Word-HTML to JSON-items..."
# ./word2json-htmlParser.py $base.html $base.json

# echo
# echo "JSON-items to MF-XML..."
# ./json2mfxml.py $base.json $base.xml

echo
echo "MF-XML to JSON-tree..."
./mfxmlpreview.py $base.xml ${base}_preview.json

echo
echo "Done!"
echo "http://localhost:5000?data=${base}_preview.json"
echo