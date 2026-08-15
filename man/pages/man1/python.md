# python - Python Commands

## NAME

python [py] - Python commands (run, compile, debug, env, path)

## DESCRIPTION

The python command provides access to Python execution and management capabilities within TerminalX. Run Python scripts, compile code, debug applications, and manage Python environment with 26 available commands.

## SYNOPSIS

```
python run <script>
python compile <file>
python debug <script>
python env list
python env set <var> <value>
python env unset <var>
python path show
python path add <dir>
python path remove <dir>
python version
python packages list
python packages install <package>
python packages uninstall <package>
python packages update <package>
python packages freeze
python packages outdated
python shell
python exec <command>
python profile <script>
python test <module>
python lint <file>
python format <file>
```

## OPTIONS

- `run <script>` - Run a Python script
- `compile <file>` - Compile Python file
- `debug <script>` - Debug Python script
- `env list` - List Python environment variables
- `env set <var> <value>` - Set environment variable
- `path show` - Show Python path
- `path add <dir>` - Add directory to Python path
- `version` - Show Python version
- `packages list` - List installed packages
- `packages install <package>` - Install Python package

## EXAMPLES

```
python run script.py
python compile module.py
python debug app.py
python env list
python packages install numpy
```

## SEE ALSO

man(1), dev(1), build(1)

## AUTHOR

Sebastian Januchowski - polsoft.ITS™ Dev
