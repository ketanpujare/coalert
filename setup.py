from setuptools import setup

setup(
    name='covalert',
    version='1.0',
    py_modules=['covcli'],
    install_requries=['Click'],
    entry_points="""
            [console_scripts]
            covcli=covcli:cli
    """,
)
