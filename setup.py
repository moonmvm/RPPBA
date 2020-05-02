from setuptools import setup, find_packages

setup(
    name='rppba',
    version='0.1',
    author='Dmitry Mishuto',
    author_email='moonmvmd@gmail.com',
    description='Backend for rppba university project',
    packages=find_packages(),
    install_requires=[
        'django==2.2.10',
        'djangorestframework==3.11.0',
        'gunicorn==20.0.4',
        'Jinja2==2.10.3',
    ],
    include_package_data=True,
)
