from setuptools import setup, find_packages

setup(
    name="kubegpt",
    author="Benji Visser",
    author_email="benji@xeol.io",
    version="0.0.6",
    description="Using human language to interact with Kubernetes",
    license="MIT",
    packages=find_packages(),
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    entry_points={
        "console_scripts": ["kubegpt = kubegpt.__main__:main"],
    },
    python_requires=">=3.9",
    install_requires=[
        "openai",
        "langchain",
    ],
    url="https://github.com/xeol-io/kubegpt"
)
