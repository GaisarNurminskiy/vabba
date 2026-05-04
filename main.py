import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
import os
import sys

# Конфигурация
FAVORITES_FILE = "favorites.json"
GITHUB_API_URL = "https://api.github.com/users/"

class GitHubUserFinder:
    def __init__(self, root):
        self.root = root
        self.root.title("GitHub User Finder")
        self.root.geometry("600x500")

        # Загрузка избранных пользователей
        self.favorites = self.load_favorites()

        # Создание интерфейса
        self.create_widgets()

    def create_widgets(self):
        # Поле поиска
        search_frame = ttk.Frame(self.root)
        search_frame.pack(pady=10, padx=20, fill="x")

        ttk.Label(search_frame, text="GitHub Username:").pack(side="left")
        self.search_entry = ttk.Entry(search_frame, width=30)
        self.search_entry.pack(side="left", padx=5)
        ttk.Button(search_frame, text="Search", command=self.search_user).pack(side="left")

        # Результаты поиска
        results_frame = ttk.LabelFrame(self.root, text="Search Results")
        results_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.results_list = tk.Listbox(results_frame, height=10)
        self.results_list.pack(fill="both", expand=True, padx=5, pady=5)

        # Кнопки действий
        button_frame = ttk.Frame(results_frame)
        button_frame.pack(pady=5)

        ttk.Button(button_frame, text="Add to Favorites", command=self.add_to_favorites).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Remove from Favorites", command=self.remove_from_favorites).pack(side="left", padx=5)

        # Список избранных
        favorites_frame = ttk.LabelFrame(self.root, text="Favorites")
        favorites_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.favorites_list = tk.Listbox(favorites_frame, height=8)
        self.favorites_list.pack(fill="both", expand=True, padx=5, pady=5)

        # Обновление списка избранных
        self.update_favorites_list()

    def search_user(self):
        """Поиск пользователя GitHub"""
        username = self.search_entry.get().strip()
        if not username:
            messagebox.showerror("Error", "Search field cannot be empty!")
            return

        try:
            response = requests.get(f"{GITHUB_API_URL}{username}")
            if response.status_code == 200:
                user_data = response.json()
                self.display_user(user_data)
            else:
                messagebox.showerror("Error", f"User not found: {username}")
        except requests.RequestException as e:
            messagebox.showerror("Error", f"Connection error: {e}")

    def display_user(self, user_data):
        """Отображение информации о пользователе"""
        self.results_list.delete(0, tk.END)
        info = f"{user_data['login']} - {user_data.get('name', 'No name')} - {user_data['public_repos']} repos"
        self.results_list.insert(tk.END, info)

    def add_to_favorites(self):
        """Добавление пользователя в избранное"""
        selection = self.results_list.curselection()
        if selection:
            user_info = self.results_list.get(selection[0])
            username = user_info.split(" - ")[0]
            if username not in self.favorites:
                self.favorites.append(username)
                self.save_favorites()
                self.update_favorites_list()
                messagebox.showinfo("Success", f"{username} added to favorites!")
            else:
                messagebox.showwarning("Warning", f"{username} is already in favorites!")
        else:
            messagebox.showwarning("Warning", "Select a user to add!")

    def remove_from_favorites(self):
        """Удаление пользователя из избранного"""
        selection = self.favorites_list.curselection()
        if selection:
            username = self.favorites_list.get(selection[0])
            self.favorites.remove(username)
            self.save_favorites()
            self.update_favorites_list()
            messagebox.showinfo("Success", f"{username} removed from favorites!")

    def load_favorites(self):
        """Загрузка избранных пользователей из JSON‑файла"""
        if os.path.exists(FAVORITES_FILE):
            with open(FAVORITES_FILE, "r") as f:
                return json.load(f)
        return []

    def save_favorites(self):
        """Сохранение избранных пользователей в JSON‑файл"""
        with open(FAVORITES_FILE, "w") as f:
            json.dump(self.favorites, f, indent=4)

    def update_favorites_list(self):
        """Обновление списка избранных пользователей"""
        self.favorites_list.delete(0, tk.END)
        for user in self.favorites:
            self.favorites_list.insert(tk.END, user)

def setup_git():
    """Настройка Git‑репозитория"""
    try:
        # Инициализация Git‑репозитория
        os.system("git init")
        # Создание .gitignore
        gitignore_content = """__pycache__/
*.pyc
*.pyo
*.pyd
.vscode/
.idea/
*.log
*.tmp
"""
        with open(".gitignore", "w") as f:
            f.write(gitignore_content)
        # Первый коммит
        os.system("git add .")
        os.system('git commit -m "Initial commit: GitHub User Finder setup"')
        print("Git repository initialized successfully!")
    except Exception as e:
        print(f"Git setup failed: {e}")
