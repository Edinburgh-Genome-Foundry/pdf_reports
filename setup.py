# This will try to import setuptools. If not here, it will reach for the embedded
# ez_setup (or the ez_setup package). If none, it fails with a message
try:
    from setuptools import setup
except ImportError:
    try:
        import ez_setup
        ez_setup.use_setuptools()
    except ImportError:
        raise ImportError("PDF_Reports could not be installed, probably because"
                          " neither setuptools nor ez_setup are installed on"
                          "this computer. \nInstall ez_setup "
                          "([sudo] pip install ez_setup) and try again.")

from setuptools import setup, find_packages

exec(open('pdf_reports/version.py').read())  # loads __version__

setup(name='pdf_reports',
      version=__version__,
      author='Zulko',
      description='Create nice-looking PDF reports from HTML content.',
      long_description=open('README.rst').read(),
      license='MIT',
      keywords="PDF report web jinja weasyprint",
      packages=find_packages(exclude='docs'),
      include_package_data=True,
      install_requires=["pypugjs", "jinja2", "weasyprint"])
