def attributes(attr={}):
    return "".join([f' {key}="{attr[key]}"' for key in attr.keys()])


def _children(ch=None):
    if ch is None:
        return ""
    if type(ch) is list:
        return "".join([str(c) for c in ch 
                        if c is not None])
    if type(ch) is str:
        return ch


def _classname(cn=None):
    if cn is None:
        return ""
    return f' class="{cn}"'

def is_empty_by_design(tag_name):
    return (
        tag_name in ["hr", "link", "img", "input", "meta"]
    )

def open_tag(name, classname, attr):
    return f"<{name}{_classname(classname)}{attributes(attr)}>"

def close_tag(name):
    return f"</{name}>"

def tag(name, classname=None, attr={}, children=None):
    parts = [open_tag(name, classname, attr)]
    if not is_empty_by_design(name):
        parts.append(_children(children))
        parts.append(close_tag(name))
    return "".join(parts)

__all__ = ["tag"]
