#!/usr/bin/env python
#coding=utf8

###################################################################################################
import os
import subprocess
import glob
import sys

###################################################################################################
def dpkgFind(debs, sstr):
	try:
		for i,deb in enumerate(debs):
			if deb.startswith('%s_' % sstr):
				return i, deb
		for i,deb in enumerate(debs):
			if deb.startswith(sstr):
				return i, deb
		return -1,None
	except:
		pass
		return -1,None
###################################################################################################
def dpkgInstall(debs, force_depend=False):
	deb = debs[0]
	print "Try to install <%s> : "%deb,
	my_env = os.environ
	my_env["LANG"] = "C"
	cmds = ['/usr/bin/dpkg']
	if force_depend: cmds.append('--force-depends')
	cmds.extend(('-i',deb))
	#print ' cmd=<%s> ' % ' '.join(cmds)
	po = subprocess.Popen(cmds, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
	po.wait()
	sout = po.stdout.read()
	serr = po.stderr.read()
	depends = []
	#print ' returncode=<%s> ' % po.returncode
	if po.returncode == 0:
		del debs[0]
		if force_depend:
			print "OK! with force-depends"
		else:
			print "OK!"
		return True, depends
	for line in serr.split('\n'):
		eles = line.split()
		if len(eles) < 2: continue
		if eles[0] != 'Package': continue
		fndx, fdeb = dpkgFind(debs, eles[1])
		if fndx < 0:
			emsg = 'dpkgInstall: Cannot find dependent package <%s>' % eles[1]
			#raise ReferenceError(emsg)
			sys.stderr.write('%s\n' % emsg)
		else:
			del [fndx]
			debs.insert(0,fdeb)
			depends.append(eles[1])
	print "Fail! Depends on %s" % depends
	if len(depends) <= 1:
		return dpkgInstall(debs, force_depend=True)
	return False, depends

###################################################################################################
def dpkgDo(folder='.'):
	debs = []
	for deb in glob.glob('%s/*.deb' % folder):
		debs.append(os.path.basename(deb))
	while len(debs) > 0:
		dpkgInstall(debs)

###################################################################################################
if __name__ == '__main__':
	dpkgDo()
