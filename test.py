import re

with open(".tmp/dynamic/index/index.html") as f:
    index_code = f.read()


def find_code(tags, text) -> str:
    return re.findall(
        f"{tags['start']}.*?{tags['end']}",
        text,
        re.DOTALL
    )[0][len(tags['start']):-len(tags['end'])]


style_tags = {
    "start": r"{% style %}",
    "end": r"{% style-end %}"
}

content_tags = {
    "start": r"{% content %}",
    "end": r"{% content-end %}"
}

style_code = find_code(style_tags, index_code)
content_code = find_code(content_tags, index_code)

print(content_code)
