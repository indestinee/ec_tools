import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

packages = {
    'ec_tools': 'src/ec_tools',
    'ec_tools.basic_tools': 'src/ec_tools/basic_tools',
}

setuptools.setup(
    name='ec_tools',
    version='0.1',
    packages=packages.keys(),
    package_dir=packages,
    url='http://github.com/indestinee/ec_tools',
    author='ec',
    author_email='indestinee@gmail.com',
    description='tools',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
