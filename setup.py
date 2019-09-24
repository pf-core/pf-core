from setuptools import setup, find_packages

setup(
    name='pathfinder',
    url='https://github.com/esteinig/pathfinder',
    author='Eike J. Steinig',
    author_email='eikejoachim.steinig@my.jcu.edu.au',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'pytest',
        'paramiko',
        'pymongo',
        'mongoengine',
        'flask',
        'flask-socketio',
        'flask-cors',
        'tqdm',
        'colorama',
        'pandas',
        'seaborn',
        'scipy',
        'scikit-learn',
        'python-dateutil',
        'numpy',
        'dendropy'

    ],
    entry_points="""
        [console_scripts]
        pathfinder=pathfinder.terminal.client:terminal_client
        pf=pathfinder.terminal.client:terminal_client
    """,
    version='0.1',
    license='MIT',
    description='Pathfinder development package.',
)
