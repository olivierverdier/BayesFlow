# -*- coding: utf-8 -*-
try:
	from setuptools import setup, Extension
except ImportError:
	try:
		from setuptools.core import setup, Extension
	except ImportError:
		from distutils.core import setup, Extension

import platform		

def is_numpy_installed():
	try:
		import numpy
	except ImportError:
		return False
	return True

def is_cython_installed():
	try:
		import Cython
	except ImportError:
		return False
	return True




def setup_package():
	
	
	if is_numpy_installed() is False:
		raise ImportError("Numerical Python (NumPy) is not installed.\n")
	if is_cython_installed() is False:
		raise ImportError("Cython is not installed.\n")
	
	from numpy import get_include
	import numpy.distutils.system_info as sysinfo
	from Cython.Distutils import build_ext

	include_dirs_ = [lib_ for lib_ in sysinfo.default_lib_dirs]
	include_dirs_.append(get_include())
	if platform.system() == "Linux":
		libraries_ = ['gfortran','m', 'blas', 'lapack_atlas']
		include_dirs_.append(sysinfo.get_info('atlas')['include_dirs'][0])
	else:
		libraries_ = ['gfortran','m','blas','cblas','lapack']
		

	metadata = dict(name='BayesFlow',
	version='0.1',
	author='Jonas Wallin',
	url='',
	author_email='jonas.wallin81@gmail.com',
	requires=['numpy (>=1.3.0)',
			'cython (>=0.17)',
			'matplotlib',
			'mpi4py'
			'yaml',
			'json'],
	cmdclass = {'build_ext': build_ext},
	packages=['BayesFlow','BayesFlow.PurePython',
			'BayesFlow.PurePython.distribution','BayesFlow.distribution',
			'BayesFlow.utils','BayesFlow.mixture_util',
			'BayesFlow.data'],
	package_dir={'BayesFlow': 'src/'},
	ext_modules = [Extension("BayesFlow.mixture_util.GMM_util",
						   sources=["src/mixture_util/GMM_util.pyx",
									"src/mixture_util/c/draw_x.c",
									"src/distribution/c/distribution_c.c"],
						   include_dirs = include_dirs_,
						   library_dirs = [dirs for dirs in sysinfo.default_lib_dirs],
						   libraries=['gfortran','m'],
						   language='c'),
				 Extension("BayesFlow.distribution.distribution_cython",
						   sources=["src/distribution/distribution_cython.pyx",
									"src/distribution/c/distribution_c.c"],
						   include_dirs = include_dirs_,
						   library_dirs = [dirs for dirs in sysinfo.default_lib_dirs],
						   libraries=['gfortran','m'],
						   language='c'),
	Extension("BayesFlow.distribution.logisticNormal",sources=["src/distribution/logisticNormal.pyx","src/distribution/c/distribution_c.c"],
						   include_dirs = include_dirs_,
						   library_dirs = [dirs for dirs in sysinfo.default_lib_dirs],
						   libraries   = libraries_,
						   language='c')],
	)
	
	setup(**metadata)

if __name__ == "__main__":
	setup_package()