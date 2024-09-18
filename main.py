from translate import Translator, exceptions
from transliterate import translit
import keyboard
import pyautogui
import pyperclip
import time
import tkinter as tk
import threading

# Global variable to store the selected language
selected_language = "sr"

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
        
        if to_lang == "sr":
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
    time.sleep(0.01)
    pyautogui.hotkey('ctrl', 'x')
    time.sleep(0.01)
    
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
    time.sleep(0.01)  # Short delay
    pyautogui.hotkey('ctrl', 'c')  # Copy selected text
    time.sleep(0.001)  # Short delay

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
    time.sleep(0.001)  # Short delay

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
    print("Select the target language:")
    print("1. French")
    print("2. Serbian")
    print("3. Polish")
    choice = input("Enter the number of your choice: ")
    
    if choice == "1":
        selected_language = "fr"
    elif choice == "2":
        selected_language = "sr"
    elif choice == "3":
        selected_language = "pl"
    else:
        print("Invalid choice, defaulting to Serbian.")
        selected_language = "sr"

def main():
    select_language()  # Add language selection
    update_gui("Press 'down arrow' to translate text to selected language. Press 'up arrow' to translate text to English. Press 'esc' to exit.", clear=True)
    print("Press 'down arrow' to translate text to selected language. Press 'up arrow' to translate text to English. Press 'esc' to exit.")
    
    def keyboard_listener():
        # Set up the keyboard hook for the down arrow key
        keyboard.add_hotkey('down', on_down_arrow)  # Bind key to function
        keyboard.add_hotkey('up', on_up_arrow)  # Bind key to function
        keyboard.wait('esc')  # Wait for exit key
    
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
