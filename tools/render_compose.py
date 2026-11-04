"""Emit a portable Compose JSON file, also accepted as TrueNAS Custom App YAML."""
import argparse
import json

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--bind", default="127.0.0.1", help="NAS LAN address, or loopback for local Docker")
parser.add_argument("--port", type=int, default=30080)
parser.add_argument("--image", default="local/timvanhelsdingen-web:latest")
args = parser.parse_args()
compose = {
    "services": {"web": {
        "image": args.image,
        "pull_policy": "never",
        "user": "101:101",
        "restart": "unless-stopped",
        "read_only": True,
        "cap_drop": ["ALL"],
        "security_opt": ["no-new-privileges:true"],
        "tmpfs": ["/tmp:rw,noexec,nosuid,size=16m,mode=1777"],
        "mem_limit": "64m",
        "cpus": 0.5,
        "pids_limit": 64,
        "ports": [f"{args.bind}:{args.port}:8080"],
        "logging": {"driver": "json-file", "options": {"max-size": "5m", "max-file": "2"}},
    }},
}
print(json.dumps(compose, ensure_ascii=True, indent=2))
