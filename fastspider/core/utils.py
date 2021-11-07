import json
from typing import Dict


def compact_json_dumps(d: Dict) -> str:
    return json.dumps(d, separators=(',', ':'))
