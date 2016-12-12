
    pyinstaller -w --clean -y \
        --additional-hooks-dir=freezing/hooks \
        --hidden-import setuptools \
        --debug \
        pyling/PyLing.py