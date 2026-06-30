import re

EMPTY_SPACE = "^\s+$"

# Small object defining a role.
class SystemRole:
    def __init__(self, name, displayName = None):
        name = str(name)

        if len(name) == 0 or re.search(EMPTY_SPACE, name):
            name = "Unknown"
        
        if (
            displayName == None
            or len(displayName) == 0
            or re.search(EMPTY_SPACE, displayName)
        ):
            displayName = name

        self.name = str(name)
    
    def named(self, _name):
        return self.name == _name