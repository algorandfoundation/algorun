# Algorun CLI

THIS IS IN BETA

## Is this for me?

This tool simplifies setting up and starting an Algorand mainnet node. You should know your way around a CLI if you're planning to use it

# Install

## Prerequisites

The key required dependency is Python 3.10+, but some of the installation options below will install that for you.

Algorun also has some runtime dependencies that also need to be available for particular commands.

- Docker - Docker Compose (and by association, Docker) is used to run the Algorand mainnet container, we require Docker Compose 2.5.0+

- Pipx - a better package manager than pip that you'll use to install the cli

## Install Algorun with pipx on any Mac, Linux and Windows subsystem for Linux

1. Ensure desired prerequisites are installed

   - [Python 3.10+](https://www.python.org/downloads/)
   - [pipx](https://pypa.github.io/pipx/installation/)
   - [Docker](https://docs.docker.com/get-docker/)

2. Install using pipx `pipx install algorun`
3. Restart the terminal to ensure Algorun is available on the path
4. [Verify installation](#verify-installation)

### Maintenance

- To update Algorun: `pipx upgrade algorun`
- To remove Algorun: `pipx uninstall algorun`

## Verify installation

Verify Algorun is installed correctly by running `algorun --version` and you should see output similar to:

```
algorun, version 0.1
```

## Usage

Create a directory where you're comfortable keeping the node config and files, we suggest naming it `algorand`, open that directory in a terminal

- `algorun start` will start your node by creating `docker-compose.yml`, `config.json` files and a `data` directory where your node will persist.
- `algorun stop` will shut down your node
- `algorun goal` is a wrapper for the [Goal CLI](https://developer.algorand.org/docs/clis/goal/goal/)
- typing `algorun goal node status` will return your nodes status, typing `algorun goal node status -w 1000` instead will keep giving you node status updates every 1 second

> **Note**
> If you get receive one of the following errors:
>
> - `command not found: algorun` (bash/zsh)
> - `The term 'algorun' is not recognized as the name of a cmdlet, function, script file, or operable program.` (PowerShell)
>
> Then ensure that `algorun` is available on the PATH by running `pipx ensurepath` and restarting the terminal.

If you're experiencing issues with algorun [raise an issue](https://github.com/algorandfoundation/algorun/issues/new).
