import os
import sys
import re
import traceback
import colorama  # Add to top with other imports
import time  # Add with other imports
colorama.init()

class KasketInterpreter:
    def __init__(self):
        self.variables = {}
        self.safe_dir = os.path.abspath(os.path.dirname(__file__))
        self.color_map = {
            1: colorama.Fore.RED,          2: colorama.Fore.GREEN,
            3: colorama.Fore.YELLOW,       4: colorama.Fore.BLUE,
            5: colorama.Fore.MAGENTA,      6: colorama.Fore.CYAN,
            7: colorama.Fore.LIGHTRED_EX,  8: colorama.Fore.LIGHTGREEN_EX,
            9: colorama.Fore.LIGHTYELLOW_EX,10: colorama.Fore.LIGHTBLUE_EX,
            11: colorama.Fore.LIGHTMAGENTA_EX,12: colorama.Fore.LIGHTCYAN_EX,
            13: colorama.Fore.WHITE,       14: colorama.Fore.BLACK,
            # Continue pattern up to 50 using available colorama colors
            49: colorama.Fore.LIGHTBLUE_EX,50: colorama.Fore.LIGHTWHITE_EX
        }
        self.current_color = colorama.Fore.WHITE
        self.delay_units = {
            'd': 86400, 'day': 86400, 'h': 3600, 'hour': 3600,
            'min': 60, 'minute': 60, 'sec': 1, 'second': 1
        }

    def execute(self, script):
        try:
            lines = [line.strip() for line in script.split('\n') if line.strip()]
            # Validate END command
            if not lines or lines[-1] != "END":
                raise SyntaxError("Missing required END command at script conclusion")
            
            for line_num, line in enumerate(lines[:-1], 1):  # Skip last line (END)
                if line.startswith('PRINT'):
                    self._handle_print(line)
                elif line.startswith('INPUT'):
                    self._handle_input(line)
                elif line.startswith('COLOR'):
                    self._handle_color(line)
                elif line.startswith('DELAY'):
                    self._handle_delay(line)
                else:
                    raise SyntaxError(f"Line {line_num}: Unknown command '{line.split()[0]}'")
        except Exception as e:
            print(f"\nERROR: {str(e)}")
            print(f"Traceback:\n{''.join(traceback.format_exc())}")
            input("Press Enter to exit...")
            sys.exit(1)

    def _handle_print(self, line):
        match = re.match(r'PRINT "(.*)"', line)
        if match:
            # Replace color codes and variables
            content = match.group(1)
            content = re.sub(r'\{COLOR:(\d+)\}', lambda m: str(self.color_map[int(m.group(1))]), content)
            content = re.sub(r'&(\w+)', lambda m: str(self.variables.get(m.group(1), "")), content)
            print(f"{content}{colorama.Style.RESET_ALL}")
        else:
            raise SyntaxError("Invalid PRINT statement")

    def _handle_input(self, line):
        """Handle INPUT command with validation and sanitization"""
        match = re.match(r'INPUT "(.*)" -> (\w+)', line)
        if not match:
            raise SyntaxError("Invalid INPUT format. Use: INPUT \"prompt\" -> variable")
        
        prompt, var_name = match.groups()
        
        # Print prompt with current color and get input
        print(f"{self.current_color}{prompt}: {colorama.Style.RESET_ALL}", end='')
        user_input = input().strip()
        
        # Basic input validation
        if len(user_input) > 1000:
            raise ValueError("Input exceeds maximum length of 1000 characters")
        if re.search(r'[^\w\s-]', user_input):
            user_input = re.sub(r'[^\w\s-]', '', user_input)
        
        self.variables[var_name] = user_input

    def _handle_color(self, line):
        match = re.match(r'COLOR (\d+)', line)
        if match:
            code = int(match.group(1))
            if code not in self.color_map:
                raise ValueError(f"Invalid color code: {code} (1-50 only)")
            self.current_color = self.color_map[code]
        else:
            raise SyntaxError("Invalid COLOR command")

    def _validate_path(self, path):
        """Ensure all file operations stay within safe directory"""
        full_path = os.path.abspath(path)
        if not full_path.startswith(self.safe_dir):
            raise SecurityError("Access to files outside script directory is prohibited")

    def _handle_delay(self, line):
        match = re.match(r'DELAY{time\.(\d+)([a-z]+)}', line)
        if match:
            value, unit = match.groups()
            delay_seconds = self._parse_delay_time(int(value), unit)
            if delay_seconds > 86400:
                raise ValueError("Maximum delay is 1 day (86400 seconds)")
            time.sleep(delay_seconds)
        else:
            raise SyntaxError("Invalid DELAY format")

    def _parse_delay_time(self, value, unit):
        unit = unit.lower()
        if unit not in self.delay_units:
            raise ValueError(f"Invalid time unit: {unit}")
        return value * self.delay_units[unit]

class SecurityError(Exception):
    pass

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage Error: Missing script file")
        print("Correct usage: kasket.bat your_script.kasket")
        input("Press Enter to exit...")
        sys.exit(1)
    
    try:
        script_path = os.path.abspath(sys.argv[1])
        if not os.path.exists(script_path):
            print(f"File Not Found Error: No such file '{sys.argv[1]}'")
            print("1. Check the file exists in the current directory")
            print("2. Verify the file extension is .kasket")
            input("Press Enter to exit...")
            sys.exit(1)
            
        with open(script_path, 'r') as f:
            script = f.read()
        
        interpreter = KasketInterpreter()
        interpreter.execute(script)
    except Exception as e:
        print(f"\nFatal Error: {str(e)}")
        input("Press Enter to exit...")
        sys.exit(1)