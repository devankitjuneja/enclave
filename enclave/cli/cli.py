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
@click.argument('key')
@click.argument('value')
def create(key, value):
    """Create a new secret."""
    payload = {
        "name": key,
        "value": value
    }
    headers = {
        "X-API-KEY": os.getenv('API_KEY')
    }
    response = requests.post(f"{API_URL}/secrets", json=payload, headers=headers)

    if response.status_code == 200:
        click.echo(f"Secret '{key}' created successfully.")
    else:
        click.echo(f"Failed to create secret. Error: {response.text}")

@click.command()
@click.argument('key')
@click.argument('value')
def update(key, value):
    """Update an existing secret"""
    payload = {
        "value": value
    }
    headers = {
        "X-API-KEY": os.getenv('API_KEY')
    }
    response = requests.put(f"{API_URL}/secrets/{key}", json=payload, headers=headers)

    if response.status_code == 200:
        click.echo(f"Secret '{key}' updated successfully.")
    else:
        click.echo(f"Failed to update secret. Error: {response.text}")

@click.command()
@click.argument('key')
@click.option('--version', default=None, help='Specify the version of the secret to retrieve.')
def read(key, version):
    """Retrieve a secret by name."""
    headers = {
        "X-API-KEY": os.getenv('API_KEY')
    }
    response = requests.get(f"{API_URL}/secrets/{key}", headers=headers)
    if version:
        response = requests.get(f"{API_URL}/secrets/{key}?version={version}", headers=headers)

    if response.status_code == 200:
        secret = response.json()
        click.echo(f"Secret: {json.dumps(secret, indent=2)}")
    else:
        click.echo(f"Failed to retrieve secret. Error: {response.text}")

@click.command()
@click.argument('key')
def delete(key):
    """Delete a secret by name."""
    headers = {
        "X-API-KEY": os.getenv('API_KEY')
    }
    response = requests.delete(f"{API_URL}/secrets/{key}", headers=headers)
    
    if response.status_code == 204:
        click.echo(f"Secret '{key}' deleted successfully.")
    else:
        click.echo(f"Failed to delete secret. Error: {response.text}")

# Add commands to the CLI group
cli.add_command(create)
cli.add_command(update)
cli.add_command(read)
cli.add_command(delete)

if __name__ == '__main__':
    cli()
