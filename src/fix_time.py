import re

with open('IMU_Processing.hpp', 'r') as f:
    content = f.read()

# Fix toSec() - need to capture the variable name before ->header
def fix_tosec(match):
    var = match.group(1)
    return f'{var}->header.stamp.sec + {var}->header.stamp.nanosec * 1e-9'

# Pattern: xxx->header.stamp.toSec()
# But we need the variable name that comes before ->header
content = re.sub(
    r'(\w+)->header\.stamp\.sec \+ ->header\.stamp\.nanosec \* 1e-9',
    lambda m: f'{m.group(1)}->header.stamp.sec + {m.group(1)}->header.stamp.nanosec * 1e-9',
    content
)

with open('IMU_Processing.hpp', 'w') as f:
    f.write(content)

print("Fixed time conversions")
