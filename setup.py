import os
import codecs

from setuptools import setup, find_packages


def main():
    with codecs.open("README.rst", encoding="utf-8") as handle:
        long_description = handle.read()

    setup(
        name="testplates",
        author="Krzysztof Przybyła",
        url="https://github.com/kprzybyla/testplates",
        description="Testing Templates",
        long_description=long_description,
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "Natural Language :: English",
            "Operating System :: POSIX",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Topic :: Software Development :: Testing",
            "Topic :: Software Development :: Libraries",
        ],
        install_requires=["typing_extensions ~= 3.7.0"],
        extras_require={
            "black": ["black == 19.3b0"],
            "lint": ["flake8 ~= 3.7.0"],
            "mypy": ["mypy ~= 0.760"],
            "test": ["pytest ~= 5.3.0", "pytest-cov ~= 2.8.0", "hypothesis ~= 5.6.0"],
            "deploy": ["wheel", "twine"],
        },
        use_scm_version={"write_to": os.path.join("src/testplates/_version.py")},
        platforms=["linux"],
        setup_requires=["setuptools_scm"],
        packages=find_packages(where="src"),
        package_dir={"": "src"},
    )


if __name__ == "__main__":
    main()
