import click
import requests
import os
import json

BASE_URL = "https://trialnr323w.jfrog.io/artifactory"
CONFIG_FILE = os.path.expanduser("~/.artifactory_cli_config")

def save_config(username, access_token, expires_in):
    config = {
        "username": username,
        "access_token": access_token,
        "expires_in": expires_in,
        "api_key": os.environ["API_KEY"],
        "url": "https://trialnr323w.jfrog.io/artifactory",
        "admin_url": "https://trialnr323w.jfrog.io"
    }
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

def load_config():
    """Load saved configuration"""
    if not os.path.exists(CONFIG_FILE):
        click.echo("You are not logged in. Please run the 'login' command first.")
        return None
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

@click.group()
def cli():
    """Artifactory CLI Tool"""
    pass

@cli.command('login')
@click.option('--username', prompt='Username', help='Username')
@click.option('--password', prompt='Password', hide_input=True, help='Password')
def authenticate(username, password):
    """Login and save credentials locally"""
    url = f"{BASE_URL}/api/security/token"
    headers = {'Authorization': f"Bearer os.environ["API_KEY"]"}
    payload = {
        "username": username,
        "password": password,
        "scope": "member-of-groups:*",
        "expires_in": 3600
    }
    response = requests.post(url, data=payload, headers=headers)
    if response.status_code == 200:
        token = response.json().get("access_token")
        save_config(username, token, url)
        click.echo("Authentication successful!")
    else:
        click.echo("Authentication failed!", response.text)

@cli.command()
def hello():
    """Prints Hello, author: Oshane Williams!"""
    click.echo("Hello, hoe you enjoy using this artifactory cli!")

@cli.command("get-repos")
def get_repos():
    """Fetch and list repositories from Artifactory"""
    config = load_config()
    if not config:
        return
    url, token = config['url'], config['token']
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f"{url}/api/repositories", headers=headers)
    if response.status_code == 200:
        repos = response.json()
        for repo in repos:
            click.echo(f"Repo: {repo['key']}")
    else:
        click.echo(f"Failed to fetch repositories: {response.status_code}")

@cli.command()
def ping():
    """Ping Artifactory"""
    config = load_config()
    if not config:
        return
    url, token = config['url'], config['token']
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f"{url}/api/system/ping", headers=headers)
    if response.status_code == 200:
        click.echo("Ping Response:", response.text)
    else:
        click.echo(f"Failed to ping artifactory url: {response.status_code}")

@cli.command()
def system_info():
    """Ping Artifactory"""
    config = load_config()
    if not config:
        return
    url, token = config['url'], config['token']
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f"{url}/api/system/version", headers=headers)
    if response.status_code == 200:
        click.echo("System Info Response:", response.text)
    else:
        click.echo(f"Failed to get system info: {response.status_code}")

@cli.command("get-user")
@click.option('--username', prompt='Username', help='Username')
def get_user(username):
    """Get User Details Artifactory"""
    config = load_config()
    if not config:
        return
    url, access_token = config['admin_url'], config['api_key']
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(f"{url}/artifactory/api/security/users/{username}", headers=headers)
    if response.status_code == 200:
        click.echo(f"User Response: {response.text}")
    else:
        click.echo(f"Failed to fetch user: {response.text}")

@cli.command("create-user")
@click.option('--username', prompt='Username', help='Username')
@click.option('--password', prompt='Password', help="User's Password", hide_input=True)
@click.option('--email', prompt='Email', help='User\'s email address')
def create_user(username, password, email):
    """Create User Artifactory"""

    config = load_config()

    if not config:
        return
    
    url, access_token = config['admin_url'], config['api_key']

    headers = {'Authorization': f'Bearer {access_token}','Content-Type': 'application/json'}

    is_admin = click.confirm('--is_admin', default=False)

    payload = {
        "username": username,
        "password": password,
        "email": email,
        "is_admin": is_admin,
        "profile_updatable": True,
        "internal_password_disabled": False,
        "disable_ui_access": False
    }

    response = requests.post(f"{url}/access/api/v2/users", json=payload, headers=headers)

    if response.status_code == 201:
        click.echo(f"Successfully created user response: {response.text}")
    else:
        click.echo(f"Failed to create user: {response.text}")

@cli.command("update-user")
@click.option('--username', prompt='Username', help='Username')
@click.option('--email', prompt='Email', help='User\'s email address', default=None, show_default=True)
def update_user(username, password, email):
    """Update User Artifactory"""

    config = load_config()

    if not config:
        return
    
    url, access_token = config['admin_url'], config['api_key']

    headers = {'Authorization': f'Bearer {access_token}','Content-Type': 'application/json'}

    is_admin = click.confirm('--is_admin', default=False)

    payload = {
        "username": username,
        "password": password,
        "email": email,
        "is_admin": is_admin,
        "profile_updatable": True,
        "internal_password_disabled": False,
        "disable_ui_access": False
    }

    response = requests.patch(f"{url}/access/api/v2/users", json=payload, headers=headers)

    if response.status_code == 201:
        click.echo(f"Successfully created user response: {response.text}")
    else:
        click.echo(f"Failed to create user: {response.text}")

@cli.command("delete-user")
@click.option('--username', prompt='Username', help='Username')
def delete_user(username):
    """Delete User Artifactory"""
    config = load_config()
    if not config:
        return
    url, access_token = config['admin_url'], config['api_key']
    headers = {'Authorization': f'Bearer {access_token}'}
   
    response = requests.delete(f"{url}/access/api/v2/users/{username}", headers=headers)

    if response.status_code == 204:
        click.echo(f"Successfully deleted {username}")
    else:
        click.echo(f"Failed to fetch user: {response.text}")

@cli.command("create-repo")
@click.option("--repokey", prompt="Enter a repokey", help="Enter a repokey for the repository")
def create_repokey(repokey):
    """Create repository from Artifactory"""
    config = load_config()

    if not config:
        return
    
    url, token = config['url'], config['api_key']

    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}

    payload = {
        "rclass": "local",
        "packageType": "docker",
        "description": "Local Docker repository",
        "repoLayoutRef": "simple-default",
        "dockerApiVersion": "V2"
    }

    response = requests.put(f"{url}/api/repositories/{repokey}", json=payload,headers=headers)

    if response.status_code == 200:
        click.echo(f"Repo: {response.text}") 
    else:
        click.echo(f"Failed to fetch repositories: {response.status_code}")

@cli.command("update-repo")
@click.option("--repokey", prompt="Enter a repokey", help="Enter a repokey for the repository")
def update_repokey(repokey):
    """Update repository from Artifactory"""
    config = load_config()

    if not config:
        return
    
    url, token = config['url'], config['api_key']

    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}

    payload = {
        "rclass": "local",
        "packageType": "docker",
        "description": "Local Docker repository",
        "repoLayoutRef": "simple-default",
        "dockerApiVersion": "V2"
    }

    response = requests.put(f"{url}/api/repositories/{repokey}", json=payload,headers=headers)
    
    if response.status_code == 200:
        click.echo(f"Repo: {response.text}") 
    else:
        click.echo(f"Failed to fetch repositories: {response.status_code}")

if __name__ == '__main__':
    cli()
