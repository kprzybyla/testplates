from setuptools import (
    setup,
)


def main():
    setup(
        python_requires="~= 3.8",
        setup_requires=[
            "setuptools",
            "setuptools_scm[toml]",
        ],
        install_requires=[
            "resultful == 1.0.0a2",
            "mypy @ git+https://github.com/kprzybyla/mypy.git@testplates",
        ],
        extras_require={
            "format": [
                "black == 20.8b1",
                "flake8 ~= 3.8.0",
            ],
            "test": [
                "pytest ~= 6.0.1",
                "pytest-cov ~= 2.8.0",
                "hypothesis ~= 5.36.0",
            ],
            "docs": [
                "sphinx ~= 3.0.0",
                "sphinx_rtd_theme ~= 0.4.3",
                "sphinx_autodoc_typehints ~= 1.10.0",
            ],
            "deploy": [
                "wheel",
                "twine",
            ],
        },
    )


if __name__ == "__main__":
    main()
