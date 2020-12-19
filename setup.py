import setuptools
import re

def find_version():
    verstrline = open("venvlink/__version__.py", "rt").read()
    try: 
        return re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", verstrline, re.M).group(1)
    except:
        raise RuntimeError("Could not find version string")

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()  

setuptools.setup(
    name='venvlink',
    description='Virtual environments centralized with activate proxy in your working dir.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    version=find_version(),
    author='Niko Pasanen',
    author_email='niko@pasanen.me',
    url = "https://github.com/np-8/venvlink",
    packages=setuptools.find_packages(),
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Utilities',
    ],
)