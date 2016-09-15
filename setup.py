from setuptools import setup

setup(name='althea',
      version='0.0.1',
      description='ALgoriTHms Exposed through a RESTful API .',
      url='https://github.com/benneely/althea',
      author='Ben Neely',
      author_email='nigelneely@gmail.com',
      license='GNU3',
      packages=['robocomp'],
      include_package_data=True,
          package_data={
        "althea": [
            "../README.md",
            "../MANIFEST.in",
            "model_db/*",
        ]
    },
      install_requires=[
          'numpy',
          'pandas'
      ],
      zip_safe=False)
