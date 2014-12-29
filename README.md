# Botnet modules
Modules for [Botnet](https://github.com/boreq/botnet).

## Usage
Install this package and include a module name prefixed with `botnet_modules.`
in your config:


    {
        "modules": ["irc", "botnet_modules.tell"],
        "module_config": {
            "irc": {
                ...
            },
            "tell": {
                "data_file": "/path/to/data.json"
            }
        }
    }
