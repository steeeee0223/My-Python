import re, json, base64


def getId(url: str) -> str:
    pattern = r"https://www.notion.so/\w+/([\w-]+-)?(\w+)"
    result = re.match(pattern, url)
    return result.group(2) if result else "Invalid Url"


def splitContent(s: str, n: int = 2000) -> list[str]:
    def _f(s, n):
        while s:
            yield s[:n]
            s = s[n:]

    return list(_f(s, n))


def writeImage(img_data, img_name="imageToSave"):
    with open(f"./notion-app/img/{img_name}.png", "wb") as fh:
        fh.write(base64.urlsafe_b64decode(img_data))


def writeJson(path: str, data: dict) -> None:
    with open(path, "w", encoding="utf8") as f:
        json.dump(data, f, ensure_ascii=False)
