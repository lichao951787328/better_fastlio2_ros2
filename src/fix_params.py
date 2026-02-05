import re

with open('laserMapping.cpp', 'r') as f:
    content = f.read()

# Pattern: nh->declare_parameter<type>("path/name", var, default);
# Should become: nh->declare_parameter<type>("path.name", default); var = nh->get_parameter("path.name").as_<type>();

def fix_param(match):
    type_str = match.group(1)
    path = match.group(2).replace('/', '.')
    var = match.group(3)
    default = match.group(4)
    
    # Map C++ types to ROS2 getter methods
    type_map = {
        'string': 'string',
        'std::string': 'string',
        'bool': 'bool',
        'int': 'int',
        'double': 'double',
        'float': 'double',  # ROS2 uses double for float params
        'vector<double>': 'double_array'
    }
    
    getter = type_map.get(type_str, 'string')
    
    return f'{var} = nh->declare_parameter<{type_str}>("{path}", {default});'

# Fix pattern: nh->declare_parameter<type>("path", var, default);
content = re.sub(
    r'nh->declare_parameter<([^>]+)>\("([^"]+)",\s*([^,]+),\s*([^)]+)\);',
    fix_param,
    content
)

with open('laserMapping.cpp', 'w') as f:
    f.write(content)

print("Fixed parameters")
