"""
Centralized configuration directory management for Janito CLI.

All Janito configuration (config.json, auth.json, secrets.json,
mcp_services.json and the skills directory) lives under a single base
directory. By default this is ``~/.janito`` but it can be overridden at
runtime with the ``-c`` / ``--config-dir`` CLI flag (see :func:`set_config_dir`).

A project-local directory ``./.janito`` (the current working directory) is
always resolved first, falling back to the base directory (global
``~/.janito`` or the ``-c`` override) for anything not stored locally.
The ``-l`` / ``--local`` CLI flag (see :func:`set_local_config_mode`)
only selects the write target: configuration is then written to
``./.janito`` instead of the base directory. Reads merge local over base
in any case.

This module intentionally has no dependencies on other janito modules so that
it can be imported from any configuration module without risking circular
imports.
"""

from pathlib import Path

# Default base configuration directory. This is the value used when -c/--config-dir
# is not provided on the command line.
DEFAULT_CONFIG_DIR = Path.home() / ".janito"

# The effective configuration directory. Updated by :func:`set_config_dir` when
# the user passes -c/--config-dir. Defaults to :data:`DEFAULT_CONFIG_DIR`.
_config_dir: Path = DEFAULT_CONFIG_DIR

# Whether -l/--local was passed: configuration is written to ./.janito (the
# current working directory). Reads always merge ./.janito over the base
# directory; the flag only selects the write target.
_local_mode: bool = False


def get_local_config_dir() -> Path:
    """Get the project-local configuration directory (``./.janito``).

    The directory is resolved from the current working directory each time it
    is queried so that it always points at the project the user invoked
    janito from.

    Returns:
        Path: ``<cwd>/.janito``
    """
    return Path.cwd() / ".janito"


def set_config_dir(path: str | None) -> None:
    """Set the base configuration directory.

    Called early in ``main()`` when the ``-c`` / ``--config-dir`` flag is used.
    All configuration, auth and secret files are then stored/read from this
    directory instead of ``~/.janito``.

    Args:
        path: The directory to use as the base configuration directory. If
            ``None`` or empty, this is a no-op and the current directory is kept.
    """
    global _config_dir
    if not path:
        return
    _config_dir = Path(path).expanduser()


def set_local_config_mode(enabled: bool) -> None:
    """Enable or disable ``-l`` / ``--local`` mode.

    Called early in ``main()`` when the ``-l`` / ``--local`` flag is used. In
    local mode the project-local directory (``./.janito``) becomes the write
    target for all configuration. Reads always merge the project-local
    directory over the base directory (see :func:`get_config_dirs`),
    with or without the flag.

    Args:
        enabled: Whether local mode should be active.
    """
    global _local_mode
    _local_mode = bool(enabled)


def get_config_dir() -> Path:
    """Get the effective base configuration directory (the write target).

    In local mode this returns the project-local ``./.janito`` directory;
    otherwise it returns ``~/.janito`` (or the value set via
    :func:`set_config_dir`).

    Returns:
        Path: The directory that new/updated configuration is written to.
    """
    if _local_mode:
        return get_local_config_dir()
    return _config_dir


def get_config_dirs() -> list[Path]:
    """Get the configuration directories used for resolution, in priority order.

    The project-local directory (``./.janito``) always comes first and the
    base directory (global ``~/.janito`` or the ``-c`` / ``--config-dir``
    override) is the fallback. The ``-l`` / ``--local`` flag only selects
    the write target (see :func:`get_config_dir`); reads merge local over
    base in any case.

    Returns:
        List of directories to consult, highest priority first.
    """
    dirs = [get_local_config_dir()]
    if _config_dir != dirs[0]:
        dirs.append(_config_dir)
    return dirs


def get_config_file_paths(name: str) -> list[Path]:
    """Get all paths for a configuration file, in resolution priority order.

    The first entry is always the project-local path (``./.janito/<name>``)
    followed by the base path (``~/.janito/<name>`` or the ``-c`` override),
    deduplicated when both resolve to the same directory.

    Args:
        name: The file name (e.g. ``"auth.json"``).

    Returns:
        List of paths, highest priority first.
    """
    return [d / name for d in get_config_dirs()]


def get_base_config_dir() -> Path:
    """Get the base configuration directory (the ``-c``/``--config-dir`` value).

    Unlike :func:`get_config_dir`, this always returns the *base* directory
    (``~/.janito`` or the ``-c`` override) and is not affected by
    ``-l``/``--local`` mode.  Used by the task manager to reproduce the
    parent's configuration in child processes (issue #94).

    Returns:
        The base configuration directory.
    """
    return _config_dir


def is_local_config_mode() -> bool:
    """Whether ``-l``/``--local`` mode is active (issue #94).

    Returns:
        ``True`` when ``set_local_config_mode(True)`` was called (i.e. the
        user passed ``-l`` / ``--local``).
    """
    return _local_mode


def config_cli_args() -> list[str]:
    """Return the CLI flags that reproduce this process's config resolution.

    The task manager appends these to the child ``janito`` command line so
    sub-processes resolve the same configuration directory and local mode as
    the parent (issue #94).

    Returns:
        A list of flags (e.g. ``["-l", "-c", "/path/to/dir"]``), or ``[]``
        when neither ``-c`` nor ``-l`` was given.
    """
    args: list[str] = []
    if _local_mode:
        args.append("-l")
    if _config_dir != DEFAULT_CONFIG_DIR:
        args.append("-c")
        # Resolve relative -c values against the parent's cwd so they stay
        # correct even when the child runs in a different working directory.
        args.append(str(_config_dir.absolute()))
    return args
