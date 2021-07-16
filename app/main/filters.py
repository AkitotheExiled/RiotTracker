from . import main
import json
@main.app_template_filter('from_json')
def convert_json_to_list(value):
    return json.loads(value)

