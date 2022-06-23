import re
from mistune.block_parser import BlockParser

CALLOUT_PATTERN = re.compile(
    r":::(success|info|warning|danger|spoiler)\n(.*)\n:::"
)

def parse_callout(block: BlockParser, m: re.Match, state: dict):
    callout = [
        {   
            "type": "callout_header", "text": m.group(1)
        },
        {
            "type": "paragraph", "text": m.group(2)
        }
    ]
    return {"type": "block_callout", "children": callout}


# def render_html_def_list(text):
#     return "<dl>\n" + text + "</dl>\n"


# def render_html_def_list_header(text):
#     return "<dt>" + text + "</dt>\n"


# def render_html_def_list_item(text):
#     return "<dd>" + text + "</dd>\n"


def render_ast_callout_header(text):
    return {"type": "callout_header", "text": text[0]["text"]}


def render_ast_callout_item(text):
    return {"type": "callout_item", "text": text[0]["text"]}


def plugin_callout(md):
    md.block.register_rule("callout", CALLOUT_PATTERN, parse_callout)
    md.block.rules.append("callout")
    # if md.renderer.NAME == "html":
    #     md.renderer.register("def_list", render_html_def_list)
    #     md.renderer.register("def_list_header", render_html_def_list_header)
    #     md.renderer.register("def_list_item", render_html_def_list_item)

    if md.renderer.NAME == "ast":
        md.renderer.register("callout_header", render_ast_callout_header)
        md.renderer.register("callout_item", render_ast_callout_item)