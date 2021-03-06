#! /usr/bin/env python3

import os
from subprocess import call 
import time
import json

timeStartAll = time.time()

hostOpenUxAS_Dir = '{0}/..'.format(os.getcwd())


print("\n##### STARTING DOCKER BUILD #####\n")

call('export PATH=/usr/local/bin:$PATH',shell=True)

print("\n##### START uxas_build container #####\n")
cmd = ('docker run -i --rm -d ' +
      '--name uxas_build -w="/UxASDev/OpenUxAS" ' +
      '--mount type=bind,source={0}/../..,target="/UxASDev" '.format(os.getcwd()) +
      '--mount source=UxAS_Build_Vol,target="/tmp_build" ' + 
      'uxas/uxas-build:x86_64')
call(cmd,shell=True)


timeStartBuild = time.time()
print("\n##### START BuildUxAS #####\n")
cmd = 'docker exec -i uxas_build  bash /UxASDev/OpenUxAS/docker/ContainerScriptsAndFiles/buildUxAS.sh'
call(cmd,shell=True)
print('\n##### FINISHED-BuildUxAS  Build Time [{0}] #####\n\n\n'.format(time.time() - timeStartBuild))

print('\n##### KILL uxas_build container #####\n')
cmd = 'docker kill uxas_build'
call(cmd,shell=True)

print("\n#####  Building Deploy Container #####\n\n\n")
cmd = 'docker build -t uxas/uxas-deploy:x86_64 -f ContainerScriptsAndFiles/Dockerfile_uxas-deploy .'
call(cmd,shell=True);

print('\n##### FINISHED  Total Build/Deploy Time [{0}] #####\n'.format(time.time() - timeStartAll))



