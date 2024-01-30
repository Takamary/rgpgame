import tkinter as tk
from tkinter import messagebox
import json
import os
import random

class Character:
    def __init__(self, character_id, name, class_type, strength=10, agility=10, intelligence=10, experience=0, level=1, health=100, admin="off"):
        self.character_id = character_id
        self.name = name
        self.class_type = class_type
        self.strength = max(0, min(strength, 999))
        self.agility = max(0, min(agility, 999))
        self.intelligence = max(0, min(intelligence, 999))
        self.experience = max(0, min(experience, 999))
        self.level = max(1, min(level, 999))
        self.base_health = 100
        self.health_per_level = 10
        self.health = self.calculate_health()
        self.damage = self.calculate_damage()
        self.admin = admin

    def calculate_health(self):
        return self.base_health + (self.level - 1) * self.health_per_level

    def calculate_damage(self):
        base_damage = (self.strength + self.level) // 2
        damage_multiplier = random.uniform(0.8, 1.2)
        return round(base_damage * damage_multiplier)

def create_character(class_type, name_entry, character_label):
    global character

    character_id = len([f for f in os.listdir("prof") if f.endswith('.json')]) + 1
    character_name = name_entry.get()

    if not character_name:
        messagebox.showinfo("Error", "Please enter a name for your character.")
        return

    character = Character(character_id, character_name, class_type)
    save_character(character)
    show_profile(character_label)

def save_character(character):
    character_data = {
        "character_id": character.character_id,
        "name": character.name,
        "class_type": character.class_type,
        "strength": character.strength,
        "agility": character.agility,
        "intelligence": character.intelligence,
        "experience": character.experience,
        "level": character.level,
        "health": character.health,
        "admin": character.admin
    }

    with open(f"prof/{character.character_id}.json", "w") as file:
        json.dump(character_data, file)

def load_character_and_start(character_id, root, character_label):
    global character
    try:
        with open(f"prof/{character_id}.json", "r") as file:
            character_data = json.load(file)
            character = Character(**character_data)

        if character.admin == "on":
            admin_label = tk.Label(root, text="Admin Mode: ON")
            admin_label.pack()

        show_profile(character_label)
    except FileNotFoundError:
        messagebox.showinfo("Error", "Character not found with the provided ID.")

def open_admin_panel(admin_window, stats_label):
    global character

    strength_label = tk.Label(admin_window, text="Strength:")
    strength_label.grid(row=0, column=0)
    strength_entry = tk.Entry(admin_window)
    strength_entry.grid(row=0, column=1)

    agility_label = tk.Label(admin_window, text="Agility:")
    agility_label.grid(row=1, column=0)
    agility_entry = tk.Entry(admin_window)
    agility_entry.grid(row=1, column=1)

    intelligence_label = tk.Label(admin_window, text="Intelligence:")
    intelligence_label.grid(row=2, column=0)
    intelligence_entry = tk.Entry(admin_window)
    intelligence_entry.grid(row=2, column=1)

    health_label = tk.Label(admin_window, text="Health:")
    health_label.grid(row=3, column=0)
    health_entry = tk.Entry(admin_window)
    health_entry.grid(row=3, column=1)

    apply_changes_button = tk.Button(admin_window, text="Apply Changes", command=lambda: apply_admin_changes(strength_entry, agility_entry, intelligence_entry, health_entry, stats_label, admin_window))
    apply_changes_button.grid(row=4, column=0, columnspan=2)

def apply_admin_changes(strength_entry, agility_entry, intelligence_entry, health_entry, stats_label, admin_window):
    global character

    try:
        strength = int(strength_entry.get())
        agility = int(agility_entry.get())
        intelligence = int(intelligence_entry.get())
        health = int(health_entry.get())

        character.strength = max(0, min(strength, 999))
        character.agility = max(0, min(agility, 999))
        character.intelligence = max(0, min(intelligence, 999))
        character.base_health = max(1, min(health, 999))
        character.health = character.calculate_health()
        character.damage = character.calculate_damage()

        update_stats(stats_label)
        save_character(character)

        messagebox.showinfo("Admin Panel", "Changes applied successfully.")
    except ValueError:
        messagebox.showinfo("Error", "Please enter valid numerical values.")

    admin_window.destroy()

