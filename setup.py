from setuptools import setup, find_packages

setup(name='dxl-pygate',
      version='0.13.2',
      description='A simplified python interface for Gate.',
      url='https://github.com/tech-pi/pygate',
      author='Hong Xiang',
      author_email='hx.hongxiang@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'dxl-shape',
          'click',
          'rx',
          'jinja2',
          'jfs',
          'dask',
          'pandas',
          'pathlib',
          'numpy',
          'scipy',
          'requests'
      ],
      entry_points='''
            [console_scripts]
            pygate=pygate.cli:cli
      ''',
      include_package_data=True,
      zip_safe=False)
