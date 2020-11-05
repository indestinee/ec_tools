import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

packages = {
    'ec_tools': 'src/ec_tools',
    'ec_tools.basic_tools': 'src/ec_tools/basic_tools',
    'ec_tools.database': 'src/ec_tools/database',
    'ec_tools.spider': 'src/ec_tools/spider',
    'ec_tools.image': 'src/ec_tools/image',
}

setuptools.setup(
    name='ec_tools',
    version='0.7',
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
