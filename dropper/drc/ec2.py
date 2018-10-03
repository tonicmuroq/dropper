import click
from tabulate import tabulate

from dropper.style import info
from dropper.style import error
from dropper.resource import get_ec2_instance_by_id
from dropper.resource import create_interface_for_ec2_instance
from dropper.resource import create_eip_for_ec2_instance
from dropper.resource import clean_eip_for_ec2_instance

INFO_HEADER = ['Private IP', 'Public(Elastic) IP']


def ec2_eip_binding_info(context, instance_id):
    ec2 = get_ec2_instance_by_id(instance_id)
    if not ec2:
        click.echo(error('EC2 instance {} not found'.format(instance_id)))
        context.exit(-1)

    for interface in ec2.subnet.network_interfaces.iterator():
        click.echo(info('Interface {}'.format(interface.id)))

        data = [(n['PrivateIpAddress'],
                 n.get('Association', {}).get('PublicIp', '')) for n in interface.private_ip_addresses]
        click.echo(tabulate(data, headers=INFO_HEADER, tablefmt='fancy_grid'))


def init_ec2_eip(context, instance_id, n_interface, n_per_interface):
    ec2 = get_ec2_instance_by_id(instance_id)
    if not ec2:
        click.echo(error('EC2 instance {} not found'.format(instance_id)))
        context.exit(-1)

    # we may need to create some interfaces here
    interfaces = list(ec2.subnet.network_interfaces.iterator())
    still_need_interface = n_interface - len(interfaces)
    for _ in range(still_need_interface):
        create_interface_for_ec2_instance(ec2)

    create_eip_for_ec2_instance(ec2, n_per_interface)
    click.echo(info('Elastic IP created and bound done'))


def destroy_ec2_eip(context, instance_id):
    ec2 = get_ec2_instance_by_id(instance_id)
    if not ec2:
        click.echo(error('EC2 instance {} not found'.format(instance_id)))
        context.exit(-1)

    clean_eip_for_ec2_instance(ec2)
    click.echo(info('All elastic IP removed from {}'.format(instance_id)))
