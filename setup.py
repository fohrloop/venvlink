import setuptools
import re


def find_version():
    verstrline = open("venvlink/__version__.py", "rt").read()
    try:
        return re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", verstrline, re.M).group(
            1
        )
    except:
        raise RuntimeError("Could not find version string")


with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="venvlink",
    description="""Creating the virtual environment outside of the project folder, still retaining the feel of good ol' "python -m venv venv".""",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    version=find_version(),
    author="Niko Pasanen",
    author_email="niko@pasanen.me",
    url="https://github.com/np-8/venvlink",
    packages=setuptools.find_packages(),
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Utilities",
    ],
)