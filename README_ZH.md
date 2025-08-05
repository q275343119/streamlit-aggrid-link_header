# Streamlit Aggrid SDK 自定义链接表头组件

[English](./README.md) | [中文](#概述)

---

## 概述

本SDK扩展了`st-aggrid`库，添加了自定义链接表头组件，允许您在列标题中添加可点击的链接图标。该组件保留了所有默认的`ag-grid`功能，包括排序、筛选和调整大小。

## 功能特性

- 🔗 **自定义链接表头**: 在列标题中添加可点击的链接图标
- 📊 **完整网格功能**: 保持排序、筛选和调整大小功能
- 🎯 **事件隔离**: 点击链接图标不会干扰排序/筛选
- 🛠️ **易于集成**: 创建链接列的简单API
- 📦 **跨平台支持**: 支持Windows和HuggingFace环境

## 构建SDK

### 环境要求

- Python 3.8+
- Node.js 16+
- Yarn 或 npm

### 构建流程

1. **安装依赖**
   ```bash
   # 安装Python依赖
   pip install -r requirements.txt
   
   # 安装Node.js依赖
   cd st_aggrid/frontend
   npm install
   ```

2. **构建前端**
   ```bash
   cd st_aggrid/frontend
   npm run build
   ```

3. **构建SDK包**
   ```bash
   # 运行构建脚本
   python build_sdk.py
   ```

构建脚本将：
- 构建前端资源
- 为Windows和HuggingFace环境创建wheel包
- 在`sdk_output/`目录中生成SDK输出

### 构建输出

构建成功后，您将找到：
- `sdk_output/windows/` - Windows环境SDK
- `sdk_output/huggingface/` - HuggingFace环境SDK

每个目录包含：
- `streamlit_aggrid-1.1.7-py3-none-any.whl` - Wheel包
- `install.bat` (Windows) 或 `install.sh` (HuggingFace) - 安装脚本
- `README.md` - 安装说明

## 安装

```bash
# 从本地wheel文件安装
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple dist/streamlit_aggrid-1.1.7-py3-none-any.whl
```

## 快速开始

```python
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.link_header_builder import create_link_column

# 示例数据
data = {
    'name': ['Alice', 'Bob', 'Charlie'],
    'email': ['alice@example.com', 'bob@example.com', 'charlie@example.com'],
    'github': ['alice-github', 'bob-github', 'charlie-github'],
    'age': [25, 30, 35]
}
df = pd.DataFrame(data)

# 创建链接列
email_column = create_link_column(
    field='email',
    header_name='邮箱',
    url='mailto:{email}',
    sortable=True,
    filter=True
)

github_column = create_link_column(
    field='github',
    header_name='GitHub',
    url='https://github.com/{github}',
    sortable=True,
    filter=True
)

# 构建网格选项
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_column('name', sortable=True, filter=True)
gb.configure_column('age', sortable=True, filter=True)

# 将链接列添加到网格选项
grid_options = gb.build()
grid_options['columnDefs'].append(email_column)
grid_options['columnDefs'].append(github_column)

# 显示网格
grid_response = AgGrid(
    df,
    gridOptions=grid_options,
    data_return_mode='AS_INPUT',
    update_mode='MODEL_CHANGED',
    fit_columns_on_grid_load=True,
    theme='streamlit'
)
```

## API 参考

### `create_link_column(field, header_name, url, **kwargs)`

创建带有自定义链接表头的列定义。

**参数:**
- `field` (str): 数据字段名
- `header_name` (str): 列标题名
- `url` (str): 链接的URL模板（支持{field}占位符）
- `**kwargs`: 其他列配置选项

**返回:**
- `dict`: 列定义字典

### `create_link_columns(link_config, **default_kwargs)`

从配置字典创建多个链接列。

**参数:**
- `link_config` (dict): 字段名到URL的映射字典
- `**default_kwargs`: 所有列的默认配置

**返回:**
- `dict`: 列定义字典

### `add_link_headers_to_grid_options(grid_options, link_config, **default_kwargs)`

向现有的网格选项添加链接列配置。

**参数:**
- `grid_options` (dict): 现有的网格选项
- `link_config` (dict): 字段名到URL的映射字典
- `**default_kwargs`: 所有列的默认配置

**返回:**
- `dict`: 更新后的网格选项

## 高级用法

### 批量创建列

```python
# 定义链接配置
link_config = {
    'email': 'mailto:{email}',
    'website': 'https://{website}',
    'github': 'https://github.com/{github}'
}

# 一次性创建所有链接列
link_columns = create_link_columns(link_config, sortable=True, filter=True)

# 添加到网格选项
for column_def in link_columns.values():
    grid_options['columnDefs'].append(column_def)
```

### 动态URL生成

```python
# 带有动态字段替换的URL
email_column = create_link_column(
    field='email',
    header_name='联系方式',
    url='mailto:{email}?subject=来自{name}的问候',
    sortable=True,
    filter=True
)
```

## 配置选项

支持所有标准的`ag-grid`列选项：

- `sortable`: 启用/禁用排序
- `filter`: 启用/禁用筛选
- `resizable`: 启用/禁用列调整大小
- `suppressHeaderContextMenu`: 显示/隐藏表头上下文菜单
- `width`: 设置列宽度
- `minWidth`: 设置最小列宽度
- `maxWidth`: 设置最大列宽度

## 示例

查看`test_streamlit_app.py`获取完整的工作示例。

## 注意事项

1. **URL模板**: URL支持使用`{field}`占位符，会被实际数据替换
2. **事件处理**: 点击🔗图标会阻止事件冒泡，不会触发排序
3. **样式**: 链接图标使用默认颜色，与表头文本保持一致
4. **兼容性**: 与所有`ag-grid`功能完全兼容

## 故障排除

**问题**: 链接图标不显示
- 检查是否正确导入了`create_link_column`函数
- 确认列定义已正确添加到`grid_options['columnDefs']`

**问题**: 排序/筛选功能丢失
- 确保在`create_link_column`中设置了`sortable=True`和`filter=True`
- 检查是否正确使用了`headerComponentParams`结构

**问题**: 点击链接无响应
- 验证URL格式是否正确
- 检查浏览器控制台是否有JavaScript错误

## 使用场景

### 1. 邮件链接
```python
email_column = create_link_column(
    field='email',
    header_name='邮箱',
    url='mailto:{email}',
    sortable=True,
    filter=True
)
```

### 2. 网站链接
```python
website_column = create_link_column(
    field='website',
    header_name='网站',
    url='https://{website}',
    sortable=True,
    filter=True
)
```

### 3. 社交媒体链接
```python
github_column = create_link_column(
    field='github',
    header_name='GitHub',
    url='https://github.com/{github}',
    sortable=True,
    filter=True
)
```

### 4. 文档链接
```python
doc_column = create_link_column(
    field='doc_id',
    header_name='文档',
    url='https://docs.example.com/doc/{doc_id}',
    sortable=True,
    filter=True
)
```

## 最佳实践

1. **URL验证**: 确保URL模板格式正确，特别是占位符的使用
2. **性能优化**: 对于大量数据，考虑使用批量创建方法
3. **用户体验**: 保持链接图标与表头文本的视觉一致性
4. **错误处理**: 在URL模板中使用有效的字段名，避免运行时错误

## 更新日志

### v1.1.7
- 修复了InnerHeaderComponent的实现
- 优化了事件处理机制
- 改进了URL模板支持
- 增强了与ag-grid的兼容性 