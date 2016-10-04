from setuptools import setup

setup(name='althea',
      version='0.0.1',
      description='ALgoriTHms Exposed through a RESTful API .',
      url='https://github.com/benneely/althea',
      author='Ben Neely',
      author_email='nigelneely@gmail.com',
      license='GNU3',
      packages=['althea'],
      include_package_data=True,
      package_data={
        "althea": [
            "../README.md",
            "../MANIFEST.in",
            "./model_db/framingham30/*",

        ]
    },
      install_requires=[
          'numpy',
          'pandas'
      ],
      entry_points={
            'console_scripts': [
                'althea = althea.__main__:main'
            ]
        },
      zip_safe=False)
