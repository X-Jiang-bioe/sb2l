from distutils.core import setup
setup(
  name = 'sb2l',         
  packages = ['sb2l'],   
  version = '0.1',      
  license='MIT',        
  description = 'sb2l Translates the biological models written in SBML into LaTeX code to be compiled and read by human eye',   # Give a short description about your library
  author = 'Xieergai Jiang, Herbert Sauro',                   
  author_email = 'jiangxieergai@gmail.com',      
  
  url = 'https://github.com/X-Jiang-bioe/sb2l/archive/v_0.1.tar.gz',   
  
  download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',   
  keywords = ['SBML', 'LaTeX', 'Converter'],   
  install_requires=[           
          'pylatex',
          'python-libsbml',
      ],
  python_requires='>=3',
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Science/Research',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)