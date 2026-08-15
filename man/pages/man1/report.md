# report - TerminalX Report Engine v1.0.0

## NAME

report - advanced report engine with plugin system for TerminalX

## DESCRIPTION

The report command is the TerminalX report engine with a comprehensive plugin system. It provides advanced report generation capabilities including template-based reports, multiple output formats, filtering, post-processing, and full integration with TerminalX's logging and notification systems.

## SYNOPSIS

```
report create <title>
report template <template_name> [json_data]
report render <report_id> <format>
report save <report_id> <filepath> [format]
report display <report_id> [format]
report plugins
report formats
report list
report add_section <report_id> <title> <content> [level]
report enable
report disable
report commands
```

## OPTIONS

- `create <title>` - Create a new empty report with specified title.
- `template <template_name> [json_data]` - Generate report from template with optional JSON data (file or string).
- `render <report_id> <format>` - Render report to specific format (txt, md, json).
- `save <report_id> <filepath> [format]` - Save report to file in specified format.
- `display <report_id> [format]` - Display report in terminal with ANSI colors.
- `plugins` - List all available plugins (template, output, filter, post-process).
- `formats` - List supported output formats.
- `list` - List all created reports.
- `add_section <report_id> <title> <content> [level]` - Add section to existing report.
- `enable` - Enable report engine.
- `disable` - Disable report engine.
- `commands` - Display list of available report commands.

## EXAMPLES

```
report create "System Status Report"
report template simple_template '{"title": "Daily Report", "sections": [{"title": "Overview", "content": "System is running normally"}]}'
report render <report_id> json
report save <report_id> /tmp/report.txt txt
report display <report_id>
report plugins
report formats
report list
report add_section <report_id> "Network Status" "All connections active" 2
```

## PLUGIN SYSTEM

The report engine supports four types of plugins:

### Template Plugins
Generate reports from predefined templates.
- **simple_template**: Basic template with header and sections from data

### Output Plugins
Render reports to different formats.
- **basic_text_output**: TXT and MD formats
- **json_output**: JSON format

### Filter Plugins
Modify report content before rendering.
- **uppercase_filter**: Convert content to uppercase

### Post-Process Plugins
Actions after report generation.
- **logging_postprocess**: Log report generation details

## SUPPORTED FORMATS

- **txt** - Plain text format
- **md** - Markdown format
- **json** - JSON format

## CONFIGURATION

The report engine can be configured via the main TerminalX configuration file:

```json
{
  "report": {
    "enabled": true,
    "plugin_paths": [],
    "default_format": "txt",
    "allow_unknown_format": false,
    "terminal_integration_enabled": true,
    "metadata_defaults": {}
  }
}
```

## FILES

- `~/.terminalx/config/report/report.json` - Report engine configuration
- `report/report_engine.py` - Report engine implementation
- `commands/report.py` - Report command handlers

## SEE ALSO

help(1), commands(1), terminal(1), version(1)

## AUTHOR

Sebastian Januchowski - polsoft.ITS™ Dev
