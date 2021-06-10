from typing import Any, Dict, List, Tuple
import os

from jsonschema import validate
import json

from rich.console import Console

# A sample schema, like what we'd get from json.load()
script_jsonschema = {
    "type": "object",
    "properties": {
        "script_name": {"type": "string"},
        "content": {
            "type": ["array", "null"],
            "items": {
                "type": "object",
                "properties": {
                    "command_type": {
                        "enum": [
                            "press_key",
                            "release_key",
                            "press_key_then_release",
                            "send_text",
                            "open_program",
                        ]
                    },
                    "command_argument": {"type": "string"},
                },
                "required": ["command_type", "command_argument"],
            },
        },
    },
    "required": ["script_name", "content"],
}


USERS_SCRIPT: Dict[str, Any] = dict()


def get_script_files_from_dir(path_to_json_dir: str) -> List[Any]:
    all_scripts = []
    for file_name in [
        file for file in os.listdir(path_to_json_dir) if file.endswith(".json")
    ]:
        with open(
            os.path.join(path_to_json_dir, file_name), encoding="utf-8"
        ) as json_file:
            print(f"READING: {file_name}\n")
            _script_data = json.load(json_file)
            all_scripts.append(_script_data)

    return all_scripts


def validate_scripts(all_script_data: List[Any]) -> Tuple[bool, List[Any]]:
    every_script_is_valid = True
    valid_only = []
    for json_script in all_script_data:
        try:
            validate(instance=json_script, schema=script_jsonschema)
            valid_only.append(json_script)
        except Exception as e:
            # TODO: log or print to debug
            every_script_is_valid = False

    return every_script_is_valid, valid_only


if __name__ == "__main__":

    def try_exec_scripts_test():
        cwd = os.path.dirname(os.path.realpath(__file__))
        dirname = "tmp_db"
        all_scripts = get_script_files_from_dir(os.path.join(cwd, dirname))
        _, good_scripts = validate_scripts(all_scripts)
        for scr in good_scripts:
            name = scr["script_name"]
            content = scr["content"]
            print("Running:", name)
            for command in content:
                print("\t\t\t => Command type is:", command["command_type"])
                print("\t\t\t\t => Command arg is:", command["command_argument"])

    def json_whole_directory_validation_test():
        cwd = os.path.dirname(os.path.realpath(__file__))
        dirname = "tmp_db"
        all_scripts = get_script_files_from_dir(os.path.join(cwd, dirname))
        print("Total count of JSON files in", dirname, "=", len(all_scripts))
        status, good_scripts = validate_scripts(all_scripts)
        print("All JSON files is valid:", status)
        print("Total count of VALID files =", len(good_scripts))

    def json_file_validation_test():
        cwd = os.path.dirname(os.path.realpath(__file__))
        dirname = "tmp_db"
        filename = "chrome_incognito.json"
        full_path = os.path.join(cwd, dirname, filename)
        with open(full_path, encoding="utf-8") as json_file:
            data = json.load(json_file)
            validate(instance=data, schema=script_jsonschema)
            print(filename, "is: VALID")
            # print beautifully
            rich_console = Console(width=80)
            rich_console.print(data, justify="left", highlight=True)

    # json_file_validation_test()
    json_whole_directory_validation_test()
    try_exec_scripts_test()
