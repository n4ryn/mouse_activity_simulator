import pyautogui
import random
import time
from datetime import datetime, timedelta
import sys
import math

class ActivitySimulator:
    def __init__(self):
        # Safety feature - moving to corner stops the program
        pyautogui.FAILSAFE = True
        
        # Configuration parameters
        self.SIMULATION_DURATION = 7 * 60 * 60  # 7 hours in seconds
        self.MOVEMENT_RADIUS = 200  # Maximum distance for movement
        self.MIN_MOVEMENT_RADIUS = 50  # Minimum distance for movement
        self.MIN_PAUSE_DURATION = 1  # Minimum seconds between movements
        self.MAX_PAUSE_DURATION = 3  # Maximum seconds between movements
        self.MOVEMENT_SPEED = 0.3  # Duration of each movement
        self.KEYBOARD_PROBABILITY = 0.3  # 30% chance of keyboard action
        
        # Available movement patterns
        self.MOVEMENT_PATTERNS = ['random', 'circle', 'square']
        
        # Available keyboard patterns
        self.KEYBOARD_PATTERNS = [
            self.alt_tab,
            self.ctrl_alt_up,
            self.ctrl_alt_down,
            self.ctrl_tab,
            self.ctrl_shift_tab,
            self.alt_shift_tab
        ]
    
    def calculate_circular_coordinates(self, center_position, radius, angle_degrees):
        # Convert angle to radians and calculate new position
        angle_radians = math.radians(angle_degrees)
        new_x = center_position[0] + radius * math.cos(angle_radians)
        new_y = center_position[1] + radius * math.sin(angle_radians)
        return (int(new_x), int(new_y))
    
    def get_next_position(self, movement_type, current_position):
        if movement_type == 'circle':
            current_angle = (time.time() * 30) % 360  # Complete circle every 12 seconds
            return self.calculate_circular_coordinates(current_position, self.MOVEMENT_RADIUS, current_angle)
        elif movement_type == 'square':
            # Define square corner positions
            corner_positions = [
                (current_position[0] + self.MOVEMENT_RADIUS, current_position[1] + self.MOVEMENT_RADIUS),
                (current_position[0] + self.MOVEMENT_RADIUS, current_position[1] - self.MOVEMENT_RADIUS),
                (current_position[0] - self.MOVEMENT_RADIUS, current_position[1] - self.MOVEMENT_RADIUS),
                (current_position[0] - self.MOVEMENT_RADIUS, current_position[1] + self.MOVEMENT_RADIUS)
            ]
            current_corner = int((time.time() * 0.5) % 4)
            return corner_positions[current_corner]
        else:  # random movement
            # Generate random radius between MIN and MAX
            current_radius = random.randint(self.MIN_MOVEMENT_RADIUS, self.MOVEMENT_RADIUS)
            # Generate random angle and convert to radians
            angle = random.uniform(0, 2 * math.pi)
            # Calculate offset using polar coordinates for more natural movement
            random_x_offset = int(current_radius * math.cos(angle))
            random_y_offset = int(current_radius * math.sin(angle))
            return (current_position[0] + random_x_offset, current_position[1] + random_y_offset)
    
    def alt_tab(self):
        """Simulate Alt+Tab key combination"""
        pyautogui.keyDown('alt')
        pyautogui.press('tab')
        pyautogui.keyUp('alt')
        return "Alt+Tab"
    
    def ctrl_alt_up(self):
        """Simulate Ctrl+Alt+Up key combination"""
        pyautogui.keyDown('ctrl')
        pyautogui.keyDown('alt')
        pyautogui.press('up')
        pyautogui.keyUp('alt')
        pyautogui.keyUp('ctrl')
        return "Ctrl+Alt+Up"
    
    def ctrl_alt_down(self):
        """Simulate Ctrl+Alt+Down key combination"""
        pyautogui.keyDown('ctrl')
        pyautogui.keyDown('alt')
        pyautogui.press('down')
        pyautogui.keyUp('alt')
        pyautogui.keyUp('ctrl')
        return "Ctrl+Alt+Down"
    
    def ctrl_tab(self):
        """Simulate Ctrl+Tab key combination"""
        pyautogui.keyDown('ctrl')
        pyautogui.press('tab')
        pyautogui.keyUp('ctrl')
        return "Ctrl+Tab"
    
    def ctrl_shift_tab(self):
        """Simulate Ctrl+Shift+Tab key combination"""
        pyautogui.keyDown('ctrl')
        pyautogui.keyDown('shift')
        pyautogui.press('tab')
        pyautogui.keyUp('shift')
        pyautogui.keyUp('ctrl')
        return "Ctrl+Shift+Tab"
    
    def alt_shift_tab(self):
        """Simulate Alt+Shift+Tab key combination"""
        pyautogui.keyDown('alt')
        pyautogui.keyDown('shift')
        pyautogui.press('tab')
        pyautogui.keyUp('shift')
        pyautogui.keyUp('alt')
        return "Alt+Shift+Tab"
    
    def format_duration(self, seconds):
        return str(timedelta(seconds=int(seconds)))
    
    def start_simulation(self):
        try:
            # Initialize tracking variables
            start_position = pyautogui.position()
            simulation_start_time = time.time()
            movement_count = 0
            keyboard_count = 0
            
            # Calculate when simulation should end
            simulation_end_time = simulation_start_time + self.SIMULATION_DURATION
            
            print(f"Activity simulation started at {datetime.now().strftime('%H:%M:%S')}")
            print(f"Simulation will run until {datetime.fromtimestamp(simulation_end_time).strftime('%H:%M:%S')}")
            print("Move to any screen corner to stop simulation")
            
            while time.time() < simulation_end_time:
                # Decide between mouse movement and keyboard action
                if random.random() < self.KEYBOARD_PROBABILITY:
                    # Perform keyboard action
                    selected_keyboard_pattern = random.choice(self.KEYBOARD_PATTERNS)
                    pattern_name = selected_keyboard_pattern()
                    keyboard_count += 1
                    action_type = "Keyboard"
                    pattern_desc = pattern_name
                else:
                    # Perform mouse movement
                    selected_pattern = random.choice(self.MOVEMENT_PATTERNS)
                    target_position = self.get_next_position(selected_pattern, start_position)
                    pyautogui.moveTo(target_position[0], target_position[1], duration=self.MOVEMENT_SPEED)
                    movement_count += 1
                    action_type = "Mouse"
                    pattern_desc = selected_pattern
                
                # Calculate and display simulation progress
                elapsed_time = time.time() - simulation_start_time
                remaining_time = self.SIMULATION_DURATION - elapsed_time
                completion_percentage = (elapsed_time / self.SIMULATION_DURATION) * 100
                
                # Update status display
                sys.stdout.write('\r')
                sys.stdout.write(
                    f"Progress: {completion_percentage:.1f}% | "
                    f"Time remaining: {self.format_duration(remaining_time)} | "
                    f"Mouse moves: {movement_count} | "
                    f"Keyboard actions: {keyboard_count} | "
                    f"Last action: {action_type} ({pattern_desc})"
                )
                sys.stdout.flush()
                
                # Pause between actions
                time.sleep(random.uniform(self.MIN_PAUSE_DURATION, self.MAX_PAUSE_DURATION))
                
            print("\nActivity simulation completed successfully!")
            
        except pyautogui.FailSafeException:
            print("\nSimulation stopped - moved to corner")
        except KeyboardInterrupt:
            print("\nSimulation stopped by user")
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
        finally:
            print(f"Total mouse movements: {movement_count}")
            print(f"Total keyboard actions: {keyboard_count}")
            print(f"Total simulation duration: {self.format_duration(time.time() - simulation_start_time)}")

if __name__ == "__main__":
    simulator = ActivitySimulator()
    simulator.start_simulation()
