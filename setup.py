from setuptools import setup, find_packages


def readme():
    with open('README.md', encoding='utf-8') as f:
        content = f.read()
    return content


setup(
    name='xprint',
    version='0.0.1',
    description='xprint',
    long_description=readme(),
    long_description_content_type='text/markdown',
    author='kurt.niu',
    author_email='niu1187203155@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=[], 
)