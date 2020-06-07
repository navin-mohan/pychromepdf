import setuptools

with open('README.md','r') as f:
    long_desc = f.read()

setuptools.setup(
    name='pychromepdf',
    version='1.1',
    author='Navin Mohan',
    author_email='navinmohan81@gmail.com',
    description='Creates PDFs from HTML rendered using chrome or chromium',
    long_description=long_desc,
    long_description_content_type='text/markdown',
    url='https://github.com/nvnmo/pychromepdf',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta'
    ],
)
