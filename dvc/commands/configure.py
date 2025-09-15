import argparse
import os
from dvc.cli.command import CmdBase

CONFIG_FILE = os.path.expanduser("~/.dvc_enhance_config.json")

def load_config():
    if os.path.exists(CONFIG_FILE):
        import json
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}

def save_config(cfg):
    import json
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f, indent=2)

def add_parser(subparsers, parent_parser):
    parser = subparsers.add_parser(
        "configure",
        parents=[parent_parser],
        description="Configure DVC enhance global log path.",
        help="Configure DVC enhance global log path.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--global-log-path", type=str, default=None, help="Set the global log file path (default: ~/.dvc_push_history_global.json)"
    )
    parser.set_defaults(func=CmdConfigure)
    return parser

class CmdConfigure(CmdBase):
    def run(self):
        cfg = load_config()
        path = getattr(self.args, "global_log_path", None)
        if path:
            cfg["global_log_path"] = os.path.expanduser(path)
            save_config(cfg)
            print(f"Set global log path to: {cfg['global_log_path']}")
        else:
            print("Current config:")
            for k, v in cfg.items():
                print(f"  {k}: {v}")
        return 0
