import click

from dropper.drc.ec2 import ec2_eip_binding_info
from dropper.drc.ec2 import init_ec2_eip
from dropper.drc.ec2 import destroy_ec2_eip


@click.group()
@click.pass_context
def dropper_commands(ctx):
    pass


@dropper_commands.command()
@click.argument('instance_id')
@click.option('--interface-count', 'n_interface', default=1, type=int)
@click.option('--per-interface-count', 'n_per_interface', default=1, type=int)
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


def main():
    dropper_commands(obj={})
