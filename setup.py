try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

version = 0.1

setup(
    name='fa.demo',
    version='0.1',
    description="",
    author='',
    author_email='',
    #url='',
    install_requires=[
        "Pylons==dev,>=0.9.7", 
        "Formalchemy>=1.2.3",
        "fa.jquery>=0.6",
    ],
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    test_suite='nose.collector',
    package_data={'fademo': ['i18n/*/LC_MESSAGES/*.mo']},
    #message_extractors = {'fademo': [
    #        ('**.py', 'python', None),
    #        ('templates/**.mako', 'mako', {'input_encoding': 'utf-8'}),
    #        ('public/**', 'ignore', None)]},
    zip_safe=False,
    entry_points="""
    [paste.app_factory]
    main = fademo.config.middleware:make_app

    [paste.app_install]
    main = pylons.util:PylonsInstaller
    """,
)
