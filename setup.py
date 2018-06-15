from distutils.core import setup

setup(
    name             = 'sexpr',
    version          = '0.1.0',
    license          = 'MIT',
    requires         = ['python (>= 3.4)'],
    provides         = ['sexpr'],
    description      = 'S-expression toolkit for Python',
    url              = 'http://github.com/IwoHerka/sexpr',
    packages         = ['sexpr', 'tests'],
    maintainer       = 'Iwo Herka',
    maintainer_email = 'hi@iwoherka.eu',
    author           = 'Iwo Herka',
    author_email     = 'hi@iwoherka.eu',

    classifiers  = [
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
