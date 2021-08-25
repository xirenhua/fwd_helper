import json
import click
import subprocess


@click.command()
@click.option(
    "-l",
    "--local_ports",
    help="List of local forwarding ports in json format",
)
@click.option(
    "-r",
    "--remote_ports",
    help="List of remote forwarding ports in json format",
)
@click.argument("host")
def fwd(local_ports, remote_ports, host):
    """SSH port forwarding helper"""
    stat = ["autossh", "-M", "0", "-N"]
    if local_ports:
        local_ports = json.loads(local_ports)
        assert isinstance(local_ports, list), "local_ports should be a json list"
        assert isinstance(local_ports[0], int), "ports should be integers"
        for port in local_ports:
            stat += ["-L", f"{port}:localhost:{port}"]

    if remote_ports:
        remote_ports = json.loads(remote_ports)
        assert isinstance(remote_ports, list), "remote_ports should be a json list"
        assert isinstance(remote_ports[0], int), "ports should be integers"
        for port in remote_ports:
            stat += ["-R", f"{port}:localhost:{port}"]

    stat += [f"{host}"]

    subprocess.run(args=stat)


if __name__ == "__main__":
    fwd()
