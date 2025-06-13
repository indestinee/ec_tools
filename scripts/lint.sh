autoflake --in-place --remove-all-unused-imports --remove-unused-variables $(find ec_tools demos tests -name "*.py" -not -path "**/__init__.py")
black ec_tools demos tests
pylint ec_tools demos tests

