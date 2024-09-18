from translate import Translator, exceptions
from transliterate import translit
import keyboard
import pyautogui
import pyperclip
import time
import tkinter as tk
import threading
import difflib

languages = {
    "english": "en",
    "serbian": "sr",
    "french": "fr",
    "polish": "pl",
    "spanish": "es",
    "german": "de",
    "italian": "it",
    "portuguese": "pt",
    "russian": "ru",
    "chinese": "zh",
    "japanese": "ja",
    "korean": "ko",
    "arabic": "ar",
    "dutch": "nl",
    "greek": "el",
    "hebrew": "he",
    "hindi": "hi",
    "hungarian": "hu",
    "swedish": "sv",
    "turkish": "tr",
    "vietnamese": "vi",
    "thai": "th",
    "czech": "cs",
    "danish": "da",
    "finnish": "fi",
    "norwegian": "no",
    "romanian": "ro",
    "slovak": "sk",
    "ukrainian": "uk",
    "bulgarian": "bg",
    "croatian": "hr",
    "indonesian": "id",
    "malay": "ms",
    "filipino": "tl",
    "persian": "fa",
    "swahili": "sw",
    "tamil": "ta",
    "telugu": "te",
    "urdu": "ur",
    "bengali": "bn",
    "punjabi": "pa",
    "marathi": "mr",
    "gujarati": "gu",
    "kannada": "kn",
    "malayalam": "ml",
    "sinhala": "si",
    "slovenian": "sl",
    "estonian": "et",
    "latvian": "lv",
    "lithuanian": "lt",
    "icelandic": "is",
    "irish": "ga",
    "welsh": "cy",
    "scots_gaelic": "gd",
    "luxembourgish": "lb",
    "maltese": "mt",
    "macedonian": "mk",
    "albanian": "sq",
    "armenian": "hy",
    "azerbaijani": "az",
    "basque": "eu",
    "belarusian": "be",
    "bosnian": "bs",
    "georgian": "ka",
    "kazakh": "kk",
    "kyrgyz": "ky",
    "mongolian": "mn",
    "tajik": "tg",
    "turkmen": "tk",
    "uzbek": "uz",
    "yiddish": "yi",
    "zulu": "zu"
    # Add more languages as needed
}

# Global variables to store settings
selected_language = "sr"
translate_cyrillic = True
time_to_sleep = 0.01
kybind1 = "down"
kybind2 = "up"
kybind3 = "esc"

# Function to update the GUI with messages
def update_gui(message, clear=False):
    if clear:
        text_widget.delete(1.0, tk.END)
    text_widget.insert(tk.END, message + "\n")
    root.update()

# Check if the text is valid
def check_is_valid_text(text):
    update_gui("Checking validity", clear=False)
    print("Checking validity")

    if len(text) > 350:
        update_gui("ERROR: Text is too long", clear=False)
        print("ERROR: Text is too long")
        return False
    elif len(text) < 1:
        update_gui("ERROR: Text is too short", clear=False)
        print("ERROR: Text is too short")
        return False
    else:
        update_gui("Text is valid, translating...", clear=False)
        print("Text is valid, translating...")
        return True

# Translate the text
def translate_text(user_input, to_lang):
    t = Translator(from_lang="en", to_lang=to_lang)  # Initialize translator
    
    try:
        update_gui("Starting translation...", clear=False)
        print("Starting translation...")
        translation = t.translate(user_input)  # Perform translation
        
        update_gui(f"Translation: {translation}", clear=False)
        print(f"Translation: {translation}")
        
        if to_lang == "sr" and translate_cyrillic:
            try:
                latin_translation = translit(translation, 'sr', reversed=True)  # Convert to Latin
                update_gui(f"Latin Transliteration: {latin_translation}", clear=False)
                print(f"Latin Transliteration: {latin_translation}")
            except Exception as e:
                update_gui(f"Transliteration failed: {e}", clear=False)
                print(f"Transliteration failed: {e}")
                latin_translation = translation  # Fallback to the original translation if transliteration fails
            
            update_gui(f"Final Translation: {latin_translation}", clear=False)  # Output translation
            print(f"Final Translation: {latin_translation}")
            return latin_translation
        else:
            return translation
    
    except exceptions.TranslationError as e:
        update_gui(f"Translation failed: {e}", clear=False)  # Handle translation errors
        print(f"Translation failed: {e}")
    except Exception as e:
        update_gui(f"An unexpected error occurred: {e}", clear=False)  # Handle other errors
        print(f"An unexpected error occurred: {e}")
    return None

# Replace original text with translated text
def replace_text(text):
    if text is None:
        update_gui("No text to replace", clear=False)
        print("No text to replace")
        return
    
    # Simulate a select all and cut
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(time_to_sleep)
    pyautogui.hotkey('ctrl', 'x')
    time.sleep(time_to_sleep)
    
    # Paste the translated text
    pyperclip.copy(text)  # Copy the translated text
    pyautogui.hotkey('ctrl', 'v')  # Paste the text

