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
            "Development Status :: 4 - Beta",
            "Intended Audience :: Developers",
            "Natural Language :: English",
            "Operating System :: POSIX",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Topic :: Software Development :: Testing",
            "Topic :: Software Development :: Libraries",
        ],
        install_requires=["typing_extensions>=3.7.2"],
        extras_require={
            "black": ["black==19.3b0"],
            "lint": ["flake8>=3.5.0"],
            "mypy": ["mypy>=0.620"],
            "test": ["pytest>=3.4.0", "pytest-cov>=2.5.1", "hypothesis~=5.3.1"],
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
