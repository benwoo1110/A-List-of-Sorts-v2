import os
import pkg_resources


class Dependency:
    def __init__(self, requiredPackages:list):
        self.requiredPackages = requiredPackages

    def check(self):
        for dependency in self.requiredPackages:
            try:
                pkg_resources.require(dependency)

            except pkg_resources.VersionConflict:
                print('Dependency {} outdated. Attempting to update now...'.format(dependency))
                os.system('pip3 install --no-cache-dir {}'.format(dependency))

            except pkg_resources.DistributionNotFound:
                print('Dependency {} not found. Attempting to install now...'.format(dependency))
                os.system('pip3 install --no-cache-dir {}'.format(dependency))
