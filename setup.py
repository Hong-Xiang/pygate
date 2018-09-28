from setuptools import setup, find_packages

setup(name='dxl-pygate',
      version='0.13.0',
      description='A simplified python interface for Gate.',
      url='https://github.com/tech-pi/pygate',
      author='Hong Xiang',
      author_email='hx.hongxiang@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=['fs', 'click',
                        'rx', 'jinja2',
                        'jfs', 'dxl-cluster>=0.0.5', 'dask'],
      entry_points='''
            [console_scripts]
            pygate=pygate.cli:cli
      ''',
      include_package_data=True,
      zip_safe=False)
