from tkinter import *
from tkinter import messagebox
from random import randint, shuffle, choice
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
# Password Generator Project

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


def generate_password():
    password_list = [choice(letters) for _ in range(randint(8, 12))]
    password_list += [choice(symbols) for _ in range(randint(4, 6))]
    password_list += [choice(numbers) for _ in range(randint(4, 6))]
    shuffle(password_list)
    password = "".join(password_list)

    entry_password.insert(END, string=f"{password}")
    # what this module (pyperclip, imported at the beginning) does is to automatically copy the password
    # we generate and then we can directly paste it wherever we want
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
# save to data.json file

def save_password():
    website = (entry_website.get()).capitalize()
    email = entry_email.get()
    password = entry_password.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showwarning(title="Oops", message="Please don't leave any fields empty!")
    else:
        try:
            with open("data.json", "r") as data_file:
                # Reading old data
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            # Updating old data with new data
            data.update(new_data)

            with open("data.json", "w") as data_file:
                # Saving updated data
                json.dump(data, data_file, indent=4)
        finally:
            entry_website.delete(0, END)
            entry_password.delete(0, END)


# ---------------------------- Find PASSWORD ------------------------------- #
def find_password():
    website = (entry_website.get()).capitalize()
    try:
        with open("data.json", "r") as data_file:
            # Reading old data
            data = json.load(data_file)
        if website in data:
            messagebox.showinfo(title=f"{website}",
                                message=f"Email: {data[website]['email']}\nPassword: {data[website]['password']}\n---------------------------------\nPassword Copied to Clipboard!")
            pyperclip.copy(data[website]['password'])
        else:
            messagebox.showerror(title=f"{website}", message="No details for the website exist")

    except FileNotFoundError:
        messagebox.showerror(title=f"{website}", message="No Data File Found")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager - Gero")
window.iconbitmap(bitmap="Gero_icon.ico")
window.config(padx=50, pady=50, bg="white")

# -------------  CANVAS IMAGE WITH LOGO -------------
canvas = Canvas(width=200, height=200, bg="white", highlightthickness=0)
logo_img = PhotoImage(file="Logo_Gero.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# -------------  LABELS -------------
lb_website = Label(text="Website:", font=("Arial", 12, "normal"), fg="black", bg="white")
lb_website.grid(column=0, row=1)

lb_email_us_name = Label(text="Email/Username:", font=("Arial", 12, "normal"), fg="black", bg="white")
lb_email_us_name.grid(column=0, row=2)

lb_password = Label(text="Password:", font=("Arial", 12, "normal"), fg="black", bg="white")
lb_password.grid(column=0, row=3)

# -------------  ENTRIES -------------
entry_website = Entry(width=32)
entry_website.focus()
entry_website.insert(END, string="")
entry_website.grid(column=1, row=1, columnspan=1)

entry_email = Entry(width=50)
entry_email.insert(END, string="gerozayas@gmail.com")
entry_email.grid(column=1, row=2, columnspan=2)

entry_password = Entry(width=32)
entry_password.insert(END, string="")
entry_password.grid(column=1, row=3, columnspan=1)

# -------------  Buttons -------------

add_button = Button(text="Add", command=save_password, width=42, bg="snow", relief=GROOVE)
add_button.grid(column=1, row=4, columnspan=2)

generate_pass_button = Button(text="Generate Password", command=generate_password, width=14, bg="snow", relief=GROOVE)
generate_pass_button.grid(column=2, row=3, columnspan=1)

search_button = Button(text="Search", command=find_password, width=14, bg="snow", relief=GROOVE)
search_button.grid(column=2, row=1, columnspan=1)

# -------------  End of Code
window.mainloop()
