import click

from dropper.drc.ec2 import ec2_eip_binding_info
from dropper.drc.ec2 import init_ec2_eip
from dropper.drc.ec2 import destroy_ec2_eip
from dropper.drc.export import export_squid_conf
from dropper.drc.export import export_proxy


@click.group()
@click.pass_context
def dropper_commands(ctx):
    pass


@dropper_commands.command()
@click.argument('instance_id')
@click.option('--interface-count', '-n', 'n_interface', default=1, type=int)
@click.option('--per-interface-count', '-p', 'n_per_interface', default=1, type=int)
@click.pass_context
def init(ctx, instance_id, n_interface, n_per_interface):
    init_ec2_eip(ctx, instance_id, n_interface, n_per_interface)


@dropper_commands.command()
@click.argument('instance_id')
@click.pass_context
def info(ctx, instance_id):
    ec2_eip_binding_info(ctx, instance_id)


@dropper_commands.command()
@click.argument('instance_id')
@click.pass_context
def destroy(ctx, instance_id):
    destroy_ec2_eip(ctx, instance_id)


@dropper_commands.command()
@click.argument('instance_id')
@click.option('--squid', is_flag=True)
@click.option('--proxy', is_flag=True)
@click.pass_context
def export(ctx, instance_id, squid, proxy):
    if squid:
        export_squid_conf(ctx, instance_id)
    if proxy:
        export_proxy(ctx, instance_id)


def main():
    dropper_commands(obj={})
