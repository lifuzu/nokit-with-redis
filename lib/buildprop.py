#!/usr/bin/env python

import redis
import ast

class Project(object):
  def __init__(self, name):
    self.name = name
    self.db = redis.StrictRedis(host="platbuild30.sjc1700.bnweb.user.bn", port=6379, db=0)

  @property
  def version(self):
    return self.db.hget(self.name, 'major') + '.' + self.db.hget(self.name, 'minor') + '.' + \
      self.db.hget(self.name, 'patch') + '.' + self.db.hget(self.name, 'build')

  @property
  def tag(self):
    return self.db.hget(self.name, 'branch') + '_' + self.version

  @property
  def description(self):
    return self.version + '.' + self.db.hget(self.name, 'branch') + '.' + \
      self.db.hget(self.name, 'target') + '.' + self.db.hget(self.name, 'region') + '.' + \
      self.db.hget(self.name, 'code') + '.' + self.db.hget(self.name, 'type') + '.' + \
      self.name + '.' + 'reserve'

  @property
  def major(self):
    return self.db.hget(self.name, 'major')

  @property
  def minor(self):
    return self.db.hget(self.name, 'minor')

  @property
  def patch(self):
    return self.db.hget(self.name, 'patch')

  @property
  def build(self):
    return self.db.hget(self.name, 'build')

  @property
  def branch(self):
    return self.db.hget(self.name, 'branch')

  @property
  def target(self):
    return self.db.hget(self.name, 'target')

  @property
  def region(self):
    return self.db.hget(self.name, 'region')

  @property
  def code(self):
    return self.db.hget(self.name, 'code')

  @property
  def type(self):
    return self.db.hget(self.name, 'type')

  @major.setter
  def major(self, value):
    self.db.hset(self.name, 'major', value)

  @minor.setter
  def minor(self, value):
    self.db.hset(self.name, 'minor', value)

  @patch.setter
  def patch(self, value):
    self.db.hset(self.name, 'patch', value)

  @build.setter
  def build(self, value):
    self.db.hset(self.name, 'build', value)

  @branch.setter
  def branch(self, value):
    self.db.hset(self.name, 'branch', value)

  @target.setter
  def target(self, value):
    self.db.hset(self.name, 'target', value)

  @region.setter
  def region(self, value):
    self.db.hset(self.name, 'region', value)

  @code.setter
  def code(self, value):
    self.db.hset(self.name, 'code', value)

  @type.setter
  def type(self, value):
    self.db.hset(self.name, 'type', value)

  def backup(self):
    backup_name = self.name + '_' + self.tag
    self.db.hset(backup_name, self.name, self.db.hgetall(self.name))
    return backup_name

  def restore(self, backup_name):
    backup_value = self.db.hgetall(backup_name)
    self.db.hmset(self.name, ast.literal_eval(backup_value[self.name]))

  def keys(self):
    return self.db.keys(self.name + "*")

if __name__ == "__main__":
  p = Project('demo')
  p.major = 1
  p.minor = 2
  p.patch = 12
  p.build = 125
  print p.version
  print p.major
  p.major = 5
  print p.version
  p.branch = 'debug'
  p.target = 'win32'
  p.region = 'US'
  p.code = 'EN'
  p.type = 'dxxx'
  print p.description
  print p.tag
  
  bn = p.backup()
  p.major = 15
  print p.description
  p.restore(bn)
  print p.description
  
  print sorted(p.keys())