import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='gsselect',
     version='1.0.1',
     scripts=['gsselect.py', 'gemcats.py', 'inpoly.py', 'parangle.py', 'urltrigger.py'] ,
     author="Bryan Miller",
     author_email="millerwbryan@gmail.com",
     description="Gemini guide star selection and URL TOO triggering",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/bryanmiller/gsselect",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python",
         'Intended Audience :: Science/Research',
         "License :: AURA copyright",
         "Operating System :: OS Independent",
     ],
     install_requires=[
         'astropy',
         'matplotlib',
         'numpy',
         'aplpy'
     ]
)