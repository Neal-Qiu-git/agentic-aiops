"""CI/CD 工具 - Jenkins / GitLab CI / GitHub Actions

Jenkins: 传统 CI/CD 霸主，40%+ 企业仍在使用
GitLab CI: DevOps 全平台，增长最快
GitHub Actions: 开源/中小项目首选
"""
import json
import logging
import subprocess
from .base import BaseTool, ToolResult, ToolCategory

logger = logging.getLogger(__name__)


def _ci_cmd(cmd: str, timeout: int = 30) -> ToolResult:
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return ToolResult(success=(r.returncode == 0), output=r.stdout.strip()[:8000],
                          error=r.stderr.strip() if r.returncode != 0 else "")
    except Exception as e:
        return ToolResult(success=False, error=str(e))


class JenkinsJob(BaseTool):
    """Jenkins 作业管理"""
    name = "jenkins_job"
    description = "查看/触发 Jenkins 构建任务"
    category = ToolCategory.CICD
    parameters = {"type": "object", "properties": {
        "action": {"type": "string", "description": "list/build/status/log", "default": "list"},
        "job": {"type": "string", "description": "Job 名称"},
        "build_number": {"type": "integer", "description": "构建号"},
    }}

    def execute(self, action: str = "list", job: str = "", build_number: int = 0, **kwargs) -> ToolResult:
        import os
        url = os.environ.get("JENKINS_URL", "http://localhost:8080")
        user = os.environ.get("JENKINS_USER", "")
        token = os.environ.get("JENKINS_TOKEN", "")
        auth = f"-u {user}:{token}" if user else ""
        if action == "list":
            return _ci_cmd(f"curl -s {auth} '{url}/api/json?tree=jobs[name,url,color]'")
        if action == "build" and job:
            return _ci_cmd(f"curl -s -X POST {auth} '{url}/job/{job}/buildWithParameters'", timeout=60)
        if action == "status" and job:
            bn = build_number or "lastBuild"
            return _ci_cmd(f"curl -s {auth} '{url}/job/{job}/{bn}/api/json'")
        if action == "log" and job:
            bn = build_number or "lastBuild"
            return _ci_cmd(f"curl -s {auth} '{url}/job/{job}/{bn}/consoleText'")
        return ToolResult(success=False, error="参数不足")


class GitLabCI(BaseTool):
    """GitLab CI/CD 管理"""
    name = "gitlab_ci"
    description = "查看/触发 GitLab CI 流水线"
    category = ToolCategory.CICD
    parameters = {"type": "object", "properties": {
        "action": {"type": "string", "description": "list/pipelines/jobs/trigger", "default": "list"},
        "project_id": {"type": "string", "description": "项目 ID 或路径"},
        "pipeline_id": {"type": "integer"},
        "ref": {"type": "string", "description": "分支名", "default": "main"},
    }}

    def execute(self, action: str = "list", project_id: str = "",
                pipeline_id: int = 0, ref: str = "main", **kwargs) -> ToolResult:
        import os
        url = os.environ.get("GITLAB_URL", "https://gitlab.com")
        token = os.environ.get("GITLAB_TOKEN", "")
        auth = f"-H 'PRIVATE-TOKEN: {token}'" if token else ""
        if action == "pipelines" and project_id:
            return _ci_cmd(f"curl -s {auth} '{url}/api/v4/projects/{project_id}/pipelines?per_page=20'")
        if action == "jobs" and project_id:
            if pipeline_id:
                return _ci_cmd(f"curl -s {auth} '{url}/api/v4/projects/{project_id}/pipelines/{pipeline_id}/jobs'")
            return _ci_cmd(f"curl -s {auth} '{url}/api/v4/projects/{project_id}/jobs?per_page=20'")
        if action == "trigger" and project_id:
            return _ci_cmd(f"curl -s -X POST {auth} '{url}/api/v4/projects/{project_id}/pipeline' -d 'ref={ref}'")
        return _ci_cmd(f"curl -s {auth} '{url}/api/v4/projects?per_page=20'")


class GitHubActions(BaseTool):
    """GitHub Actions 管理"""
    name = "github_actions"
    description = "查看/触发 GitHub Actions 工作流"
    category = ToolCategory.CICD
    parameters = {"type": "object", "properties": {
        "action": {"type": "string", "description": "list/runs/trigger", "default": "list"},
        "repo": {"type": "string", "description": "owner/repo"},
        "workflow_id": {"type": "string", "description": "工作流 ID 或文件名"},
        "ref": {"type": "string", "default": "main"},
    }}

    def execute(self, action: str = "list", repo: str = "",
                workflow_id: str = "", ref: str = "main", **kwargs) -> ToolResult:
        token = subprocess.run("gh auth token 2>/dev/null", shell=True, capture_output=True, text=True).stdout.strip()
        if not token:
            import os
            token = os.environ.get("GITHUB_TOKEN", "")
        auth = f"-H 'Authorization: token {token}'" if token else ""
        api = "https://api.github.com"
        if action == "list" and repo:
            return _ci_cmd(f"curl -s {auth} '{api}/repos/{repo}/actions/workflows?per_page=20'")
        if action == "runs" and repo:
            return _ci_cmd(f"curl -s {auth} '{api}/repos/{repo}/actions/runs?per_page=20'")
        if action == "trigger" and repo and workflow_id:
            return _ci_cmd(f"curl -s -X POST {auth} '{api}/repos/{repo}/actions/workflows/{workflow_id}/dispatches' "
                           f"-H 'Content-Type: application/json' -d '{{\"ref\":\"{ref}\"}}'")
        return ToolResult(success=False, error="参数不足")
