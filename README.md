# Algorun CLI

## Is this for me?

The target audience for this tool is software developers building applications on the Algorand network. A working knowledge of using a command line interfaces and experience using the supported programming languages is assumed.

# Install

## Prerequisites

The key required dependency is Python 3.10+, but some of the installation options below will install that for you.

Algorun also has some runtime dependencies that also need to be available for particular commands.

- Docker - Docker Compose (and by association, Docker) is used to run the Algorand mainnet container, we require Docker Compose 2.5.0+

## Install Algorun with pipx on any Mac, Linux and Windows subsystem for Linux

1. Ensure desired prerequisites are installed

   - [Python 3.10+](https://www.python.org/downloads/)
   - [pipx](https://pypa.github.io/pipx/installation/)
   - [Docker](https://docs.docker.com/get-docker/)

2. Install using pipx `pipx install algorun`
3. Restart the terminal to ensure AlgoKit is available on the path
4. [Verify installation](#verify-installation)

### Maintenance

- To update Algorun: `pipx upgrade algorun`
- To remove Algorun: `pipx uninstall algorun`

## Verify installation

Verify AlgoKit is installed correctly by running `algorun --version` and you should see output similar to:

```
algorun, version 0.1
```

> **Note**
> If you get receive one of the following errors:
>
> - `command not found: algorun` (bash/zsh)
> - `The term 'algorun' is not recognized as the name of a cmdlet, function, script file, or operable program.` (PowerShell)
>
> Then ensure that `algorun` is available on the PATH by running `pipx ensurepath` and restarting the terminal.

If you're experiencing issues with algorun [raise an issue](https://github.com/algorandfoundation/algokit-cli/issues/new).
