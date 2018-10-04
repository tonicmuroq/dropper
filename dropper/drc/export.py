import click

import dropper
from dropper.style import info
from dropper.style import error
from dropper.resource import get_ec2_instance_by_id
from dropper.templates import Jinja2

INFO_HEADER = ['Private IP', 'Public(Elastic) IP']
TEMPLATE = Jinja2(dropper.__name__)


def export_squid_conf(context, instance_id, filename='squid.conf'):
    ec2 = get_ec2_instance_by_id(instance_id)
    if not ec2:
        click.echo(error('EC2 instance {} not found'.format(instance_id)))
        context.exit(-1)

    ifs = ec2.subnet.network_interfaces.iterator()
    data = [(n['PrivateIpAddress'],
             n.get('Association', {}).get('PublicIp', '')) for i in ifs for n in i.private_ip_addresses]
    data = sorted(data)

    privates = [{'ip': k[0], 'port': index} for index, k in enumerate(data, 12000)]
    content = TEMPLATE.render_template('/squid.jinja', privates=privates)
    with open(filename, 'w') as f:
        f.write(content)

    click.echo(info('squid config generated at {}'.format(filename)))


def export_proxy(context, instance_id, filename='proxy'):
    ec2 = get_ec2_instance_by_id(instance_id)
    if not ec2:
        click.echo(error('EC2 instance {} not found'.format(instance_id)))
        context.exit(-1)

    ifs = ec2.subnet.network_interfaces.iterator()
    data = [(n['PrivateIpAddress'],
             n.get('Association', {}).get('PublicIp', '')) for i in ifs for n in i.private_ip_addresses]
    data = sorted(data)

    data = ['{}:{}\n'.format(k[1], index) for index, k in enumerate(data, 12000)]
    with open(filename, 'w') as f:
        for d in data:
            f.write(d)

    click.echo(info('proxy generated at {}'.format(filename)))
