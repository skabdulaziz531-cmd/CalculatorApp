# main.py - উন্নত ডিজাইন, বৈজ্ঞানিক ও ইউনিট কনভার্টার ফিচার সহ হাইব্রিড অ্যাপ (ত্রুটিমুক্ত)

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
import math 

# --- কালার প্যালেট ---
BG_COLOR = (0.05, 0.05, 0.05, 1)    # অ্যাপের ব্যাকগ্রাউন্ড (কালো)
ACCENT_COLOR = (0.0, 0.6, 0.8, 1)   # হাইলাইট/ডিসপ্লে টেক্সট (নীল)
OPERATOR_COLOR = (0.9, 0.5, 0.2, 1) # অপারেটর বাটন (কমলা)
CLEAR_COLOR = (0.7, 0.2, 0.2, 1)    # ক্লিয়ার বাটন (লাল)
BUTTON_COLOR = (0.2, 0.2, 0.2, 1)   # সাধারণ বাটন (গাঢ় ধূসর)

# --- সাহায্যকারী ফাংশন ---
def calculate(expression):
    try:
        expression = expression.replace('π', str(math.pi)).replace('e', str(math.e))
        expression = expression.replace('^', '**') 
        expression = expression.rstrip('+-*/.')
        if not expression:
            return "0"
        
        # eval() ব্যবহার করে গণনার কাজ
        result = str(eval(expression))
        return result
    except Exception:
        return "Error"

# --- ১. বৈজ্ঞানিক ও বেসিক ক্যালকুলেটর স্ক্রিন ---
class CalcScreen(Screen):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=5, spacing=5)
        self.add_widget(self.layout)
        
        # ডিসপ্লে তৈরি
        self.display = Label(
            text="0", 
            font_size=60, 
            size_hint_y=0.25, 
            halign='right', 
            valign='bottom', 
            padding=(20, 20),
            color=ACCENT_COLOR
        )
        self.layout.add_widget(self.display)
        
        # মোড পরিবর্তনের জন্য বক্স লেআউট
        mode_layout = BoxLayout(orientation='horizontal', size_hint_y=0.08)
        self.basic_btn = Button(text="BASIC", font_size=16, background_color=ACCENT_COLOR, on_press=self.toggle_mode)
        self.sci_btn = Button(text="SCI/ADV", font_size=16, background_color=BUTTON_COLOR, on_press=self.toggle_mode)
        self.conv_btn = Button(text="UNIT CONV.", font_size=16, background_color=BUTTON_COLOR, on_press=self.go_to_converter)
        mode_layout.add_widget(self.basic_btn)
        mode_layout.add_widget(self.sci_btn)
        mode_layout.add_widget(self.conv_btn)
        self.layout.add_widget(mode_layout)
        
        self.button_container = BoxLayout(orientation='horizontal', size_hint_y=0.67)
        self.layout.add_widget(self.button_container)
        
        self.create_basic_buttons()
        self.current_mode = 'basic'

    def go_to_converter(self, instance):
        self.manager.current = 'converter'

    def toggle_mode(self, instance):
        self.button_container.clear_widgets()
        
        if instance.text == "SCI/ADV":
            self.create_sci_buttons()
            self.sci_btn.background_color = ACCENT_COLOR
            self.basic_btn.background_color = BUTTON_COLOR
            self.current_mode = 'sci'
        else:
            self.create_basic_buttons()
            self.basic_btn.background_color = ACCENT_COLOR
            self.sci_btn.background_color = BUTTON_COLOR
            self.current_mode = 'basic'

    def create_basic_buttons(self):
        self.button_container.clear_widgets()
        basic_buttons = [
            'C', '(', ')', '/',
            '7', '8', '9', '*',
            '4', '5', '6', '-',
            '1', '2', '3', '+',
            '+/-', '0', '.', '='
        ]
        grid = GridLayout(cols=4, spacing=2)
        
        for text in basic_buttons:
            btn = self.create_button(text)
            grid.add_widget(btn)
        self.button_container.add_widget(grid)

    def create_sci_buttons(self):
        self.button_container.clear_widgets()
        
        sci_buttons = [
            'sin', 'cos', 'tan', 'log',
            'asin', 'acos', 'atan', 'ln',
            'x^2', 'x^y', 'sqrt', '1/x',
            'π', 'e', '(', ')',
        ]
        sci_grid = GridLayout(cols=4, spacing=2, size_hint_x=0.4)
        for text in sci_buttons:
            btn = self.create_button(text, font_size=20, bg_color=(0.15, 0.15, 0.15, 1))
            sci_grid.add_widget(btn)
        
        self.button_container.add_widget(sci_grid)
        
        basic_buttons = [
            'C', '/',
            '7', '*',
            '4', '-',
            '1', '+',
            '0', '='
        ]
        basic_grid = GridLayout(cols=2, spacing=2, size_hint_x=0.6)
        for text in basic_buttons:
            btn = self.create_button(text)
            basic_grid.add_widget(btn)
        self.button_container.add_widget(basic_grid)

    def create_button(self, text, font_size=28, bg_color=BUTTON_COLOR):
        btn = Button(
            text=text, 
            font_size=font_size, 
            background_color=bg_color,
            color=(1, 1, 1, 1), 
            on_press=self.on_button_press
        )
        if text in ['/', '*', '-', '+', '=']:
            btn.background_color = OPERATOR_COLOR
        if text == 'C':
            btn.background_color = CLEAR_COLOR
        return btn

    def on_button_press(self, instance):
        current_text = self.display.text
        button_text = instance.text
        
        if button_text == 'C':
            self.display.text = "0"
            
        elif button_text == '=':
            self.display.text = calculate(current_text)

        elif button_text in ['sin', 'cos', 'tan', 'log', 'ln', 'x^2', 'x^y', 'sqrt', 'π', 'e', 'asin', 'acos', 'atan', '1/x']:
            self._handle_scientific(button_text)

        elif button_text == '+/-':
            if current_text != "0" and not current_text.startswith('Error'):
                if current_text.startswith('-'):
                    self.display.text = current_text[1:]
                else:
                    self.display.text = '-' + current_text

        else:
            if current_text == "0" and button_text not in ['+', '-', '*', '/', '.', '(', ')']:
                self.display.text = button_text
            elif current_text.startswith("Error"):
                self.display.text = button_text
            else:
                self.display.text += button_text

    def _handle_scientific(self, func):
        current_text = self.display.text
        
        if func in ['π', 'e', '^']:
            self.display.text += func
        elif func == 'x^2':
            self.display.text = calculate(f"({current_text})**2")
        elif func == 'sqrt':
            self.display.text = calculate(f"math.sqrt({current_text})")
        elif func == '1/x':
            self.display.text = calculate(f"1/({current_text})")
        
        elif func in ['sin', 'cos', 'tan', 'log', 'ln', 'asin', 'acos', 'atan']:
            # বৈজ্ঞানিক ফাংশন সরাসরি গণনার জন্য ইনপুট তৈরি
            if current_text != '0' and not current_text.startswith('Error'):
                self.display.text = self._calculate(f"math.{func}({current_text})")
            else:
                self.display.text = f"math.{func}(" # ফাংশন ইনপুট শুরুর জন্য


