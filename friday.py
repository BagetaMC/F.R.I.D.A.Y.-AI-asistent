import customtkinter as ctk
import speech_recognition as sr
import pyttsx3
import subprocess
import webbrowser
import threading
import psutil
import platform
import time
import os
import random

# ================== HLAS ==================
engine = pyttsx3.init()
engine.setProperty("rate", 165)

def speak(text):
    print("FRIDAY:", text)
    engine.stop()
    engine.say(text)
    engine.runAndWait()


# ================== LISTEN ==================
def listen():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio, language="cs-CZ")
        print("Ty:", text)
        return text.lower()
    except:
        return ""


# ================== PŘÍKAZY ==================
def run_command(command):

    if "chrome" in command:
        speak("Otevírám Chrome.")
        webbrowser.open("https://google.com")

    elif "youtube" in command:
        speak("Otevírám YouTube.")
        webbrowser.open("https://youtube.com")

    elif "discord" in command:
        speak("Otevírám Discord.")
        try:
            subprocess.Popen(
                os.path.expandvars(
                    r"%LocalAppData%\Discord\Update.exe"
                ) + " --processStart Discord.exe"
            )
        except:
            speak("Nepodařilo se otevřít Discord.")

    elif "minecraft" in command:
        speak("Spouštím Minecraft.")
        try:
            os.startfile(
                r"C:\XboxGames\Minecraft Launcher\Content\Minecraft.exe"
            )
        except:
            speak("Minecraft se nepodařilo otevřít.")

    elif "čas" in command:
        now = time.strftime("%H:%M")
        speak(f"Aktuální čas je {now}")

    elif "ukonči" in command:
        speak("Vypínám se.")
        os._exit(0)

    else:
        speak("Příkaz nerozpoznán.")


# ================== VOICE LOOP ==================
def voice_loop():
    while True:
        text = listen()

        if "friday" in text:
            speak("Ano?")
            cmd = listen()
            run_command(cmd)


# ================== UI ==================
ctk.set_appearance_mode("dark")

app = ctk.CTk()
app.geometry("900x500")
app.title("FRIDAY")
app.configure(fg_color="#050b18")

# ===== TOP =====
title = ctk.CTkLabel(
    app,
    text="F.R.I.D.A.Y",
    font=("Arial", 28, "bold"),
    text_color="#4cc9ff"
)
title.pack(pady=10)

main = ctk.CTkFrame(app, fg_color="#08101f")
main.pack(fill="both", expand=True, padx=20, pady=20)

# ===== LEFT PANEL =====
left = ctk.CTkFrame(main, width=250, fg_color="#0d1629")
left.pack(side="left", fill="y", padx=10, pady=10)

ctk.CTkLabel(left, text="SYSTEM INFO",
             font=("Arial", 18, "bold"),
             text_color="#4cc9ff").pack(pady=10)

cpu_l = ctk.CTkLabel(left, text="")
cpu_l.pack()

ram_l = ctk.CTkLabel(left, text="")
ram_l.pack()

gpu_l = ctk.CTkLabel(left, text="")
gpu_l.pack()

# ===== CENTER =====
center = ctk.CTkFrame(main, fg_color="transparent")
center.pack(expand=True)

canvas = ctk.CTkCanvas(center, width=300, height=300,
                       bg="#08101f", highlightthickness=0)
canvas.pack()

canvas.create_oval(70, 70, 230, 230,
                    outline="#4cc9ff", width=4)

canvas.create_text(150, 150,
                   text="FRIDAY",
                   fill="#4cc9ff",
                   font=("Arial", 20, "bold"))

# ===== STATUS =====
status = ctk.CTkLabel(app, text="STATUS: SPÍM",
                      text_color="#4cc9ff")
status.pack(pady=5)


# ================== SYSTEM INFO ==================
def update_system():
    while True:
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory()

        try:
            gpu = platform.processor()
        except:
            gpu = "Neznámá"

        cpu_l.configure(text=f"CPU: {cpu}%")
        ram_l.configure(text=f"RAM: {round(ram.used/1e9,1)} GB")
        gpu_l.configure(text=f"CPU INFO: {gpu}")

        time.sleep(1)


# ================== ANIMACE VLN ==================
bars = []

for i in range(8):
    bar = canvas.create_rectangle(
        40 + i*25, 250, 52 + i*25, 250,
        fill="#4cc9ff", outline=""
    )
    bars.append(bar)


def animate():
    while True:
        for b in bars:
            h = random.randint(10, 80)
            x1, _, x2, _ = canvas.coords(b)
            canvas.coords(b, x1, 260-h, x2, 260)
        time.sleep(0.12)


# ================== THREADS ==================
threading.Thread(target=voice_loop, daemon=True).start()
threading.Thread(target=update_system, daemon=True).start()
threading.Thread(target=animate, daemon=True).start()

app.mainloop()
