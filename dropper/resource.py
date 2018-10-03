import boto3

ec2_client = boto3.client('ec2')
ec2_resource = boto3.resource('ec2')


def get_ec2_instance_by_id(instance_id):
    for ec2 in ec2_resource.instances.iterator():
        if ec2.id == instance_id:
            return ec2


def list_eips_for_ec2_instance(ec2):
    filters = [{
        'Name': 'instance-id',
        'Values': [ec2.id],
    }]
    return ec2_client.describe_addresses(Filters=filters)


def create_interface_for_ec2_instance(ec2, n_private_ip_address=1):
    subnet_id = ec2.subnet.id
    # need to know how many interfaces currently
    # cuz when attach to instance, we need to set device index for interface
    n_current_interface = len(list(ec2.subnet.network_interfaces.iterator()))
    # create one interface
    interface = ec2_client.create_network_interface(SecondaryPrivateIpAddressCount=n_private_ip_address,
            SubnetId=subnet_id)
    interface_id = interface['NetworkInterface']['NetworkInterfaceId']
    # attach to instance, with given device index
    ec2_client.attach_network_interface(DeviceIndex=n_current_interface,
            InstanceId=ec2.id,
            NetworkInterfaceId=interface_id)


def create_eip_for_ec2_instance(ec2, n_per_interface):
    for interface in ec2.subnet.network_interfaces.iterator():
        current_count = len(interface.private_ip_addresses)
        still_need = n_per_interface - current_count
        if still_need > 0:
            interface.assign_private_ip_addresses(SecondaryPrivateIpAddressCount=still_need)
    
        for p in interface.private_ip_addresses:
            if 'Association' in p:
                continue
    
            private_ip_address = p['PrivateIpAddress']
            eip = ec2_client.allocate_address()
            allocation_id = eip['AllocationId']
            ec2_client.associate_address(AllocationId=allocation_id,
                                         NetworkInterfaceId=interface.id,
                                         PrivateIpAddress=private_ip_address)


def clean_eip_for_ec2_instance(ec2):
    eips = list_eips_for_ec2_instance(ec2)
    for eip in eips['Addresses']:
        ec2_client.release_address(AllocationId=eip['AllocationId'])
