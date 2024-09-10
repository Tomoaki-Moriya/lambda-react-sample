import json
import mimetypes
import os
from pathlib import Path
from typing import Callable

front_dist = Path("dist")


def root(event: dict) -> dict:
    try:
        index_html_filepath = front_dist.joinpath("index.html")
        with open(index_html_filepath, "r") as file:
            index_content = file.read()
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "text/html"},
            "body": index_content,
        }
    except FileNotFoundError:
        return {"statusCode": 400}


def get_item_route(event: dict) -> dict:
    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "items": [
                    {"id": 1, "name": "item1"},
                    {"id": 2, "name": "item2"},
                ],
            }
        ),
    }


def dynamic_route(event: dict) -> dict:
    path = event.get("path", "")
    filepath = front_dist.joinpath(path.lstrip(os.path.sep))
    try:
        with open(filepath, "r") as file:
            file_content = file.read()

        content_type, _ = mimetypes.guess_type(filepath)
        if not content_type:
            return {"statusCode": 400}

        return {
            "statusCode": 200,
            "headers": {"Content-Type": content_type},
            "body": file_content,
        }
    except FileNotFoundError:
        return {"statusCode": 404}


routes: dict[str, Callable[[dict], dict]] = {
    "/": root,
    "/api/items": get_item_route,
    "/{proxy+}": dynamic_route,
}


def lambda_handler(event, context):
    path = event.get("resource", "")
    route = routes.get(path, dynamic_route)

    if not route:
        return {"statusCode": 404}

    return route(event)
