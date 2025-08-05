"""
Link Header Builder for st-aggrid

This module provides utilities to create column definitions with custom header components
that display a link icon and allow clicking to navigate to a URL.
"""

from typing import Dict, Any, Optional
from st_aggrid.shared import JsCode


class LinkHeaderBuilder:
    """
    Builder class for creating column definitions with link header components.
    """
    
    @staticmethod
    def create_link_column(
        field: str,
        header_name: str,
        url: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        创建一个带有链接功能的列定义
        
        Args:
            field: 数据字段名
            header_name: 列标题名
            url: 点击链接时要跳转的URL
            **kwargs: 其他列配置参数
            
        Returns:
            包含自定义headerComponent的列定义字典
        """
        # 确保排序和过滤功能被启用
        default_config = {
            "sortable": True,
            "filter": True,
            "resizable": True,
            "suppressHeaderContextMenu": False  # 显示列菜单（包含过滤选项）
        }
        
        # 合并默认配置和用户提供的配置
        column_config = {**default_config, **kwargs}
        
        column_def = {
            "field": field,
            "headerName": header_name,
            "headerComponentParams": {
                "innerHeaderComponent": "linkHeaderComponent",
                "url": url,
                "headerName": header_name
            },
            **column_config
        }
        
        return column_def
    
    @staticmethod
    def create_link_columns_from_dict(
        link_config: Dict[str, str],
        **default_kwargs
    ) -> Dict[str, Dict[str, Any]]:
        """
        从字典配置批量创建链接列定义
        
        Args:
            link_config: 格式为 {field_name: url} 的字典
            **default_kwargs: 默认的列配置参数
            
        Returns:
            列定义字典的字典
        """
        columns = {}
        
        for field, url in link_config.items():
            # 使用字段名作为默认的header_name
            header_name = field.replace('_', ' ').title()
            
            columns[field] = LinkHeaderBuilder.create_link_column(
                field=field,
                header_name=header_name,
                url=url,
                **default_kwargs
            )
        
        return columns


def add_link_headers_to_grid_options(
    grid_options: Dict[str, Any],
    link_config: Dict[str, str],
    **default_kwargs
) -> Dict[str, Any]:
    """
    向现有的gridOptions中添加链接列配置
    
    Args:
        grid_options: 现有的gridOptions配置
        link_config: 格式为 {field_name: url} 的字典
        **default_kwargs: 默认的列配置参数
        
    Returns:
        更新后的gridOptions
    """
    if "columnDefs" not in grid_options:
        grid_options["columnDefs"] = []
    
    # 创建链接列定义
    link_columns = LinkHeaderBuilder.create_link_columns_from_dict(
        link_config, **default_kwargs
    )
    
    # 将链接列添加到columnDefs中
    for field, column_def in link_columns.items():
        # 检查是否已存在该字段的列定义
        existing_index = None
        for i, col in enumerate(grid_options["columnDefs"]):
            if col.get("field") == field:
                existing_index = i
                break
        
        if existing_index is not None:
            # 更新现有的列定义
            grid_options["columnDefs"][existing_index].update(column_def)
        else:
            # 添加新的列定义
            grid_options["columnDefs"].append(column_def)
    
    return grid_options


# 便捷函数
def create_link_column(field: str, header_name: str, url: str, **kwargs) -> Dict[str, Any]:
    """便捷函数：创建单个链接列定义"""
    return LinkHeaderBuilder.create_link_column(field, header_name, url, **kwargs)


def create_link_columns(link_config: Dict[str, str], **default_kwargs) -> Dict[str, Dict[str, Any]]:
    """便捷函数：批量创建链接列定义"""
    return LinkHeaderBuilder.create_link_columns_from_dict(link_config, **default_kwargs) 