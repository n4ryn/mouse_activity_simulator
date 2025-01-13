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
        self.MOVEMENT_RADIUS = 40  # Maximum distance for movement
        self.MIN_PAUSE_DURATION = 1  # Minimum seconds between movements
        self.MAX_PAUSE_DURATION = 3  # Maximum seconds between movements
        self.MOVEMENT_SPEED = 0.3  # Duration of each movement
        
        # Available movement patterns
        self.MOVEMENT_PATTERNS = ['random', 'circle', 'square']
        
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
            random_x_offset = random.randint(-self.MOVEMENT_RADIUS, self.MOVEMENT_RADIUS)
            random_y_offset = random.randint(-self.MOVEMENT_RADIUS, self.MOVEMENT_RADIUS)
            return (current_position[0] + random_x_offset, current_position[1] + random_y_offset)
    
    def format_duration(self, seconds):
        return str(timedelta(seconds=int(seconds)))
    
    def start_simulation(self):
        try:
            # Initialize tracking variables
            start_position = pyautogui.position()
            simulation_start_time = time.time()
            movement_count = 0
            
            # Calculate when simulation should end
            simulation_end_time = simulation_start_time + self.SIMULATION_DURATION
            
            print(f"Activity simulation started at {datetime.now().strftime('%H:%M:%S')}")
            print(f"Simulation will run until {datetime.fromtimestamp(simulation_end_time).strftime('%H:%M:%S')}")
            print("Move to any screen corner to stop simulation")
            
            while time.time() < simulation_end_time:
                # Select random movement pattern
                selected_pattern = random.choice(self.MOVEMENT_PATTERNS)
                
                # Calculate next position
                target_position = self.get_next_position(selected_pattern, start_position)
                
                # Move to new position
                pyautogui.moveTo(target_position[0], target_position[1], duration=self.MOVEMENT_SPEED)
                movement_count += 1
                
                # Calculate and display simulation progress
                elapsed_time = time.time() - simulation_start_time
                remaining_time = self.SIMULATION_DURATION - elapsed_time
                completion_percentage = (elapsed_time / self.SIMULATION_DURATION) * 100
                
                # Update status display
                sys.stdout.write('\r')
                sys.stdout.write(f"Progress: {completion_percentage:.1f}% | Time remaining: {self.format_duration(remaining_time)} | Movements: {movement_count} | Pattern: {selected_pattern}")
                sys.stdout.flush()
                
                # Pause between movements
                time.sleep(random.uniform(self.MIN_PAUSE_DURATION, self.MAX_PAUSE_DURATION))
                
            print("\nActivity simulation completed successfully!")
            
        except pyautogui.FailSafeException:
            print("\nSimulation stopped - moved to corner")
        except KeyboardInterrupt:
            print("\nSimulation stopped by user")
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
        finally:
            print(f"Total movements: {movement_count}")
            print(f"Total simulation duration: {self.format_duration(time.time() - simulation_start_time)}")

if __name__ == "__main__":
    simulator = ActivitySimulator()
    simulator.start_simulation()