# --- ২. ইউনিট কনভার্টার স্ক্রিন ---
class ConverterScreen(Screen):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_type = 'Length' # ডিফল্ট টাইপ
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # ব্যাক বাটন
        self.layout.add_widget(Button(
            text="< BACK TO CALCULATOR", 
            size_hint_y=0.1, 
            background_color=BUTTON_COLOR, 
            on_press=self.go_back,
            font_size=18
        ))
        self.add_widget(self.layout)
        
        # টাইপ সিলেক্টর
        self.type_spinner = Spinner(
            text='Select Unit Type',
            values=('Length', 'Weight', 'Temperature'),
            size_hint=(1, 0.1),
            font_size=20,
            on_text=self.update_converter
        )
        self.layout.add_widget(self.type_spinner)
        
        self.conversion_layout = GridLayout(cols=2, size_hint_y=0.3, spacing=10)
        self.layout.add_widget(self.conversion_layout)

        # ইনপুট লেবেল ও স্পিনার
        self.from_unit = Spinner(text='From Unit', values=[''], font_size=20)
        self.to_unit = Spinner(text='To Unit', values=[''], font_size=20)
        
        # ইনপুট/আউটপুট ডিসপ্লে (এখানে Button ব্যবহার করা হয়েছে ত্রুটি এড়ানোর জন্য)
        self.input_value = Button(
            text='0', 
            font_size=40, 
            background_color=(0.1, 0.1, 0.1, 1), 
            halign='right', 
            size_hint_y=None, 
            height=60, 
            disabled=True,
            disabled_color=(1,1,1,1) # ইনপুট টেক্সটের রঙ
        )
        self.output_value = Button(
            text='0', 
            font_size=40, 
            background_color=(0.1, 0.1, 0.1, 1), 
            halign='right', 
            size_hint_y=None, 
            height=60, 
            disabled=True,
            disabled_color=OPERATOR_COLOR # আউটপুট টেক্সটের রঙ
        )

        self.conversion_layout.add_widget(self.from_unit)
        self.conversion_layout.add_widget(self.to_unit)
        self.conversion_layout.add_widget(self.input_value)
        self.conversion_layout.add_widget(self.output_value)
        
        # কীপ্যাড (সংখ্যা ইনপুট)
        self.keypad = GridLayout(cols=4, spacing=2, size_hint_y=0.5)
        self.layout.add_widget(self.keypad)
        
        keys = ['7', '8', '9', 'C', '4', '5', '6', '.', '1', '2', '3', '0', '+', '-', '*', '/'] # কীপ্যাড বিন্যাস পরিবর্তন করা হয়েছে
        for text in keys:
            btn = Button(text=text, font_size=32, background_color=BUTTON_COLOR, on_press=self.on_keypad_press)
            if text in ['C']: btn.background_color = CLEAR_COLOR
            if text in ['+', '-', '*', '/']: btn.background_color = OPERATOR_COLOR
            self.keypad.add_widget(btn)

        self.from_unit.bind(text=self.perform_conversion)
        self.to_unit.bind(text=self.perform_conversion)
        self.update_converter(self.type_spinner, 'Length') # ডিফল্ট লোড

    def go_back(self, instance):
        self.manager.current = 'calc'

    def update_converter(self, spinner, text):
        self.current_type = text
        units = []
        if text == 'Length':
            units = ['m', 'km', 'cm', 'ft', 'in']
        elif text == 'Weight':
            units = ['kg', 'g', 'lb', 'oz']
        elif text == 'Temperature':
            units = ['C', 'F', 'K']
            
        self.from_unit.values = units
        self.to_unit.values = units
        self.from_unit.text = units[0]
        self.to_unit.text = units[1]
        self.input_value.text = '0'
        self.output_value.text = '0'
        
    def on_keypad_press(self, instance):
        key = instance.text
        current_input = self.input_value.text
        
        if key == 'C':
            self.input_value.text = '0'
        elif key.isdigit() or key == '.':
            if current_input == '0' and key.isdigit():
                self.input_value.text = key
            elif key == '.' and '.' not in current_input:
                self.input_value.text += key
            elif key.isdigit():
                 self.input_value.text += key
        
        # কনভার্টার মোডে শুধু সংখ্যা এবং দশমিক অনুমোদিত, অপারেটর নয়
        
        self.perform_conversion(None, None)

    def perform_conversion(self, instance, value):
        try:
            # এখানে ইউনিট কনভার্সনের লজিক অপরিবর্তিত আছে
            input_val = float(self.input_value.text)
            from_unit = self.from_unit.text
            to_unit = self.to_unit.text
            result = 0.0
            
            # (Length, Weight, Temperature এর কনভার্সন লজিক)
            if self.current_type == 'Length':
                base_val = input_val
                if from_unit == 'km': base_val *= 1000
                elif from_unit == 'cm': base_val /= 100
                elif from_unit == 'ft': base_val *= 0.3048
                elif from_unit == 'in': base_val *= 0.0254
                
                result = base_val
                if to_unit == 'km': result /= 1000
                elif to_unit == 'cm': result *= 100
                elif to_unit == 'ft': result /= 0.3048
                elif to_unit == 'in': result /= 0.0254

            elif self.current_type == 'Weight':
                base_val = input_val
                if from_unit == 'g': base_val /= 1000
                elif from_unit == 'lb': base_val *= 0.453592
                elif from_unit == 'oz': base_val *= 0.0283495
                
                result = base_val
                if to_unit == 'g': result *= 1000
                elif to_unit == 'lb': result /= 0.453592
                elif to_unit == 'oz': result /= 0.0283495

            elif self.current_type == 'Temperature':
                if from_unit == 'C': base_val = input_val + 273.15
                elif from_unit == 'F': base_val = (input_val - 32) * 5/9 + 273.15
                else: base_val = input_val
                
                if to_unit == 'C': result = base_val - 273.15
                elif to_unit == 'F': result = (base_val - 273.15) * 9/5 + 32
                else: result = base_val
            
            self.output_value.text = "{:.4f}".format(result)
            
        except:
            self.output_value.text = "Error"
        
        
# --- ৩. মূল অ্যাপ্লিকেশন ক্লাস ---
class AdvancedCalculatorApp(App):
    def build(self):
        Window.clearcolor = BG_COLOR
        sm = ScreenManager()
        
        calc_screen = CalcScreen(name='calc')
        sm.add_widget(calc_screen)
        
        converter_screen = ConverterScreen(name='converter')
        sm.add_widget(converter_screen)
        
        return sm

if __name__ == '__main__':
    AdvancedCalculatorApp().run()
