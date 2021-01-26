import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lucier",
    version="0.0.1",
    author="Jacob Lurye",
    description="Sequence MIDI messages using a Flask-style interface.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jacoblurye/lucier",
    packages=["lucier"],
    install_requires=["mido==1.2.9", "python-rtmidi==1.4.6"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)