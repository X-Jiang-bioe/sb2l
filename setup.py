import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
  name = 'sb2l',         
  packages=setuptools.find_packages(),
  
  version = '0.1.2',      
  license='MIT',        
  description = 'sb2l Translates the biological models written in SBML into LaTeX code to be compiled and read by human eye',  
  long_description=long_description,
  long_description_content_type="text/markdown",
  author = 'Xieergai Jiang, Herbert Sauro',                   
  author_email = 'jiangxieergai@gmail.com',      
  url = 'https://github.com/X-Jiang-bioe/sb2l',   
  
  download_url = 'https://github.com/X-Jiang-bioe/sb2l/archive/v_0.1.2.tar.gz',  
  
  
  package_data={
        '': ['*.xsl', '*.rtf'], # to include yarosh files
    },
  
  keywords = ['SBML', 'LaTeX', 'Converter'],   
  install_requires=[           
          'pylatex',
          'python-libsbml',
      ],
  
  python_requires='>=3',
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Science/Research',     
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
