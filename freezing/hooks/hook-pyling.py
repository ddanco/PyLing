

import os
import sys

from PyInstaller.utils.hooks import (
    collect_data_files, collect_dynamic_libs, copy_metadata)



root_dir = os.path.abspath('pyling')
categories_dir = os.path.join(root_dir, 'categories')
logo_dir = os.path.join(root_dir, 'logos')
datas = [(os.path.join(root_dir, 'dict.txt'), '.'), (os.path.join(root_dir, 'Lexique381.txt'), '.')] + [( os.path.join(categories_dir, x), 'categories')
            for x in os.listdir(categories_dir)
    ]+ [( os.path.join(logo_dir, x), 'logos')
            for x in os.listdir(logo_dir)
    ]
