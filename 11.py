import tkinter as tk
import random
import math

class Game:
    def __init__(self, root):
        self.root = root
        self.root.title("Tank vs Aliens")
        self.root.resizable(False, False)

        self.width = 600
        self.height = 400

        self.lives = 11
        self.score = 0

        
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg="black")
        self.canvas.pack() # Create canvas game

        self.tank_width = 60
        self.tank_height = 30
        self.tank = self.canvas.create_rectangle(self.width//2 - self.tank_width//2, self.height - self.tank_height - 10,
                                                 self.width//2 + self.tank_width//2, self.height - 10, fill="green")

        self.bullets = []
        self.aliens = []
        self.max_aliens = 211  # Max number of aliens at a time
        self.create_aliens()

        
        self.score_text = self.canvas.create_text(10, 10, anchor="nw", text=f"Score: {self.score}", fill="white", font=('Helvetica', 12))
        self.lives_text = self.canvas.create_text(self.width - 10, 10, anchor="ne", text=f"Lives: {self.lives}", fill="white", font=('Helvetica', 12)) # Display score and lives

        # Key bindings for tank movement and firing
        self.root.bind("<Left>", self.move_left)
        self.root.bind("<Right>", self.move_right)
        self.root.bind("<space>", self.fire_bullets)  # Fire multiple bullets at once

        self.update_game()

    def move_left(self, event):
        self.canvas.move(self.tank, -20, 0) """Move tank left."""

    def move_right(self, event):
        self.canvas.move(self.tank, 20, 0) """Move tank right."""

    def fire_bullets(self, event):"""Fire multiple bullets at once in different directions."""
        x1, y1, x2, y2 = self.canvas.coords(self.tank)
        angles = [54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108]  # Angles in degrees for each bullet
        speed = 10  # Speed of the bullet movement
        
        for angle in angles: # Convert angle to radian for trigonometric calculations
            radian = math.radians(angle)
            
            # Calculate the movement direction for each bullet
            dx = speed * math.cos(radian)
            dy = -speed * math.sin(radian)  # Bullets move upwards, hence negative sin
            
            # Create the bullet and store its movement direction
            bullet = {
                "id": self.canvas.create_oval(x1 + self.tank_width//2 - 5, y1 - 10, x1 + self.tank_width//2 + 5, y1 - 30, fill="pink"),
                "dx": dx,
                "dy": dy
            }
            self.bullets.append(bullet)

    def create_aliens(self):
        """Create aliens only if there are less than the maximum allowed (20)."""
        current_aliens = len(self.aliens)
        if current_aliens < self.max_aliens:
            num_aliens = self.max_aliens - current_aliens  # Create only enough aliens to reach max_aliens
            for _ in range(num_aliens):
                x = random.randint(50, self.width - 50)
                y = random.randint(-150, -50)
                alien = self.canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill="blue")
                self.aliens.append(alien)

    def update_game(self):
        """Game loop to update bullets, aliens, and check for collisions."""
        self.move_bullets()
        self.move_aliens()
        self.check_collisions()
        self.check_game_over()
        self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}") # Update score and lives
        self.canvas.itemconfig(self.lives_text, text=f"Lives: {self.lives}")

        # Continue the game if lives are not over
        if self.lives > 0:
            # Call the update_game method again after 30 ms
            self.root.after(30, self.update_game)

    def move_bullets(self):
        """Move bullets in their respective directions."""
        for bullet in self.bullets[:]:
            self.canvas.move(bullet["id"], bullet["dx"], bullet["dy"])
            x1, y1, x2, y2 = self.canvas.coords(bullet["id"])
            if y2 < 0 or x2 < 0 or x1 > self.width:  # Delete bullet if it goes off-screen
                self.canvas.delete(bullet["id"])
                self.bullets.remove(bullet)

    def move_aliens(self):
        """Move aliens downwards."""
        for alien in self.aliens[:]:
            self.canvas.move(alien, 0, 2)
            x1, y1, x2, y2 = self.canvas.coords(alien)
            if y2 >= self.height:  # If alien reaches the bottom, reduce lives
                self.lives -= 1
                self.canvas.delete(alien)
                self.aliens.remove(alien)
                self.create_aliens()  # Create a new alien after losing a life

    def check_collisions(self):
        """Check for collisions between bullets and aliens."""
        for bullet in self.bullets[:]:
            x1, y1, x2, y2 = self.canvas.coords(bullet["id"])
            for alien in self.aliens[:]:
                ax1, ay1, ax2, ay2 = self.canvas.coords(alien)
                if self.is_collision(x1, y1, x2, y2, ax1, ay1, ax2, ay2):
                    # If collision happens, remove bullet and alien
                    self.canvas.delete(bullet["id"])
                    self.canvas.delete(alien)
                    self.bullets.remove(bullet)
                    self.aliens.remove(alien)
                    self.score += 10  # Increase score
                    self.create_aliens()  # Create a new alien after hitting one
                    break

    def is_collision(self, x1, y1, x2, y2, ax1, ay1, ax2, ay2):
        """Check if two objects (bullet and alien) collide."""
        return not (x2 < ax1 or x1 > ax2 or y2 < ay1 or y1 > ay2)

    def check_game_over(self):
        """Check if the game is over (when the player loses all lives)."""
        if self.lives <= 0:
            self.canvas.create_text(self.width//2, self.height//2, text="GAME OVER", fill="red", font=('Helvetica', 30))
            self.root.after(1000, self.root.quit)  # Quit the game after 1 second


root = tk.Tk() # Create game window
game = Game(root)

root.mainloop() # Start game
