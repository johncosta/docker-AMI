import time
import sys
import boto

from boto.exception import EC2ResponseError

DEFAULT_INSTANCE_SIZE = 't1.micro'
DEFAULT_AWS_USER = 'ubuntu'


def create_ssh_group(ec2_connection):
    """ Creates a security group used for SSH access.

    :params ec2_connection: an active ec2 connection
    :returns: ec2 security group
    """
    # TODO user logger
    print "Creating security group..."
    try:
        ssh_group = ec2_connection.create_security_group(
            'SSH', 'Basic SSH Access')
        ssh_group.authorize(
            ip_protocol='tcp', from_port=22, to_port=22, cidr_ip='0.0.0.0/0')
    except EC2ResponseError, re:
        print "Security group already created, retrieving..."
        ssh_groups = ec2_connection.get_all_security_groups(groupnames="SSH")
        ssh_group = ssh_groups[0]
    return ssh_group


def get_ec2_image(ec2_connection, image_id, my_image=None):
    """ Returns a ec2 image for the image_id requested.

    :params ec2_connection:
    :params image_id:
    :returns: ec2 image instance
    """
    # TODO use logger
    print "Getting image..."
    images = ec2_connection.get_all_images(image_ids=[image_id, ])

    for image in images:
        if image.id == image_id:
            my_image = image
    return my_image


def wait_until_instance_running(ec2_instance, image_id, image_name):
    """

    """
    # TODO use logger
    print "Spinning up instance for '%s' - %s. Waiting for it to boot up." % (
        image_id, image_name)
    waited = 0
    while ec2_instance.state != 'running':
        ec2_instance.update()
        time.sleep(1)
        waited += 1
        display = waited % 40
        try:
            sys.stdout.write("\r%s" % (display * ". "))
            sys.stdout.flush()
        except:
            pass

    print "\n"
    return ec2_instance


# boot an instance
def boot_image(ec2_connection, image_id, user_data, private_key_name,
               image_name, image_size):
    """

    """
    dev_sda1 = boto.ec2.blockdevicemapping.EBSBlockDeviceType()
    dev_sda1.size = image_size # size in Gigabytes
    bdm = boto.ec2.blockdevicemapping.BlockDeviceMapping()
    bdm['/dev/sda1'] = dev_sda1

    ssh_group = create_ssh_group(ec2_connection)
    image = get_ec2_image(ec2_connection, image_id)
    new_reservation = image.run(
        user_data=user_data, instance_type=DEFAULT_INSTANCE_SIZE,
        security_group_ids=[ssh_group.id, ],
        key_name=private_key_name,
        block_device_map=bdm
    )
    instance = new_reservation.instances[0]
    instance = wait_until_instance_running(instance, image_id, image_name)
    return instance


def stop_instance(ec2_connection, instance, image_id, image_name):
    """

    """
    # TODO use logger
    print "Stopping instance '%s' - %s. Waiting for it to stop." % (
        image_id, image_name)
    ec2_connection.stop_instances(instance_ids=[instance.id])
    waited = 0
    while instance.state != 'stopped':
        time.sleep(1)
        instance.update()
        waited += 1
        display = waited % 40
        try:
            sys.stdout.write("\r%s" % (display * ". "))
            sys.stdout.flush()
        except:
            pass
    print "\n"


def create_image(ec2_connection, instance, new_image_name, values):
    """  Snaps a new image

    """
    # TODO use logger
    print "Creating AMI '%s'. Waiting for image creation." % (
        new_image_name)
    try:
        new_image_id = ec2_connection.create_image(instance.id, new_image_name,
                                                   description=values)
    except EC2ResponseError, e:
        print "Unable to create image: {0}".format(e)
        return

    image = get_ec2_image(ec2_connection, new_image_id)

    waited = 0
    while image.state != 'available':
        time.sleep(1)
        image.update()
        waited += 1
        display = waited % 40
        try:
            sys.stdout.write("\r%s" % (display * ". "))
            sys.stdout.flush()
        except:
            pass
    print "\n"


def terminate_instance(ec2_connection, instance, image_id, image_name):
    """

    """
    # TODO use logger
    print "Terminating instance '%s' - %s. Waiting for it to terminate." % (
        image_id, image_name)
    ec2_connection.terminate_instances(instance_ids=[instance.id])
    waited = 0
    while instance.state != 'terminated':
        time.sleep(1)
        instance.update()
        waited += 1
        display = waited % 40
        try:
            sys.stdout.write("\r%s" % (display * ". "))
            sys.stdout.flush()
        except:
            pass
    print "\n"
