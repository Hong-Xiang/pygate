from setuptools import setup

setup(name='dxl-pygate',
      version='0.2',
      description='A simplified python interface for Gate.',
      url='https://github.com/Hong-Xiang/pygate',
      author='Hong Xiang',
      author_email='hx.hongxiang@gmail.com',
      license='MIT',
      packages=['pygate'],
      install_requires=['fs', 'click', 'pyyaml', 'rx'],
      scripts=['bin/pygate'],
      zip_safe=False)
