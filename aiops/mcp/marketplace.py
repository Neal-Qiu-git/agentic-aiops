"""MCP Marketplace - 工具市场"""
import logging
from typing import Any, Dict, List, Optional
from .base import BaseMCPTool, MCPToolInfo, MCPCapability

logger = logging.getLogger(__name__)


class MCPMarketplace:
    """MCP 工具市场"""

    def __init__(self):
        self._tools: Dict[str, BaseMCPTool] = {}
        self._categories: Dict[str, List[str]] = {}
        self._tags: Dict[str, List[str]] = {}

    def register_tool(self, tool: BaseMCPTool):
        """注册工具"""
        info = tool.get_info()
        self._tools[info.name] = tool

        # 更新分类索引
        if info.category:
            if info.category not in self._categories:
                self._categories[info.category] = []
            if info.name not in self._categories[info.category]:
                self._categories[info.category].append(info.name)

        # 更新标签索引
        for tag in info.tags:
            if tag not in self._tags:
                self._tags[tag] = []
            if info.name not in self._tags[tag]:
                self._tags[tag].append(info.name)

        logger.info(f"注册 MCP 工具: {info.name} v{info.version}")

    def unregister_tool(self, tool_name: str):
        """注销工具"""
        if tool_name in self._tools:
            info = self._tools[tool_name].get_info()
            del self._tools[tool_name]

            # 更新分类索引
            if info.category and info.category in self._categories:
                if tool_name in self._categories[info.category]:
                    self._categories[info.category].remove(tool_name)

            # 更新标签索引
            for tag in info.tags:
                if tag in self._tags and tool_name in self._tags[tag]:
                    self._tags[tag].remove(tool_name)

            logger.info(f"注销 MCP 工具: {tool_name}")

    def get_tool(self, tool_name: str) -> Optional[BaseMCPTool]:
        """获取工具"""
        return self._tools.get(tool_name)

    def list_tools(self, category: str = None, tag: str = None,
                   capability: MCPCapability = None) -> List[MCPToolInfo]:
        """
        列出工具

        Args:
            category: 分类过滤
            tag: 标签过滤
            capability: 能力过滤

        Returns:
            工具信息列表
        """
        tools = []

        # 获取工具名称列表
        if category and category in self._categories:
            tool_names = self._categories[category]
        elif tag and tag in self._tags:
            tool_names = self._tags[tag]
        else:
            tool_names = list(self._tools.keys())

        # 过滤
        for name in tool_names:
            tool = self._tools.get(name)
            if not tool:
                continue

            info = tool.get_info()

            # 能力过滤
            if capability and capability not in info.capabilities:
                continue

            # 只返回启用的工具
            if info.enabled:
                tools.append(info)

        return tools

    def execute_tool(self, tool_name: str, command: str, **kwargs) -> Dict[str, Any]:
        """执行工具"""
        tool = self._tools.get(tool_name)
        if not tool:
            return {"success": False, "error": f"工具不存在: {tool_name}"}

        try:
            result = tool.execute(command, **kwargs)
            return {"success": True, "result": result}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def query_tool(self, tool_name: str, query: str, **kwargs) -> Dict[str, Any]:
        """查询工具"""
        tool = self._tools.get(tool_name)
        if not tool:
            return {"success": False, "error": f"工具不存在: {tool_name}"}

        try:
            result = tool.query(query, **kwargs)
            return {"success": True, "result": result}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def search_tools(self, keyword: str) -> List[MCPToolInfo]:
        """搜索工具"""
        results = []
        keyword_lower = keyword.lower()

        for tool in self._tools.values():
            info = tool.get_info()
            # 搜索名称、描述、标签
            if (keyword_lower in info.name.lower() or
                keyword_lower in info.description.lower() or
                any(keyword_lower in tag.lower() for tag in info.tags)):
                results.append(info)

        return results

    def get_tools_by_capability(self, capability: MCPCapability) -> List[MCPToolInfo]:
        """获取具有某种能力的工具"""
        return self.list_tools(capability=capability)

    def get_categories(self) -> List[str]:
        """获取所有分类"""
        return list(self._categories.keys())

    def get_tags(self) -> List[str]:
        """获取所有标签"""
        return list(self._tags.keys())

    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            "total_tools": len(self._tools),
            "categories": {cat: len(tools) for cat, tools in self._categories.items()},
            "tags": {tag: len(tools) for tag, tools in self._tags.items()},
            "enabled_tools": sum(1 for t in self._tools.values() if t.get_info().enabled),
        }


# 全局 MCP Marketplace 实例
_global_marketplace: Optional[MCPMarketplace] = None


def get_marketplace() -> MCPMarketplace:
    """获取全局 MCP Marketplace"""
    global _global_marketplace
    if _global_marketplace is None:
        _global_marketplace = MCPMarketplace()
    return _global_marketplace
