from setuptools import setup, find_packages


setup(
    name='git-datasets',
    version='0.1.0-alpha',
    packages=find_packages(where="src"),
    package_dir={'': 'src'},
    install_requires=[
        line.strip() for line in 
        open("requirements.txt", encoding="utf-8").readlines()
    ],
    author='Rui Campos',
    description='Declaratively create, transform, and manage ML datasets.',
    long_description=open('README.md', encoding="utf-8").read(),
    long_description_content_type='text/markdown',
    url='https://github.com/RuiFilipeCampos/git-datasets',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ],
)
