# Streamlit Aggrid SDK with Custom Link Header Component

[English](#overview) | [中文](./README_ZH.md)

---

## Overview

This SDK extends the `st-aggrid` library with a custom link header component that allows you to add clickable link icons to column headers. The component preserves all default `ag-grid` functionality including sorting, filtering, and resizing.

## Features

- 🔗 **Custom Link Headers**: Add clickable link icons to column headers
- 📊 **Full Grid Functionality**: Maintains sorting, filtering, and resizing capabilities
- 🎯 **Event Isolation**: Clicking the link icon doesn't interfere with sorting/filtering
- 🛠️ **Easy Integration**: Simple API for creating link-enabled columns
- 📦 **Cross-Platform**: Supports both Windows and HuggingFace environments

## Building the SDK

### Prerequisites

- Python 3.8+
- Node.js 16+
- Yarn or npm

### Build Process

1. **Install Dependencies**
   ```bash
   # Install Python dependencies
   pip install -r requirements.txt
   
   # Install Node.js dependencies
   cd st_aggrid/frontend
   npm install
   ```

2. **Build Frontend**
   ```bash
   cd st_aggrid/frontend
   npm run build
   ```

3. **Build SDK Package**
   ```bash
   # Run the build script
   python build_sdk.py
   ```

The build script will:
- Build the frontend assets
- Create wheel packages for both Windows and HuggingFace environments
- Generate SDK output in `sdk_output/` directory

### Build Output

After successful build, you'll find:
- `sdk_output/windows/` - Windows environment SDK
- `sdk_output/huggingface/` - HuggingFace environment SDK

Each directory contains:
- `streamlit_aggrid-1.1.7-py3-none-any.whl` - Wheel package
- `install.bat` (Windows) or `install.sh` (HuggingFace) - Installation script
- `README.md` - Installation instructions

## Installation

```bash
# Install from local wheel file
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple dist/streamlit_aggrid-1.1.7-py3-none-any.whl
```

## Quick Start

```python
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.link_header_builder import create_link_column

# Sample data
data = {
    'name': ['Alice', 'Bob', 'Charlie'],
    'email': ['alice@example.com', 'bob@example.com', 'charlie@example.com'],
    'github': ['alice-github', 'bob-github', 'charlie-github'],
    'age': [25, 30, 35]
}
df = pd.DataFrame(data)

# Create link columns
email_column = create_link_column(
    field='email',
    header_name='Email',
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

# Build grid options
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_column('name', sortable=True, filter=True)
gb.configure_column('age', sortable=True, filter=True)

# Add link columns to grid options
grid_options = gb.build()
grid_options['columnDefs'].append(email_column)
grid_options['columnDefs'].append(github_column)

# Display the grid
grid_response = AgGrid(
    df,
    gridOptions=grid_options,
    data_return_mode='AS_INPUT',
    update_mode='MODEL_CHANGED',
    fit_columns_on_grid_load=True,
    theme='streamlit'
)
```

## API Reference

### `create_link_column(field, header_name, url, **kwargs)`

Creates a column definition with a custom link header.

**Parameters:**
- `field` (str): Data field name
- `header_name` (str): Column header name
- `url` (str): URL template for the link (supports {field} placeholder)
- `**kwargs`: Additional column configuration options

**Returns:**
- `dict`: Column definition dictionary

### `create_link_columns(link_config, **default_kwargs)`

Creates multiple link columns from a configuration dictionary.

**Parameters:**
- `link_config` (dict): Dictionary mapping field names to URLs
- `**default_kwargs`: Default configuration for all columns

**Returns:**
- `dict`: Dictionary of column definitions

### `add_link_headers_to_grid_options(grid_options, link_config, **default_kwargs)`

Adds link column configurations to existing grid options.

**Parameters:**
- `grid_options` (dict): Existing grid options
- `link_config` (dict): Dictionary mapping field names to URLs
- `**default_kwargs`: Default configuration for all columns

**Returns:**
- `dict`: Updated grid options

## Advanced Usage

### Batch Column Creation

```python
# Define link configurations
link_config = {
    'email': 'mailto:{email}',
    'website': 'https://{website}',
    'github': 'https://github.com/{github}'
}

# Create all link columns at once
link_columns = create_link_columns(link_config, sortable=True, filter=True)

# Add to grid options
for column_def in link_columns.values():
    grid_options['columnDefs'].append(column_def)
```

### Dynamic URL Generation

```python
# URL with dynamic field substitution
email_column = create_link_column(
    field='email',
    header_name='Contact',
    url='mailto:{email}?subject=Hello from {name}',
    sortable=True,
    filter=True
)
```

## Configuration Options

All standard `ag-grid` column options are supported:

- `sortable`: Enable/disable sorting
- `filter`: Enable/disable filtering
- `resizable`: Enable/disable column resizing
- `suppressHeaderContextMenu`: Show/hide header context menu
- `width`: Set column width
- `minWidth`: Set minimum column width
- `maxWidth`: Set maximum column width

## Examples

See `test_streamlit_app.py` for a complete working example.

## Troubleshooting

**Issue**: Link icons not showing
- Check if `create_link_column` function is imported correctly
- Verify column definitions are properly added to `grid_options['columnDefs']`

**Issue**: Sorting/filtering functionality lost
- Ensure `sortable=True` and `filter=True` are set in `create_link_column`
- Check if `headerComponentParams` structure is used correctly

**Issue**: Clicking links not responding
- Verify URL format is correct
- Check browser console for JavaScript errors

## Notes

1. **URL Templates**: URLs support `{field}` placeholders that get replaced with actual data
2. **Event Handling**: Clicking the 🔗 icon prevents event bubbling and won't trigger sorting
3. **Styling**: Link icons use default colors and maintain consistency with header text
4. **Compatibility**: Fully compatible with all `ag-grid` functionality
