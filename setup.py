from setuptools import setup, find_packages
from simula_bibrestclient import version


setup(name = 'simula_bibrestclient',
      description = 'RESTful client for the Simula (http://simula.no) bibliography REST api.',
      long_description = 'See http://github.com/espenak/simula_bibrestclient',
      version = version,
      license='BSD',
      url = 'http://github.com/espenak/simula_bibrestclient',
      author = 'Espen Angell Kristiansen',
      author_email = 'post@espenak.net',
      packages=find_packages(exclude=['ez_setup']),
      install_requires = ['distribute', 'restkit'],
      include_package_data=True,
      zip_safe=True,
      classifiers=[
                   'Development Status :: 5 - Production/Stable',
                   'License :: OSI Approved',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python'
                  ],
      entry_points = {
          'console_scripts': [
              'simula_bibrestclient = simula_bibrestclient.cli.main:main',
          ],
      }
)
