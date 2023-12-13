from pg_configurator.version import __version__ as version
from setuptools import find_namespace_packages, setup

name = 'pg_configurator'
install_requires = [
    'psutil',
]


if __name__ == "__main__":
    setup(name=name,
          version=version,
          description='PostgreSQL configuration tool',
          classifiers=[
              'Intended Audience :: Developers',
              'Intended Audience :: System Administrators',
              'Programming Language :: Python',
              'Programming Language :: Python :: 3',
              'Topic :: Database',
          ],
          author='Oleg Gurov',
          url='https://github.com/TantorLabs/pg_configurator',
          license='MIT',
          keywords='postgresql configuration',
          python_requires='>=3.4',
          packages=find_namespace_packages(exclude=['tests*']),
          package_data={name: ['pg_settings_history/*']},
          include_package_data=True,
          install_requires=install_requires,
          entry_points={
              'console_scripts': [
                  'pg_configurator = pg_configurator.__main__:_cli_entrypoint',
              ],
          },
    )
