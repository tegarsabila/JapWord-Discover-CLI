import json
from prompt_toolkit import prompt
from yaspin import yaspin

from urllib import request, parse

banner = "\n   ___             _    _       ______\n  |_  |           | |  | |      |  _  \ \n    | | __ _ _ __ | |  | |______| | | |\n    | |/ _` | '_ \| |/\| |______| | | |\n/\__/ / (_| | |_) \  /\  /      | |/ /\n\____/ \__,_| .__/ \/  \/       |___/\n            | |\n            |_| JapWord-Discover v1.0.0\n"

def get_japanese_word_data(word):
    url = f"https://jisho.org/api/v1/search/words?keyword={parse.quote(word)}"
    response = request.urlopen(url)
    data = json.loads(response.read().decode())
    return data

def search_japanese_word(word, display_proc, spinner):
    data = get_japanese_word_data(word)

    if not data['data']:
        print(f"The word '{word}' was not found.")
    else:
        first_result = data['data'][0]
        japanese_word = first_result['japanese'][0].get('word') or first_result['japanese'][0]['reading']
        english_meaning = ', '.join(first_result['senses'][0]['english_definitions'])

        spinner.ok("✅")
        display_proc(japanese_word, english_meaning)

def main():
    print(banner)
    def display_result(japanese_word, english_meaning):
        print(f"\nWord: {japanese_word}")
        print(f"Meaning: {english_meaning}")

    while True:
        kata = prompt("Enter word: ")

        with yaspin(text="Searching...", color="yellow") as spinner:
            search_japanese_word(kata, display_result, spinner)

        again = prompt("Do you wish to re-search the word? (Yes/Exit): ")
        if again.lower() == 'exit':
            break

if __name__ == "__main__":
    main()
