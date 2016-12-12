import sys
from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='speechtools',
      version='0.5.0',
      description='',
      long_description='',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering',
        'Topic :: Text Processing :: Linguistic',
      ],
      keywords='speech corpus phonetics',
      url='https://github.com/MontrealCorpusTools/speechcorpustools',
      author='Montreal Corpus Tools',
      author_email='michael.e.mcauliffe@gmail.com',
      packages=['pyling'],
      install_requires=[
          'PyQt5',
      ]
      package_data={'pyling': ['categories/*.txt', 'logos/*', 'dict.txt', 'Lexique381.txt']},
      )