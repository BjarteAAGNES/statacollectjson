import json
import requests
import re
import uuid
from dash import html
import dash_bootstrap_components as dbc

def fetch_json_from_source(source):
    if source.startswith("http://") or source.startswith("https://"):
        try:
            resp = requests.get(source)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            return {"error": str(e)}
    else:
        try:
            with open(source, "r") as f:
                return json.load(f)
        except Exception as e:
            return {"error": str(e)}

def filter_items(items_dict, include_regex, exclude_regex, omit_base):
    include_re = re.compile(include_regex) if include_regex else None
    exclude_re = re.compile(exclude_regex) if exclude_regex else None
    filtered = {}
    for k, v in items_dict.items():
        if omit_base and v.get("omit-type") == "base":
            continue
        if include_re and not include_re.search(k):
            continue
        if exclude_re and exclude_re.search(k):
            continue
        filtered[k] = v
    return filtered

import uuid
from dash import html
import dash_bootstrap_components as dbc

def json_to_accordion(data, include_regex, exclude_regex, omit_base, parent_key="root", level=0):
    components = []
    if isinstance(data, dict):
        for key, value in data.items():
            if key == "Items" and isinstance(value, dict):
                filtered_items = filter_items(value, include_regex, exclude_regex, omit_base)
                length = len(filtered_items)
                item_id = str(uuid.uuid4())
                children = json_to_accordion(filtered_items, include_regex, exclude_regex, omit_base, parent_key=key, level=level + 1)
                title = html.Span([key + " ", html.B(f"{{{length}}}")])
                components.append(dbc.AccordionItem(title=title, children=children, item_id=item_id))
            else:
                if isinstance(value, dict):
                    length = len(value)
                    children = json_to_accordion(value, include_regex, exclude_regex, omit_base, parent_key=key, level=level + 1)
                    title = html.Span([key + " ", html.B(f"{{{length}}}")])
                    components.append(dbc.AccordionItem(title=title, children=children, item_id=str(uuid.uuid4())))
                elif isinstance(value, list):
                    length = len(value)
                    children = json_to_accordion(value, include_regex, exclude_regex, omit_base, parent_key=key, level=level + 1)
                    title = html.Span([key + " ", html.B(f"[{length}]")])
                    components.append(dbc.AccordionItem(title=title, children=children, item_id=str(uuid.uuid4())))
                else:
                    components.append(
                        html.Div([
                            html.Span(f"{key}: "),
                            html.Span(str(value), style={"color": "#008B8B"})
                        ], style={"marginLeft": f"{level * 20}px"})
                    )
    elif isinstance(data, list):
        for i, item in enumerate(data):
            children = json_to_accordion(item, include_regex, exclude_regex, omit_base, parent_key=f"{parent_key}[{i}]", level=level + 1)
            length = len(item) if isinstance(item, (list, dict)) else 0
            if isinstance(item, dict):
                title = html.Span([f"{parent_key}[{i}] ", html.B(f"{{{length}}}")])
            elif isinstance(item, list):
                title = html.Span([f"{parent_key}[{i}] ", html.B(f"[{length}]")])
            else:
                title = f"{parent_key}[{i}]"
            components.append(dbc.AccordionItem(title=title, children=children, item_id=str(uuid.uuid4())))
    else:
        components.append(
            html.Div(html.Span(str(data), style={"color": "#008B8B"}), style={"marginLeft": f"{level * 20}px"})
        )
    return components
