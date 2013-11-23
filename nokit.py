#!/usr/bin/env python
# prerequisite:
# sudo apt-get install python-pip
# sudo pip install redis

import os
import sys

this_path=os.path.dirname(__file__)
sys.path.append(os.path.join(this_path, 'lib'))
import buildprop as prop

def opts(argv):
  opts = {}
  if 'help' in argv:
    return {'action': 'help'}
  for arg in argv:
    a = arg.split("=")
    opts[a[0]] = a[1]
  return opts

def double(x=3, y='hello'):
  x = int(x)
  print str(x * x) + "." + y

def buildprop(*args, **kwargs):
#def buildprop(action='create', name='demo', major='1', minor='0', patch='0', build='1', branch='master', target='debug', region='US', code='EN', type='dxxx'):
  default_args = {'action': 'create', 'name': 'demo', 'major': '1', 'minor': '0', 'patch': '0', 'build': '1', 'branch': 'master', 'target': 'debug', 'region': 'US', 'code': 'EN', 'type': 'dxxx'}
  action = kwargs['action'] if 'action' in kwargs.keys() else default_args['action']
  name  = kwargs['name'] if 'name' in kwargs.keys() else default_args['name']
  if action is None or name is None:
      print error
      exit(2)
  if action in ('create', 'initial'):
    p = prop.Project(name)
    p.major = kwargs['major'] if 'major' in kwargs.keys() else default_args['major']
    p.minor = kwargs['minor'] if 'minor' in kwargs.keys() else default_args['minor']
    p.patch = kwargs['patch'] if 'patch' in kwargs.keys() else default_args['patch']
    p.build = kwargs['build'] if 'build' in kwargs.keys() else default_args['build']
    p.branch = kwargs['branch'] if 'branch' in kwargs.keys() else default_args['branch']
    p.target = kwargs['target'] if 'target' in kwargs.keys() else default_args['target']
    p.region = kwargs['region'] if 'region' in kwargs.keys() else default_args['region']
    p.code = kwargs['code'] if 'code' in kwargs.keys() else default_args['code']
    p.type = kwargs['type'] if 'type' in kwargs.keys() else default_args['type']
  elif action in ('set'):
    p = prop.Project(name)
    if 'major' in kwargs.keys(): p.major = kwargs['major']
    if 'minor' in kwargs.keys(): p.minor = kwargs['minor']
    if 'patch' in kwargs.keys(): p.patch = kwargs['patch']
    if 'build' in kwargs.keys(): p.build = kwargs['build']
    if 'branch' in kwargs.keys(): p.branch = kwargs['branch']
    if 'target' in kwargs.keys(): p.target = kwargs['target']
    if 'region' in kwargs.keys(): p.region = kwargs['region']
    if 'code' in kwargs.keys(): p.code = kwargs['code']
    if 'type' in kwargs.keys(): p.type = kwargs['type']
  elif action in ('get'):
    p = prop.Project(name)
    if 'field' in kwargs.keys(): field = kwargs['field']
    if field is None:
      print error
      exit(2)
    print getattr(p, field)
  elif action in ('increase', '+1'):
    p = prop.Project(name)
    if 'field' in kwargs.keys(): field = kwargs['field']
    if field is None:
      print error
      exit(2)
    value = int(getattr(p, field)) + 1
    setattr(p, field, value)
  elif action in ('description'):
    p = prop.Project(name)
    print p.description
  elif action in ('version'):
    p = prop.Project(name)
    print p.version
  elif action in ('tag'):
    p = prop.Project(name)
    print p.tag
  elif action in ('setenv'):
    p = prop.Project(name)
    if sys.platform.startswith('win32'):
      f = open('setenv.bat', 'w')
      command='set'
    else:
      f = open('setenv.sh', 'w')
      command='export'
    
    f.write(command + " NOKIT_NAME=" + p.name + "\n")
    f.write(command + " NOKIT_MAJOR=" + p.major + "\n")
    f.write(command + " NOKIT_MINOR=" + p.minor + "\n")
    f.write(command + " NOKIT_PATCH=" + p.patch + "\n")
    f.write(command + " NOKIT_BUILD=" + p.build + "\n")
    f.write(command + " NOKIT_BRANCH=" + p.branch + "\n")
    f.write(command + " NOKIT_TARGET=" + p.target + "\n")
    f.write(command + " NOKIT_REGION=" + p.region + "\n")
    f.write(command + " NOKIT_CODE=" + p.code + "\n")
    f.write(command + " NOKIT_TYPE=" + p.type + "\n")
    f.write(command + " NOKIT_DESCRIPTION=" + p.description + "\n")
    f.write(command + " NOKIT_VERSION=" + p.version + "\n")
    f.write(command + " NOKIT_TAG=" + p.tag + "\n")
    f.close()
  elif action in ('print'):
    p = prop.Project(name)
    print("name = " + name)
    print("    major = " + p.major)
    print("    minor = " + p.minor)
    print("    patch = " + p.patch)
    print("    build = " + p.build)
    print("    branch = " + p.branch)
    print("    target = " + p.target)
    print("    region = " + p.region)
    print("    code = " + p.code)
    print("    type = " + p.type)
    print("    description = " + p.description)
    print("    version = " + p.version)
    print("    tag = " + p.tag)
  elif action in ('backup'):
    p = prop.Project(name)
    p.backup()
  elif action in ('restore'):
    p = prop.Project(name)
    if 'filename' in kwargs.keys(): 
      filename = kwargs['filename']
      p.restore(filename)
  elif action in ('list'):
    p = prop.Project(name)
    print '\n'.join(sorted(p.keys(), reverse=True))
  elif action in ('h', 'help'):
    print 'PLEASE USE THE FOLLOWING ACTIONS:'
    print '\n'.join(['create', 'initial', 'set', 'get', 'increase', '+1', 'description', 'version', 'setenv', 'print', 'tag', 'backup', 'restore', 'list', 'help'])
  else:
    print "error!"
    exit(2)

if __name__ == "__main__":
  if len(sys.argv) == 1:
    print "PLEASE USE THE FOLLOWING FUNCTIONS:"
    print '\n'.join( k for k, v in globals().items() if hasattr(v, "__call__") and k is not 'opts')
    exit(2)
  globals()[sys.argv[1]](**opts(sys.argv[2:]))
