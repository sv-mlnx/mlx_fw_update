import os
import sys

hosts_f = open(sys.argv[1])
hosts   = [ii.rstrip() for ii in hosts_f.readlines()]

mlx_fw  = 'fw-ConnectX4Lx-rel-14_23_1020-MCX4411A-ACQ_Ax-UEFI-14.16.17-FlexBoot-3.5.504.bin'
mlx_mft = 'mft-4.10.0-104.x86_64-rpm'
mlx_dev = '/dev/mst/mt4117_pciconf0'

for ii in hosts:
  cmd = "scp %s.zip user@%s:" %(mlx_fw, ii)
  os.system(cmd)

  cmd = "scp %s.tgz user@%s:" %(mlx_mft, ii)
  os.system(cmd)

## remote access

import paramiko

for ii in hosts:
  client = paramiko.SSHClient()
  client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  client.connect(hostname=ii, username='user', password='password')

  cmd = "tar xvzf %s.tgz" %(mlx_mft)
  stdin,stdout,stderr = client.exec_command(cmd)

  # FIXME do YUM

  cmd = "sudo bash %s/install.sh" %(mlx_mft)
  stdin,stdout,stderr = client.exec_command(cmd)
  stdin.write('password\n')

  cmd = "sudo %s" %(mst start)
  stdin,stdout,stderr = client.exec_command(cmd)
  stdin.write('password\n')

  cmd = "unzip %s.zip" %(mlx_fw)
  stdin,stdout,stderr = client.exec_command(cmd)

  cmd = "sudo flint -d %s -i %s b" %(mlx_dev, mlx_fw)
  stdin,stdout,stderr = client.exec_command(cmd)
  stdin.write('password\n')
