import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="win32mica",
    version="1.7",
    author="Martí Climent",
    author_email="marticlilop@gmail.com",
    description="Apply mica background to Windows 11 Win32 apps made with python, such as Tkinter or PyQt/PySide apps",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/martinet101/win32mica",
    project_urls={
        "Bug Tracker": "https://github.com/martinet101/win32mica/issues",
    },
    classifiers=[
          'Intended Audience :: Developers',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)