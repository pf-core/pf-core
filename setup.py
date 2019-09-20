from setuptools import setup, find_packages

setup(
    name="template",
    url="https://github.com/esteinig/app-template",
    author="Eike J. Steinig",
    author_email="eikejoachim.steinig@my.jcu.edu.au",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click",
        "pytest",
        "paramiko",
        "pymongo",
        "mongoengine",
        "flask",
        "flask-socketio",
        "flask-cors",
        "tqdm",
        "colorama",
        "pandas",
        "seaborn",
        "scipy",
        "python-dateutil",
        "numpy"
    ],
    entry_points="""
        [console_scripts]
        template=template.terminal.client:terminal_client
        elasmo=template.terminal.client:terminal_client
    """,
    version="0.1",
    license="MIT",
    description="Support package for Elasmobranch Reference Genome Consortium",
)
