import tkinter as tk
from tkinter import ttk, messagebox
import pystray
from PIL import Image, ImageDraw
import threading
import pyautogui
from pynput import keyboard
import pyperclip
import os
from dotenv import load_dotenv
import google.generativeai as genai
import time
import win32clipboard
import win32con

class GWriterApp:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('GOOGLE_API_KEY', '')
        self.setup_ai()
        
        # Main window setup
        self.root = tk.Tk()
        self.root.title("G.Writer - AI Text Rewriter")
        self.root.geometry("400x300")
        self.root.protocol("WM_DELETE_WINDOW", self.hide_window)
        
        self.setup_ui()
        self.setup_hotkey()
        self.create_tray_icon()
        
    def setup_ai(self):
        """Initialize Google Gemini AI"""
        if self.api_key and self.api_key != 'your_api_key_here':
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-1.5-flash')
                self.ai_ready = True
            except Exception as e:
                self.ai_ready = False
                print(f"AI setup failed: {e}")
        else:
            self.ai_ready = False
    
    def setup_ui(self):
        """Setup the GUI"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="G.Writer", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # API Key section
        ttk.Label(main_frame, text="Google Gemini API Key:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.api_key_entry = ttk.Entry(main_frame, width=40, show="*")
        self.api_key_entry.grid(row=2, column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E))
        self.api_key_entry.insert(0, self.api_key)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        self.verify_button = ttk.Button(button_frame, text="Verify API Key", command=self.verify_api_key)
        self.verify_button.pack(side=tk.LEFT, padx=5)
        
        self.save_button = ttk.Button(button_frame, text="Save", command=self.save_api_key)
        self.save_button.pack(side=tk.LEFT, padx=5)
        
        # Status
        self.status_label = ttk.Label(main_frame, text="")
        self.status_label.grid(row=4, column=0, columnspan=2, pady=10)
        
        # Instructions
        instructions = """Instructions:
