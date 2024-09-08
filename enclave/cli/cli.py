import click
from enclave.core.enclave_secret_manager import EnclaveSecretManager

secret_manager = EnclaveSecretManager()

@click.group()
def cli():
    """Secret Manager CLI - Create, Update, Read, Delete secrets"""
    pass

@click.command()
@click.argument('name')
@click.argument('value')
def create(name, value):
    """Create a new secret"""
    try:
        created_secret = secret_manager.create_secret(name, value)
        click.echo(f"Secret '{name}' created with ID: {created_secret.id}")
    except Exception as e:
        click.echo(f"Error: {str(e)}")

@click.command()
@click.argument('name')
@click.argument('value')
def update(name, value):
    """Update an existing secret"""
    try:
        updated_secret = secret_manager.update_secret(name, value)
        click.echo(f"Secret '{name}' updated to version: {updated_secret.active_version}")
    except Exception as e:
        click.echo(f"Error: {str(e)}")

@click.command()
@click.argument('name')
@click.option('--version', default=None, help='Specify the version of the secret to retrieve.')
def read(name, version):
    """Read a secret by name (optionally by version)"""
    try:
        secret = secret_manager.get_secret(name, version)
        click.echo(f"Secret '{name}' (version {secret.version}): {secret.value}")
    except Exception as e:
        click.echo(f"Error: {str(e)}")

@click.command()
@click.argument('name')
def delete(name):
    """Delete a secret and its versions"""
    try:
        secret_manager.delete_secret(name)
        click.echo(f"Secret '{name}' deleted successfully.")
    except Exception as e:
        click.echo(f"Error: {str(e)}")

# Add commands to the CLI group
cli.add_command(create)
cli.add_command(update)
cli.add_command(read)
cli.add_command(delete)

if __name__ == '__main__':
    cli()