def open_reset_progress_window(stats_label):
    global character

    reset_progress_window = tk.Toplevel(root)
    reset_progress_window.title("Reset Progress")

    confirm_label = tk.Label(reset_progress_window, text="Are you sure you want to reset all progress? This action cannot be undone.")
    confirm_label.pack()

    reset_button = tk.Button(reset_progress_window, text="Reset Progress", command=lambda: reset_progress(stats_label, reset_progress_window))
    reset_button.pack()

def reset_progress(stats_label, reset_progress_window):
    characters_directory = "prof"

    for file_name in os.listdir(characters_directory):
        file_path = os.path.join(characters_directory, file_name)

        try:
            with open(file_path, "r") as file:
                character_data = json.load(file)
                character = Character(**character_data)

            character.strength = 10
            character.agility = 10
            character.intelligence = 10
            character.base_health = 100
            character.experience = 0
            character.level = 1
            character.health = character.calculate_health()
            character.damage = character.calculate_damage()

            save_character(character)

        except Exception as e:
            print(f"Error resetting progress for {file_path}: {e}")

    update_stats(stats_label)

    messagebox.showinfo("Reset Progress", "All progress has been reset.")

    reset_progress_window.destroy()

def open_stat_window(stats_label):
    stat_window = tk.Toplevel(root)
    stat_window.title("Stat Upgrade")

    strength_button = tk.Button(stat_window, text="Upgrade Strength", command=lambda: upgrade_stat("strength", stats_label))
    strength_button.pack()

    agility_button = tk.Button(stat_window, text="Upgrade Agility", command=lambda: upgrade_stat("agility", stats_label))
    agility_button.pack()

    intelligence_button = tk.Button(stat_window, text="Upgrade Intelligence", command=lambda: upgrade_stat("intelligence", stats_label))
    intelligence_button.pack()

    health_button = tk.Button(stat_window, text="Upgrade Health", command=lambda: upgrade_stat("health", stats_label))
    health_button.pack()

def upgrade_stat(stat, stats_label):
    global character
    if character is not None and character.admin == "off":
        if character.experience >= 100:
            character.experience -= 100
            if stat == "strength":
                character.strength = min(999, character.strength + 1)
            elif stat == "agility":
                character.agility = min(999, character.agility + 1)
            elif stat == "intelligence":
                character.intelligence = min(999, character.intelligence + 1)
            elif stat == "health":
                character.base_health += 10
                character.health = character.calculate_health()
            character.level = min(999, character.level + 1)

        update_stats(stats_label)

def update_stats(stats_label):
    global character
    if character is not None:
        stats_label.config(text=f"Strength: {character.strength}\nAgility: {character.agility}\n"
                                f"Intelligence: {character.intelligence}\n"
                                f"Level: {character.level}\nHealth: {character.health}\nDamage: {character.damage}")

def show_profile(character_label):
    if character is not None:
        character_label.config(text=f"Character ID: {character.character_id}\nName: {character.name}\nClass: {character.class_type}\n"
                                    f"Strength: {character.strength}\nAgility: {character.agility}\n"
                                    f"Intelligence: {character.intelligence}\n"
                                    f"Experience: {character.experience}\nLevel: {character.level}\n"
                                    f"Health: {character.health}\nAdmin: {character.admin}")

def open_adventure_window():
    adventure_window = tk.Toplevel(root)
    adventure_window.title("Adventure")

    go_forward_button = tk.Button(adventure_window, text="Go Forward", command=lambda: proceed_adventure(adventure_window))
    go_forward_button.pack()

    go_back_button = tk.Button(adventure_window, text="Go Back", command=adventure_window.destroy)
    go_back_button.pack()

def proceed_adventure(adventure_window):
    global character

    result = random.choice(["continue", "attack", "nothing", "found_chest"])

    if result == "continue":
        messagebox.showinfo("Adventure", "You continue your journey.")
    elif result == "attack":
        attack_result = messagebox.askquestion("Adventure", "You are attacked by a monster!\nDo you want to attack?")
        if attack_result == 'yes':
            attack_enemy(adventure_window)
        else:
            messagebox.showinfo("Adventure", "You chose to surrender. The monster spares you.")
            adventure_window.destroy()
    elif result == "found_chest":
        open_chest(character, adventure_window)
    else:
        messagebox.showinfo("Adventure", "Nothing interesting happens.")