1. Enter your Google Gemini API key above
2. Click 'Verify API Key' to test connection
3. Click 'Save' to store the key
4. Press Alt+G anywhere to rewrite selected text
5. The app will run in the system tray"""
        
        instruction_label = ttk.Label(main_frame, text=instructions, justify=tk.LEFT)
        instruction_label.grid(row=5, column=0, columnspan=2, pady=10, sticky=tk.W)
        
        # Update status based on AI readiness
        self.update_status()
    
    def update_status(self):
        """Update the status label"""
        if self.ai_ready:
            self.status_label.config(text="✓ AI Ready - Press Alt+G to rewrite text", foreground="green")
        else:
            self.status_label.config(text="⚠ Please configure API key", foreground="red")
    
    def verify_api_key(self):
        """Verify the API key by making a test call"""
        api_key = self.api_key_entry.get()
        if not api_key or api_key == 'your_api_key_here':
            messagebox.showerror("Error", "Please enter a valid API key")
            return
        
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content("Test")
            messagebox.showinfo("Success", "API key is valid!")
            self.api_key = api_key
            self.model = model
            self.ai_ready = True
            self.update_status()
        except Exception as e:
            messagebox.showerror("Error", f"API key verification failed: {str(e)}")
            self.ai_ready = False
            self.update_status()
    
    def save_api_key(self):
        """Save the API key to .env file"""
        api_key = self.api_key_entry.get()
        if not api_key:
            messagebox.showerror("Error", "Please enter an API key")
            return
        
        try:
            with open('.env', 'w') as f:
                f.write(f'GOOGLE_API_KEY={api_key}')
            messagebox.showinfo("Success", "API key saved!")
            self.api_key = api_key
            self.setup_ai()
            self.update_status()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save API key: {str(e)}")
    
    def setup_hotkey(self):
        """Setup global hotkey Alt+G using pynput (more reliable)"""
        def on_hotkey():
            if self.ai_ready:
                print("Alt+G detected!")
                threading.Thread(target=self.rewrite_selected_text, daemon=True).start()
            else:
                print("API key not configured")
        
        try:
            # Use pynput for global hotkeys (more reliable than keyboard library)
            hotkeys = keyboard.GlobalHotKeys({
                '<alt>+g': on_hotkey
            })
            hotkeys.start()
            print("Alt+G global hotkey registered with pynput")
        except Exception as e:
            print(f"Failed to register global hotkey: {e}")
    
    def get_clipboard_text(self):
        """Get text from clipboard using Windows API"""
        try:
            win32clipboard.OpenClipboard()
            data = win32clipboard.GetClipboardData(win32con.CF_TEXT)
            win32clipboard.CloseClipboard()
            return data.decode('utf-8') if data else ""
        except:
            try:
                win32clipboard.CloseClipboard()
            except:
                pass
            return ""
    
    def set_clipboard_text(self, text):
        """Set clipboard text using Windows API"""
        try:
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32con.CF_TEXT, text.encode('utf-8'))
            win32clipboard.CloseClipboard()
            return True
        except:
            try:
                win32clipboard.CloseClipboard()
            except:
                pass
            return False

    def rewrite_selected_text(self):
        """Debug version to see exactly what's happening with clipboard"""
        try:
            print("\n=== DEBUG: Starting text rewrite ===")
            
            # Test clipboard functionality first
            print("Testing clipboard...")
            test_text = "test123"
            pyperclip.copy(test_text)
            clipboard_test = pyperclip.paste()
            print(f"Clipboard test: wrote '{test_text}', read '{clipboard_test}' - {'✅ PASS' if clipboard_test == test_text else '❌ FAIL'}")
            
            # Store and show original clipboard
            original_clipboard = pyperclip.paste()
            print(f"Original clipboard: '{original_clipboard}'")
            
            # Clear clipboard and verify
            print("\nClearing clipboard...")
            pyperclip.copy("")
            time.sleep(0.1)
            cleared = pyperclip.paste()
            print(f"Clipboard after clear: '{cleared}' (length: {len(cleared)})")
            
            # Try multiple copy approaches with detailed logging
            selected_text = ""
            
            # Method 1: Direct Ctrl+C
            print("\n--- Method 1: Direct Ctrl+C ---")
            print("Sending Ctrl+C...")
            pyautogui.keyDown('ctrl')
            pyautogui.press('c')
            pyautogui.keyUp('ctrl')
            time.sleep(0.8)  # Even longer delay
            
            selected_text = pyperclip.paste()
            print(f"After Ctrl+C: '{selected_text}' (length: {len(selected_text)})")
            
            if not selected_text and selected_text != original_clipboard:
                # Method 2: Try PyAutoGUI hotkey
                print("\n--- Method 2: PyAutoGUI hotkey ---")
                pyperclip.copy("")
                time.sleep(0.2)
                pyautogui.hotkey('ctrl', 'c')
                time.sleep(0.8)
                
                selected_text = pyperclip.paste()
                print(f"After hotkey: '{selected_text}' (length: {len(selected_text)})")
            
            if not selected_text:
                # Method 3: Select all and copy (for testing)
                print("\n--- Method 3: Select All (Ctrl+A) then Copy ---")
                pyperclip.copy("")
                time.sleep(0.2)
                
                print("Sending Ctrl+A...")
                pyautogui.hotkey('ctrl', 'a')
                time.sleep(0.5)
                
                print("Sending Ctrl+C...")
                pyautogui.hotkey('ctrl', 'c')
                time.sleep(0.8)
                
                selected_text = pyperclip.paste()
                print(f"After select all + copy: '{selected_text[:200]}...' (length: {len(selected_text)})")
            
            print(f"\n=== FINAL RESULT ===")
            print(f"Selected text: '{selected_text[:200]}...' (length: {len(selected_text)})")
            
            if not selected_text or len(selected_text) == 0:
                print("❌ FAILED: No text was copied!")
                print("💡 TIP: Try manually selecting some text first, then press Alt+G")
                return
            
            # If we got text, continue with AI processing
            if len(selected_text) > 500:
                selected_text = selected_text[:500]
                print("Text truncated to 500 characters for AI processing")
            
            print(f"\n🤖 Sending to AI: '{selected_text[:100]}...'")
            
            # Simple AI prompt
            prompt = f'Fix grammar: {selected_text}'
            
            response = self.model.generate_content(prompt)
            rewritten_text = response.text.strip()
            
            # Clean quotes
            if rewritten_text.startswith('"') and rewritten_text.endswith('"'):
                rewritten_text = rewritten_text[1:-1]
            
            print(f"✅ AI result: '{rewritten_text[:100]}...'")
            
            # Replace text
            pyperclip.copy(rewritten_text)
            time.sleep(0.3)
            pyautogui.hotkey('ctrl', 'v')
            
            print("🎉 Complete!")
            
        except Exception as e:
            print(f"❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
    
    def create_tray_icon(self):
        """Create system tray icon"""
        # Create a simple icon
        image = Image.new('RGB', (64, 64), color=(73, 109, 137))
        draw = ImageDraw.Draw(image)
        draw.text((20, 20), "G", fill=(255, 255, 255))
        
        # Create tray menu
        menu = pystray.Menu(
            pystray.MenuItem("Show", self.show_window),
            pystray.MenuItem("Exit", self.quit_app)
        )
        
        self.tray_icon = pystray.Icon("G.Writer", image, "G.Writer - AI Text Rewriter", menu)
    
    def show_window(self, icon=None, item=None):
        """Show the main window"""
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()
    
    def hide_window(self):
        """Hide the main window to system tray"""
        self.root.withdraw()
    
    def quit_app(self, icon=None, item=None):
        """Quit the application"""
        self.tray_icon.stop()
        self.root.quit()
    
    def run(self):
        """Run the application"""
        # Start tray icon in separate thread
        tray_thread = threading.Thread(target=self.tray_icon.run, daemon=True)
        tray_thread.start()
        
        # Start main window
        self.root.mainloop()

if __name__ == "__main__":
    app = GWriterApp()
    app.run()