import tkinter as tk
from tkinter import messagebox
import json


def load_quiz_data(file_name):
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        messagebox.showerror("ERROR", "FILE NOT FOUND")
        exit(1)  # exit does not run the code any further
    except json.JSONDecodeError:
        messagebox.showerror("ERROR", "INVALID JSON")
        exit(1)


# filename always to be written as string
quiz_data = load_quiz_data("data.json")


class SpotTheScam:
    # initializing constructor
    def __init__(self, root):
        self.root = root
        self.root.title("Spot the Scam Quiz")
        self.root.geometry("600x400")
        self.root.resizable(True, True)

        self.score = 0
        self.q_no = 0

        self.home_page()

# HOME PAGE
    def home_page(self):
        self.screen_refresh()  # clears all the widgets
        frame = tk.Frame(self.root, bg="#C2E2FA")
        frame.pack(fill='both', expand=True)
        label = tk.Label(frame, text="Spot The Scam Quiz",
                         font=("Helvetica", 24, "bold"), bg="#C2E2FA")
        label.pack(pady=40)

        instructions = tk.Label(
            frame, text="Read the message carefully and decide: Scam or Legit?", font=("Helvetica", 14), fg="#7A0000", bg="#C2E2FA", )
        instructions.pack(pady=10)

        start_btn = tk.Button(frame, text="START", font=(
                              "helvetica", 18), bg="#60DF4F", command=self.quiz_start)
        start_btn.pack(pady=20)


# QUIZ START


    def quiz_start(self,):
        self.score = 0
        self.q_no = 0
        self.disp_q()

# DISPLAY QUESTION
    def disp_q(self):
        self.screen_refresh()
        q = quiz_data[self.q_no]  # gets the q of tht index
        msg_label = tk.Label(self.root, text="Situation:",
                             font=("Helvetica", 18, "underline"))
        msg_label.pack_configure(padx=20, pady=20)
        msg_txt = tk.Text(self.root, width=70, height=7,
                          wrap=tk.WORD, font=("Helvetica", 12))
        msg_txt.insert(tk.END, q["message"])
        # disabled so users cant edit txt
        msg_txt.config(state=tk.DISABLED, bg="#F5EEDC")
        msg_txt.pack(padx=2, pady=2)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        scam_btn = tk.Button(btn_frame, text="SCAM!", width=12, font=(
            "Helvetica", 14), bg="#ff6666", command=lambda: self.check_ans("Scam"))
        # here lambda is an anonymous function used to execute a certain func only after the button is pressed
        scam_btn.grid(row=0, column=0, padx=20)

        legit_btn = tk.Button(btn_frame, text="LEGIT", width=12, font=(
            "Helvetica", 14), bg="#1dd545", command=lambda: self.check_ans("Legit"))
        legit_btn.grid(row=0, column=1, padx=20)

        tips_btn = tk.Button(self.root, text="Scam Spotting Tips", font=(
            "Helvetica", 12), bg="#DDA853", command=self.show_tips)
        tips_btn.pack(pady=5)

# CHECK ANS
    def check_ans(self, ans):
        q = quiz_data[self.q_no]
        correct = q["answer"]
        expl = q["explanation"]

        if ans == correct:
            self.score += 1
            messagebox.showinfo("CORRECT", f"Correct!\n{expl}")
        else:
            messagebox.showwarning("WRONG", f"Ooops! wrong answer\n{expl}")

        self.q_no += 1
        if self.q_no < len(quiz_data):
            self.disp_q()
        else:
            self.disp_score()

# SHOW SCORE
    def disp_score(self):
        self.screen_refresh()
        score = tk.Label(
            self.root, text=f"You scored {self.score} out of {len(quiz_data)}", font=("Helvetica", 20))
        score.pack(pady=50)

        if self.score == len(quiz_data):
            msg = "Excellent! You're a scam-spotting pro.\n :))"
        elif self.score >= len(quiz_data) // 2:
            msg = "Good job! Stay alert out there.\n :))"
        else:
            msg = "Keep learning, scammers are tricky!\n :))"

        msg_label = tk.Label(self.root, text=msg, font=("Helvetica", 16))
        msg_label.pack(pady=10)

        restart_btn = tk.Button(self.root, text="Restart Quiz", font=(
            "Helvetica", 14), command=self.quiz_start)
        restart_btn.pack(pady=20)

        exit_btn = tk.Button(self.root, text="Exit", font=(
            "Helvetica", 14), command=self.root.destroy)
        exit_btn.pack()

    # TIPS
    def show_tips(self):
        tips = ("1. Be wary of urgent requests.\n"
                "2. Check sender's email/phone carefully.\n"
                "3. Don't click suspicious links.\n"
                "4. Look for spelling mistakes.\n"
                "5. Never give personal info over email.")
        messagebox.showinfo("Scam Spotting Tips", tips)

    # SCREEN REFRESH

    def screen_refresh(self):
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = SpotTheScam(root)
    root.mainloop()
