import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="chat-server",
    version="0.0.0",
    author="Alberto Oporto",
    author_email="alberto.oporto@utec.edu.pe",
    description="Chat server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CS-UTEC/tarea2-clienteservidor-otreblan",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
    ],
    install_requires=[
        "Flask",
        "SQLAlchemy",
    ],
    entry_points={
        "console_scripts": [
            "chat-server = chat_server.__init__:main",
        ],
    },
    package_data={
        "": ["static/*/*"]
    },
    python_requires='>=3.3',
)
