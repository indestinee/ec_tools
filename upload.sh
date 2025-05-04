pytest
black .
rm -rf dist/ build/ *.egg-info .pytest_cache/
find . | grep -E "(/__pycache__$|/\.DS_Store$)" | xargs rm -rf
python3 -m build
twine upload --repository ec-tools dist/*

