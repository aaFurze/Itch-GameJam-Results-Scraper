from .scraper import check_webpage_exists

def validate_url_input(url: str) -> bool:
    page_found = check_webpage_exists(url)
    if not page_found: 
        print("Could not find the GameJam results page provided.")
        print("Exiting program...")
        return False
    return True

def validate_results_number_input(number: str) -> int:
    max_pages = number
    if max_pages == "":
        return 100
    try:
        max_pages = int(max_pages)
    except ValueError:
        print("Invalid input (must be a positive number)")
        print("Setting value to 20")
        return None
    if int(max_pages) <= 20:
        print("Low number detected. Setting to 20.")
        return 1
    else:
        return int(int(max_pages) / 20)


def validate_file_name_input(name: str):
    output = ""
    for char in name:
        if not char.isalnum() and char not in ["_", "-"]:
            continue
        if char == " ":
            output += "-"
            continue
        output += char
    return output
