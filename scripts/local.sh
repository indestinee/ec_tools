autoflake --in-place --remove-all-unused-imports --remove-unused-variables $(find ec_tools demos tests -name "*.py" -not -path "**/__init__.py")
black .
pytest
rm -rf dist/ build/ *.egg-info .pytest_cache/
find . | grep -E "(/__pycache__$|/\.DS_Store$)" | xargs rm -rf
python3 -m build
pip3 install .

