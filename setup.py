import sys
from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='PyLing',
      version='1.0',
      description='',
      long_description='',
      classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
      ],
      keywords='vocabulary flashcards english french',
      url='https://github.com/ddanco/PyLing',
      author='Dominique Danco',
      author_email='ddanco@gmail.com',
      packages=['pyling'],
      install_requires=[
          'PyQt5',
      ]
      package_data={'pyling': ['categories/*.txt', 'logos/*', 'dict.txt', 'Lexique381.txt']},
      )