def attack_enemy(adventure_window):
    global character

    enemy_health = random.randint(10, 30)
    enemy_damage = random.randint(5, 15)

    messagebox.showinfo("Battle", f"You are attacked by a monster!\nEnemy Health: {enemy_health}")

    while enemy_health > 0 and character.health > 0:
        attack_choice = messagebox.askquestion("Battle", "Do you want to attack?")
        if attack_choice == 'yes':
            character_damage = random.randint(5, 15)
            enemy_health -= character_damage
            messagebox.showinfo("Battle", f"You dealt {character_damage} damage to the monster!\nEnemy Health: {enemy_health}")

            if enemy_health > 0:
                enemy_attack = random.randint(3, 10)
                character.health -= enemy_attack
                character.health = max(0, character.health)
                messagebox.showinfo("Battle", f"The monster attacks! You lose {enemy_attack} health.\nYour Health: {character.health}")
        else:
            messagebox.showinfo("Battle", "You chose to surrender. The monster defeats you.")
            adventure_window.destroy()
            return

    if character.health <= 0:
        messagebox.showinfo("Battle", "You have been defeated. Your character died.")
        character = None
        show_profile(character_label)
    else:
        messagebox.showinfo("Battle", "Congratulations! You defeated the monster and gained 50 experience points.")
        character.experience += 50
        adventure_window.destroy()
        show_profile(character_label)

def open_chest(character, adventure_window):
    gold_amount = random.randint(20, 120)
    experience_gain = random.randint(20, 120)

    character.experience += experience_gain

    messagebox.showinfo("Found Chest", f"You found a chest!\n"
                                        f"Gold: {gold_amount}\n"
                                        f"Experience Gained: {experience_gain}")

    adventure_window.destroy()
    show_profile(character_label)

def on_create_button(class_type, name_entry, character_label):
    create_character(class_type, name_entry, character_label)

def on_show_profile_button(character_label):
    if character is not None:
        show_profile(character_label)

def on_adventure_button():
    if character is not None:
        open_adventure_window()

def on_update_stats_button(stats_label):
    if character is not None:
        open_stat_window(stats_label)

def on_admin_button(stats_label):
    if character is not None and character.admin == "on":
        open_admin_panel(tk.Toplevel(root), stats_label)

def on_reset_progress_button(stats_label):
    open_reset_progress_window(stats_label)

root = tk.Tk()
root.title("RPG Game")

class_type_label = tk.Label(root, text="Choose your class:")
class_type_label.pack()

class_types = ["Warrior", "Mage", "Rogue"]

for class_type in class_types:
    class_button = tk.Button(root, text=class_type, command=lambda class_type=class_type: on_create_button(class_type, name_entry, character_label))
    class_button.pack()

name_entry_label = tk.Label(root, text="Enter your character's name:")
name_entry_label.pack()

name_entry = tk.Entry(root)
name_entry.pack()

character_label = tk.Label(root, text="")
character_label.pack()

show_profile_button = tk.Button(root, text="Show Profile", command=lambda: on_show_profile_button(character_label))
show_profile_button.pack()

stats_label = tk.Label(root, text="")
stats_label.pack()

update_stats_button = tk.Button(root, text="Update Stats", command=lambda: on_update_stats_button(stats_label))
update_stats_button.pack()

adventure_button = tk.Button(root, text="Go on Adventure", command=on_adventure_button)
adventure_button.pack()

admin_button = tk.Button(root, text="Admin Panel", command=lambda: on_admin_button(stats_label))
admin_button.pack()

reset_progress_button = tk.Button(root, text="Reset Progress", command=lambda: on_reset_progress_button(stats_label))
reset_progress_button.pack()

load_character_id_label = tk.Label(root, text="Enter your character's ID to load:")
load_character_id_label.pack()

load_character_id_entry = tk.Entry(root)
load_character_id_entry.pack()

load_character_button = tk.Button(root, text="Load Character", command=lambda: load_character_and_start(int(load_character_id_entry.get()), root, character_label))
load_character_button.pack()

root.mainloop()