# Function triggered by down arrow key
def on_down_arrow():
    update_gui("", clear=True)  # Clear the GUI for new translation
    update_gui("Starting new translation process...", clear=False)
    print("Starting new translation process...")
    
    # Simulate a copy action
    pyautogui.hotkey('ctrl', 'a')  # Select all text
    time.sleep(time_to_sleep)  # Short delay
    pyautogui.hotkey('ctrl', 'c')  # Copy selected text
    time.sleep(time_to_sleep)  # Short delay

    # Store the copied text
    harvested_text = pyperclip.paste()  # Get text from clipboard
    update_gui(f"Harvested text: {harvested_text}", clear=False)  # Output harvested text
    print(f"Harvested text: {harvested_text}")

    # Check if the text is valid
    if check_is_valid_text(harvested_text):
        # Translate the text if valid
        translated_text = translate_text(harvested_text, selected_language)
        replace_text(translated_text)
        update_gui(f"Replaced text: {translated_text}", clear=False)
        print(f"Replaced text: {translated_text}")

# Function triggered by up arrow key
def on_up_arrow():
    update_gui("", clear=True)  # Clear the GUI for new translation
    update_gui("Starting new translation process...", clear=False)
    print("Starting new translation process...")
    
    # Simulate a copy action
    pyautogui.hotkey('ctrl', 'c')  # Copy selected text
    time.sleep(time_to_sleep)  # Short delay

    # Store the copied text
    harvested_text = pyperclip.paste()  # Get text from clipboard
    update_gui(f"Harvested text: {harvested_text}", clear=False)  # Output harvested text
    print(f"Harvested text: {harvested_text}")

    # Check if the text is valid
    if check_is_valid_text(harvested_text):
        # Translate the text if valid
        translated_text = translate_text(harvested_text, "en")
        update_gui(f"Translated to English: {translated_text}", clear=False)
        print(f"Translated to English: {translated_text}")

def select_language():
    global selected_language
    while True:
        usr_input = input("Select the target language: ").lower()
        close_matches = difflib.get_close_matches(usr_input, languages.keys())
        
        if close_matches:
            confirm = input(f"Is '{close_matches[0]}' the correct language? (y/n): ").lower()
            if confirm == "y":
                selected_language = languages[close_matches[0]]
                print(f"Language selected: {selected_language}")
                break
        print("Invalid choice, try again.")

def main_menu():
    while True:
        print("1. start")
        print("2. settings")
        print("3. Exit")
        print("Enter the number of your choice: ")
        choice = input("> ")
        if choice == "1":
            break
        elif choice == "2":
            settings_menu()
        elif choice == "3":
            exit()

def settings_menu():
    global translate_cyrillic, time_to_sleep, kybind1, kybind2, kybind3

    while True:
        print("1. Translate cyrillic to latin (for serbian language) : ", translate_cyrillic)
        print("2. Time to sleep :", time_to_sleep)
        print("3. Keybinds")
        print("       Translate english to selected language : ", kybind1)
        print("       Translate selected language to english : ", kybind2)
        print("       Exit : ", kybind3)
        print("4. Back")
        choice = input("> ")

        if choice == "1":
            translate_cyrillic = not translate_cyrillic
        elif choice == "2":
            time_to_sleep = float(input("Enter the time to sleep: "))
        elif choice == "3":
            kybind1 = input("Enter the new keybind for translate english to selected language: ")
            kybind2 = input("Enter the new keybind for translate selected language to english: ")
            kybind3 = input("Enter the new keybind for exit: ")
        elif choice == "4":
            break
        else:
            close_matches = difflib.get_close_matches(choice, ["1", "2", "3", "4"])
            if close_matches:
                print(f"Did you mean: {close_matches[0]}? (y/n)")
                confirm = input("> ")
                if confirm.lower() == "y":
                    choice = close_matches[0]
                    continue
            print("Invalid choice, try again")

def main():
    main_menu()
    select_language()  # Add language selection
    update_gui("Press 'down arrow' to translate text to selected language. Press 'up arrow' to translate text to English. Press 'esc' to exit.", clear=True)
    print("Press 'down arrow' to translate text to selected language. Press 'up arrow' to translate text to English. Press 'esc' to exit.")
    
    def keyboard_listener():
        # Set up the keyboard hook for the down arrow key
        keyboard.add_hotkey(kybind1, on_down_arrow)  # Bind key to function
        keyboard.add_hotkey(kybind2, on_up_arrow)  # Bind key to function
        keyboard.wait(kybind3)  # Wait for exit key
    
    # Run the keyboard listener in a separate thread to avoid GUI freezing
    listener_thread = threading.Thread(target=keyboard_listener)
    listener_thread.start()

if __name__ == "__main__":
    # Set up the tkinter GUI
    root = tk.Tk()
    root.title("Translation Status")
    root.geometry("400x200")
    root.attributes("-topmost", True)  # Keep the window on top
    root.configure(bg="black")  # Set the background color of the window to black

    text_widget = tk.Text(root, font=("Helvetica", 12), wrap=tk.WORD, bg="black", fg="white", bd=0, highlightthickness=0)
    text_widget.pack(pady=5, padx=5, fill=tk.BOTH, expand=True)  # Adjust padding to reduce border size

    # Start the main function
    main()
    root.mainloop()
