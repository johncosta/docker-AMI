import time

import paramiko

from docker_ami.utils.aws import DEFAULT_AWS_USER


class Timeout(RuntimeError):
    """ """


class DockerVersionChecker(object):
    """ Class that uses paramiko to ssh into our image to check the docker
    version.  We need to poll for the following things:

    1) We can ssh into the instance
    2) We can execute the docker command

    Each polling option has a timeout, that when met, considers the option a
    failure

    """
    _user = DEFAULT_AWS_USER  # we're building aws images for now
    _max_ssh_wait = 120  # seconds
    _max_docker_wait = 240  # seconds
    _ssh_wait_increment = 2  # seconds
    _docker_wait_incrememnt = 10  # seconds
    _docker_version_command = 'docker version'

    def __init__(self, hostname, private_key_file, private_key_file_password):
        super(DockerVersionChecker, self).__init__()

        self._hostname = hostname
        self._private_key_file = private_key_file
        self._private_key_file_password = private_key_file_password

    def _wait_for_ssh_connection(self, client, hostname, username, pkey,
                                 max_wait, wait_increment):
        """ Tries to make an ssh connection with the client.  Will wait
        max_wait seconds to try to connect.

        :param client:
        :param hostname:
        :param username:
        :param pkey:
        :param max_wait:

        :returns waited: Returns the number of seconds waited before a
        connection was made

        :throws Timeout: If a connection cannot be made within max_wait time
        """
        not_done = True
        waited = 0

        while not_done and waited < max_wait:
            try:
                client.connect(hostname, username=username, pkey=pkey)
                not_done = False
            except Exception, e:
                # TODO: improve log message
                # TODO: use a real logger
                print("\rTrying to connect via ssh: {0}.  Waited: {1} of "
                      "{2}".format(e, waited, max_wait))
                time.sleep(wait_increment)
                waited += wait_increment

        if not_done:  # done
            raise Timeout("Timed out ({0} seconds) when trying to SSH into "
                          "({1})".format(max_wait, hostname))

        return waited

    def _wait_for_docker_version(self, client, max_wait, wait_increment):
        """ Docker may not be immediately available. We wait for max_wait
        seconds before giving up and assuming it's not installed.

        :param client:
        :param max_wait:
        :param wait_increment:
        """
        not_done = True
        waited = 0

        while not_done and waited < max_wait:
            stdin, stdout, stderr = client.exec_command(
                self._docker_version_command)
            err = ''.join([line.replace('\n', ' ') for line in stderr])
            if len(err) > 0:
                # TODO improve message
                # TODO use a real logger
                print "Trying to access docker: {0}. Waited: {1} of " \
                      "{2}".format(err, waited, max_wait)
                time.sleep(wait_increment)
                waited += wait_increment
            else:
                not_done = False

        if not_done:
            raise Timeout("Timed out ({0} seconds) when trying to get docker "
                          "version.".format(max_wait))

        values = self._get_docker_version_info(stdout=stdout)

        return waited, values

    def _get_docker_version_info(self, stdout=None):
        """ Parses the stdout for the docker information. """
        values = {}
        for line in stdout:
            try:
                (key, value) = line.split(":")
                new_key = key.strip('\n').lower().replace(' ', '_')
                value = value.strip()
                values.update({new_key: value})
            except Exception, e:
                print "Unable to get values: {0}".format(e)

        return values

    def get_docker_version(self, values=None):
        """ SSH's into the host and retrieves the version of docker installed

            ... Client version: 0.4.6
            ... Server version: 0.4.6
            ... Git commit: 9fe8bfb
            ... Go version: go1.1.1
        """
        pkey = paramiko.RSAKey.from_private_key_file(
            self._private_key_file, password=self._private_key_file_password)

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            ssh_wait = self._wait_for_ssh_connection(
                client, self._hostname, self._user, pkey, self._max_ssh_wait,
                self._ssh_wait_increment)
            # TODO improve message
            # TODO use a real logger
            print "Waited ({0}) for ssh to become available.".format(ssh_wait)

            docker_wait, values = self._wait_for_docker_version(
                client, self._max_docker_wait, self._docker_wait_incrememnt)
            # TODO improve message
            # TODO use a real logger
            print "Waited ({0}) for docker information.".format(docker_wait)

        except Timeout, e:
            print e

        finally:
            try:
                client.close()
            except:
                pass

        return values
