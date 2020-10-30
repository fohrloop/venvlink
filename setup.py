import setuptools
import re

def find_version():
    verstrline = open("venvlink/__version__.py", "rt").read()
    try: 
        return re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", verstrline, re.M).group(1)
    except:
        raise RuntimeError("Could not find version string")
        

setuptools.setup(
    name='venvlink',
    description='Virtual environments centralized with activate proxy in your working dir.',
    version=find_version(),
    author='Niko Pasanen',
    author_email='niko@pasanen.me',
    packages=setuptools.find_packages(),

)