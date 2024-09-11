import os
import click
import requests
import json

API_URL = os.getenv('API_URL')

@click.group()
def cli():
    """Secret Manager CLI - Create, Update, Read, Delete secrets"""
    pass

@click.command()
@click.option('--name', required=True, help='The name of the secret')
@click.option('--value', required=True, help='The value of the secret')
def create(name, value):
    """Create a new secret."""
    payload = {
        "name": name,
        "value": value
    }
    headers = {
        "X-API-KEY": os.getenv('API_KEY')
    }
    response = requests.post(f"{API_URL}/secrets", json=payload, headers=headers)

    if response.status_code == 200:
        click.echo(f"Secret '{name}' created successfully.")
    else:
        click.echo(f"Failed to create secret. Error: {response.text}")

@click.command()
@click.option('--name', required=True, help='The name of the secret to update')
@click.option('--value', required=True, help='The new value of the secret')
def update(name, value):
    """Update an existing secret."""
    payload = {
        "value": value
    }
    headers = {
        "X-API-KEY": os.getenv('API_KEY')
    }
    response = requests.put(f"{API_URL}/secrets/{name}", json=payload, headers=headers)

    if response.status_code == 200:
        click.echo(f"Secret '{name}' updated successfully.")
    else:
        click.echo(f"Failed to update secret. Error: {response.text}")

@click.command()
@click.option('--name', required=True, help='The name of the secret to read')
@click.option('--version', default=None, help='Specify the version of the secret to retrieve.')
def read(name, version):
    """Retrieve a secret by name."""
    headers = {
        "X-API-KEY": os.getenv('API_KEY')
    }
    url = f"{API_URL}/secrets/{name}"
    if version:
        url += f"?version={version}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        secret = response.json()
        click.echo(f"Secret: {json.dumps(secret, indent=2)}")
    else:
        click.echo(f"Failed to retrieve secret. Error: {response.text}")

@click.command()
@click.option('--name', required=True, help='The name of the secret to delete')
def delete(name):
    """Delete a secret by name."""
    headers = {
        "X-API-KEY": os.getenv('API_KEY')
    }
    response = requests.delete(f"{API_URL}/secrets/{name}", headers=headers)
    
    if response.status_code == 204:
        click.echo(f"Secret '{name}' deleted successfully.")
    else:
        click.echo(f"Failed to delete secret. Error: {response.text}")

# Add commands to the CLI group
cli.add_command(create)
cli.add_command(update)
cli.add_command(read)
cli.add_command(delete)

if __name__ == '__main__':
    cli()
