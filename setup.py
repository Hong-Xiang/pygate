from setuptools import setup

setup(name='dxl-pygate',
      version='0.5.0',
      description='A simplified python interface for Gate.',
      url='https://github.com/Hong-Xiang/pygate',
      author='Hong Xiang',
      author_email='hx.hongxiang@gmail.com',
      license='MIT',
      packages=['pygate', 'pygate.template'],
      install_requires=['fs', 'click', 'pyyaml', 'rx', 'jinja2', 'dxl-dxpy>=0.4'],
      scripts=['bin/pygate'],
      zip_safe=False)
