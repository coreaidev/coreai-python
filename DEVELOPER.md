rm -r dist/
python3 -m build
python3 -m twine upload -r testpypi dist/*
# or for production python3 -m twine upload  dist/*

