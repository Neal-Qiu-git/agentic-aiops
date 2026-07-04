"""JSON报告"""
import json, os
from datetime import datetime

class JsonReporter:
    def generate(self, data, output=None):
        report = {"report_time": datetime.now().isoformat(), "data": data}
        content = json.dumps(report, indent=2, ensure_ascii=False, default=str)
        if output:
            with open(output, "w") as f: f.write(content)
        return content
