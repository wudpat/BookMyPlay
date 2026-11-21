import abc
from user import User
from admin import Admin
from sport_facility import SportFacility
from booking import Booking
from tkinter import *
from tkinter import font, messagebox, filedialog
from tkcalendar import DateEntry
from PIL import Image, ImageOps, ImageTk
import datetime
import os
import pickle

class BookMyPlay(Tk):
    def __init__(self):
        super().__init__()
        self.title("BookMyPlay")
        self.geometry("1150x760")
        self.minsize(900, 600)
        self.users = list()
        self.admins = list()
        self.facilities_data = list()
        self.booking_data = dict()
        self.current_account = None
        self.data_file = "data.pkl"
        self.load_data()
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.pages = dict()

        self.header_color = "#EEEEEE"
        self.content_color = "#EAE2D6"
        self.card_color = "#F7F2EB"
        self.accept_color = "#8B9A6E"
        self.accept_hover = "#7A8960"
        self.reject_color = "#790D16"
        self.reject_hover = "#5E0A11"
        self.pending_color = "#C28A2C"
        self.selected_color = "#E5D3AF"
        self.neutral_color = "#DDD3C2"
        self.neutral_hover = "#CFC3AE"
        self.border_color = "#D9CFBD"
        self.text_color = "#2B2B2B"
        self.muted_color = "#6B6257"
        self.card_image_size = 200
        self.header_font = ("Bahnschrift SemiBold", 20)
        self.subheader_font = ("Bahnschrift", 16)
        self.title_font = ("Bahnschrift SemiBold", 16)
        self.button_font = ("Bahnschrift SemiBold", 12)
        self.small_font = ("Bahnschrift", 11)
        font.nametofont("TkDefaultFont").configure(family="Bahnschrift", size=14)
        font.nametofont("TkTextFont").configure(family="Bahnschrift", size=12)
        self.config(bg=self.content_color)

        for page_class in (SignUp, LogIn, UserMode, AdminMode):
            page = page_class(self)
            self.pages.update({page_class: page})
            page.grid(row=0, column=0, sticky="nsew")

        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.display(LogIn)
        self.mainloop()

    def display(self, page_class):
        page = self.pages[page_class]
        if hasattr(page, "on_show"):
            page.on_show()
        page.tkraise()

    def make_button(self, parent, text, kind="primary", command=None, **options):
        palette = {
            "primary": (self.accept_color, "white", self.accept_hover),
            "danger": (self.reject_color, "white", self.reject_hover),
            "neutral": (self.neutral_color, self.text_color, self.neutral_hover)
        }
        bg, fg, hover = palette[kind]
        settings = dict(text=text, bg=bg, fg=fg, activebackground=hover, activeforeground=fg,
                        relief=FLAT, bd=0, padx=18, pady=6, cursor="hand2", font=self.button_font, command=command)
        settings.update(options)
        button = Button(parent, **settings)
        button.bind("<Enter>", lambda e: button.config(bg=hover))
        button.bind("<Leave>", lambda e: button.config(bg=bg))
        return button

    def make_entry(self, parent, variable, width=28, show=None):
        return Entry(parent, textvariable=variable, width=width, show=show, relief=FLAT, bg="white",
                     fg=self.text_color, insertbackground=self.text_color, highlightthickness=1,
                     highlightbackground=self.border_color, highlightcolor=self.accept_color, font=("Bahnschrift", 13))

    def make_card(self, parent, padx=20, pady=20):
        return Frame(parent, bg=self.card_color, padx=padx, pady=pady, highlightthickness=1, highlightbackground=self.border_color)

    def make_radio(self, parent, text, variable, value):
        return Radiobutton(parent, text=text, variable=variable, value=value, font=("Bahnschrift", 13), bg=self.card_color,
                           activebackground=self.card_color, selectcolor="white", cursor="hand2", bd=0, highlightthickness=0)

    def save_data(self):
        saving_data = {"users": self.users, "admins": self.admins, "facilities_data": self.facilities_data, "booking_data": self.booking_data}
        try:
            with open(self.data_file, "wb") as file:
                pickle.dump(saving_data, file)
        except Exception as e:
            messagebox.showerror("Save failed", f"Cannot save the data.\n{e}")

    def load_data(self):
        try:
            with open(self.data_file, "rb") as file:
                loaded_file = pickle.load(file)
        except FileNotFoundError:
            return
        except Exception as e:
            messagebox.showerror("Load failed", f"Cannot load the previous data.\n{e}")
            return
        self.users = loaded_file["users"]
        self.admins = loaded_file["admins"]
        self.facilities_data = loaded_file["facilities_data"]
        self.booking_data = loaded_file["booking_data"]

    def on_close(self):
        self.save_data()
        self.destroy()

class SignUp(Frame):
    def __init__(self, main_window):
        super().__init__(main_window, bg=main_window.content_color)
        self.main_window = main_window
        self.grid_anchor("center")
        self.input_username = StringVar()
        self.input_password = StringVar()
        self.input_firstname = StringVar()
        self.input_surname = StringVar()
        self.input_account_type = StringVar(value="User")

        self.card = main_window.make_card(self, padx=50, pady=35)
        self.card.grid(row=0, column=0)

        self.header = Label(self.card, text="BookMyPlay Sign-Up", font=("Bahnschrift SemiBold", 24), bg=main_window.card_color, fg=main_window.text_color)
        self.username_label = Label(self.card, text="Username:", bg=main_window.card_color, fg=main_window.muted_color)
        self.username_entry = main_window.make_entry(self.card, self.input_username)
        self.password_label = Label(self.card, text="Password:", bg=main_window.card_color, fg=main_window.muted_color)
        self.password_entry = main_window.make_entry(self.card, self.input_password, show="*")
        self.firstname_label = Label(self.card, text="First name", bg=main_window.card_color, fg=main_window.muted_color)
        self.firstname_entry = main_window.make_entry(self.card, self.input_firstname)
        self.surname_label = Label(self.card, text="Surname", bg=main_window.card_color, fg=main_window.muted_color)
        self.surname_entry = main_window.make_entry(self.card, self.input_surname)
        self.account_type_label = Label(self.card, text="Account type", bg=main_window.card_color, fg=main_window.muted_color)
        self.radio_frame = Frame(self.card, bg=main_window.card_color)
        self.user_type = main_window.make_radio(self.radio_frame, "User", self.input_account_type, "User")
        self.admin_type = main_window.make_radio(self.radio_frame, "Admin", self.input_account_type, "Admin")
        self.user_type.pack(side=LEFT, padx=(0, 15))
        self.admin_type.pack(side=LEFT)
        self.sign_up_button = main_window.make_button(self.card, "Sign Up", "primary", command=lambda: self.register_acc())
        self.back_to_login = main_window.make_button(self.card, "Back to Login", "neutral", command=lambda: self.main_window.display(LogIn))

        self.form_toggle()
        self.input_account_type.trace_add("write", self.form_toggle)

    def form_toggle(self, *args):
        for widget in self.card.winfo_children():
            widget.grid_forget()
        
        self.header.grid(row=0, column=0, columnspan=2, pady=(0, 25))
        fields = [(self.username_label, self.username_entry), (self.password_label, self.password_entry)]
        if self.input_account_type.get() == "User":
            fields += [(self.firstname_label, self.firstname_entry), (self.surname_label, self.surname_entry)]
        current_row = 1
        for label, entry in fields:
            label.grid(row=current_row, column=0, sticky="w", pady=8, padx=(0, 20))
            entry.grid(row=current_row, column=1, sticky="ew", pady=8, ipady=4)
            current_row += 1

        self.account_type_label.grid(row=current_row, column=0, sticky="w", pady=8, padx=(0, 20))
        self.radio_frame.grid(row=current_row, column=1, sticky="w")
        current_row += 1
        self.sign_up_button.grid(row=current_row, column=0, columnspan=2, sticky="ew", pady=(25, 8))
        current_row += 1
        self.back_to_login.grid(row=current_row, column=0, columnspan=2, sticky="ew")

    def register_acc(self):
        if not self.input_username.get().strip() or not self.input_password.get().strip() or (self.input_account_type.get() == "User" and (not self.input_firstname.get().strip() or not self.input_surname.get().strip())):
            messagebox.showerror("Registration failed", "Please fill in all fields.")
        elif any(user.username.lower() == self.input_username.get().lower() for user in self.main_window.users) or any(admin.username.lower() == self.input_username.get().lower() for admin in self.main_window.admins):
            messagebox.showerror("Registration failed", "This username already exists.")
        elif self.input_account_type.get() == "User":
            new_account = User(self.input_username.get(), self.input_password.get(), self.input_firstname.get(), self.input_surname.get(), self.main_window.booking_data)
            self.main_window.users.append(new_account)
            self.main_window.current_account = new_account
            self.main_window.display(UserMode)
            messagebox.showinfo("Registration successful", "Your user account has been registered.")
        else:
            new_account = Admin(self.input_username.get(), self.input_password.get(), self.main_window.facilities_data, self.main_window.booking_data)
            self.main_window.admins.append(new_account)
            self.main_window.current_account = new_account
            self.main_window.display(AdminMode)
            messagebox.showinfo("Registration successful", "Your admin account has been registered.")

    def on_show(self):
        self.input_username.set("")
        self.input_password.set("")
        self.input_firstname.set("")
        self.input_surname.set("")
        self.input_account_type.set("User")

class LogIn(Frame):
    def __init__(self, main_window):
        super().__init__(main_window, bg=main_window.content_color)
        self.main_window = main_window
        self.grid_anchor("center")
        self.input_username = StringVar()
        self.input_password = StringVar()
        self.input_account_type = StringVar(value="User")

        self.card = main_window.make_card(self, padx=50, pady=35)
        self.card.grid(row=0, column=0)

        self.header = Label(self.card, text="BookMyPlay Log-In", font=("Bahnschrift SemiBold", 24), bg=main_window.card_color, fg=main_window.text_color)
        self.username_label = Label(self.card, text="Username", bg=main_window.card_color, fg=main_window.muted_color)
        self.username_entry = main_window.make_entry(self.card, self.input_username)
        self.password_label = Label(self.card, text="Password", bg=main_window.card_color, fg=main_window.muted_color)
        self.password_entry = main_window.make_entry(self.card, self.input_password, show="*")
        self.account_type_label = Label(self.card, text="Account type", bg=main_window.card_color, fg=main_window.muted_color)
        self.radio_frame = Frame(self.card, bg=main_window.card_color)
        self.user_type = main_window.make_radio(self.radio_frame, "User", self.input_account_type, "User")
        self.admin_type = main_window.make_radio(self.radio_frame, "Admin", self.input_account_type, "Admin")
        self.log_in_button = main_window.make_button(self.card, "Log In", "primary", command=lambda: self.log_in())
        self.go_to_signup = main_window.make_button(self.card, "Go to Sign-Up", "neutral", command=lambda: self.main_window.display(SignUp))

        self.header.grid(row=0, column=0, columnspan=2, pady=(0, 25))
        self.username_label.grid(row=1, column=0, sticky="w", pady=8, padx=(0, 20))
        self.username_entry.grid(row=1, column=1, sticky="ew", pady=8, ipady=4)
        self.password_label.grid(row=2, column=0, sticky="w", pady=8, padx=(0, 20))
        self.password_entry.grid(row=2, column=1, sticky="ew", pady=8, ipady=4)
        self.account_type_label.grid(row=3, column=0, sticky="w", pady=8, padx=(0, 20))
        self.radio_frame.grid(row=3, column=1, sticky="w")
        self.user_type.pack(side=LEFT, padx=(0, 15))
        self.admin_type.pack(side=LEFT)
        self.log_in_button.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(25, 8))
        self.go_to_signup.grid(row=5, column=0, columnspan=2, sticky="ew")

    def log_in(self):
        if self.input_account_type.get() == "User":
            username_match = next(iter([user for user in self.main_window.users if user.username == self.input_username.get()]), None)
            if username_match == None:
                messagebox.showerror("Login failed", "Username not found")
            elif username_match.getPassword() == self.input_password.get():
                self.main_window.current_account = username_match
                self.main_window.display(UserMode)
            else:
                messagebox.showerror("Login failed", "Incorrect password")
        else:
            username_match = next(iter([admin for admin in self.main_window.admins if admin.username == self.input_username.get()]), None)
            if username_match == None:
                messagebox.showerror("Login failed", "Username not found")
            elif username_match.getPassword() == self.input_password.get():
                self.main_window.current_account = username_match
                self.main_window.display(AdminMode)
            else:
                messagebox.showerror("Login failed", "Incorrect password")

    def on_show(self):
        self.input_username.set("")
        self.input_password.set("")
        self.input_account_type.set("User")

class ModePage(Frame, metaclass=abc.ABCMeta):
    def __init__(self, main_window, role):
        super().__init__(main_window, bg=main_window.content_color)
        self.main_window = main_window
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.role = role
        self.images = list()
        self.tab_widgets = dict()
        self.current_tab = None
        self.header()
        self.content()

    def header(self):
        self.header_frame = Frame(self, bg=self.main_window.header_color)
        self.header_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
        self.header_frame.columnconfigure(1, weight=1)
        self.app_title = Label(self.header_frame, text="BookMyPlay", font=self.main_window.header_font, bg=self.main_window.header_color, fg=self.main_window.text_color)
        self.username_label = Label(self.header_frame, font=self.main_window.subheader_font, bg=self.main_window.header_color, fg=self.main_window.muted_color)
        self.log_out_button = self.main_window.make_button(self.header_frame, "Log Out", "neutral", command=self.log_out, padx=14, pady=4)

        self.app_title.grid(row=0, column=0, sticky="w", padx=(30, 0), pady=(15, 0))
        self.username_label.grid(row=0, column=2, sticky="e", padx=(0, 20), pady=(15, 0))
        self.log_out_button.grid(row=0, column=3, padx=(0, 30), pady=(15, 0))

        self.tabs_frame = Frame(self.header_frame, bg=self.main_window.header_color)
        self.tabs_frame.grid(row=1, column=0, columnspan=4, sticky="w", padx=(30, 0), pady=(8, 0))

        for col, (tab_text, cmd) in enumerate(self.tabs):
            tab = Frame(self.tabs_frame, bg=self.main_window.header_color, cursor="hand2")
            tab_label = Label(tab, text=tab_text, font=self.main_window.subheader_font, bg=self.main_window.header_color, fg=self.main_window.muted_color, cursor="hand2", padx=6)
            indicator = Frame(tab, height=3, bg=self.main_window.header_color)
            tab_label.pack()
            indicator.pack(fill=X, pady=(4, 0))
            tab.grid(row=0, column=col, padx=(0, 35))
            for widget in (tab, tab_label, indicator):
                widget.bind("<Button-1>", lambda e, c=cmd: self.open_tab(c))
            self.tab_widgets.update({cmd: (tab_label, indicator)})

        thin_border = Frame(self.header_frame, height=1, bg=self.main_window.border_color)
        thin_border.grid(row=2, column=0, columnspan=4, sticky="ew")

    def highlight_tab(self):
        for cmd, (label, indicator) in self.tab_widgets.items():
            if cmd == self.current_tab:
                label.config(fg=self.main_window.text_color, font=self.main_window.title_font)
                indicator.config(bg=self.main_window.accept_color)
            else:
                label.config(fg=self.main_window.muted_color, font=self.main_window.subheader_font)
                indicator.config(bg=self.main_window.header_color)

    def content(self):
        self.scrollable = True
        self.canvas = Canvas(self, bg=self.main_window.content_color, highlightthickness=0, yscrollincrement=20)
        self.scrollbar = Scrollbar(self, orient=VERTICAL, command=self.canvas.yview)
        self.canvas.config(yscrollcommand=self.scrollbar.set)
        self.canvas.grid(row=1, column=0, sticky="nsew")
        self.scrollbar.grid(row=1, column=1, sticky="ns")

        self.content_frame = Frame(self.canvas, bg=self.main_window.content_color)
        self.content_frame.grid_anchor("center")
        self.canvas_window = self.canvas.create_window((0, 0), window=self.content_frame, anchor="center")
        self.content_frame.bind("<Configure>", self.update_scroll_region)
        self.canvas.bind("<Configure>", self.update_scroll_region)
        self.bind_all("<MouseWheel>", self.on_mousewheel, add="+")

    def update_scroll_region(self, event=None):
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        if self.scrollable:
            width = max(canvas_width, self.content_frame.winfo_reqwidth())
            height = max(canvas_height, self.content_frame.winfo_reqheight())
        else:
            width = canvas_width
            height = canvas_height
        self.canvas.coords(self.canvas_window, width // 2, height // 2)
        self.canvas.config(scrollregion=(0, 0, width, height))

    def on_mousewheel(self, event):
        if not self.scrollable or self.canvas.yview() == (0, 1):
            return
        try:
            widget = self.winfo_containing(event.x_root, event.y_root)
        except KeyError:
            return
        while widget is not None and widget is not self.header_frame and widget is not self:
            widget = widget.master
        if widget is not self:
            return
        if event.num == 4:
            step = -3
        elif event.num == 5:
            step = 3
        else:
            step = -3 if event.delta > 0 else 3
        self.canvas.yview_scroll(step, "units")

    def load_image(self, path):
        try:
            img = Image.open(path)
            img = ImageOps.fit(img, (self.main_window.card_image_size, self.main_window.card_image_size))
        except (FileNotFoundError, AttributeError, TypeError, OSError):
            img = Image.new("RGB", (self.main_window.card_image_size, self.main_window.card_image_size), "#B8B8B8")
        return ImageTk.PhotoImage(img)

    def clear_view(self, scrollable=True):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        for column in range(8):
            self.content_frame.columnconfigure(column, minsize=0, weight=0)
        self.images.clear()
        self.scrollable = scrollable
        if self.scrollable:
            self.scrollbar.grid()
        else:
            self.scrollbar.grid_remove()
        self.canvas.yview_moveto(0)
        self.update_scroll_region()

    def empty_state(self, text):
        empty_label = Label(self.content_frame, text=text, font=self.main_window.subheader_font, bg=self.main_window.content_color, fg=self.main_window.muted_color)
        empty_label.grid(row=0, column=0, pady=80)

    def status_color(self, status):
        return {"Approved": self.main_window.accept_color, "Pending": self.main_window.pending_color}.get(status, self.main_window.reject_color)

    def booking_card(self, id, booking):
        card = self.main_window.make_card(self.content_frame)
        fac_image = self.load_image(booking.site.image)
        self.images.append(fac_image)
        image_label = Label(card, image=fac_image, bg=self.main_window.card_color, bd=0)
        fac_name_label = Label(card, text=booking.site.name, font=self.main_window.title_font, bg=self.main_window.card_color, fg=self.main_window.text_color)
        status_label = Label(card, text=booking.getStatus(), font=self.main_window.small_font, bg=self.status_color(booking.getStatus()), fg="white", padx=12, pady=3)

        time_slot = booking.getTimeSlot()
        details = [("Booking ID", id),
                   ("Booker", booking.booker_name),
                   ("Date", time_slot[0]),
                   ("Time", f"{time_slot[1][0]:02d}:00 - {time_slot[1][1]:02d}:00"),
                   ("Total Fee", f"฿{booking.getTotalFee():.2f}")]
        details_frame = Frame(card, bg=self.main_window.card_color)
        for row, (head, value) in enumerate(details):
            head_label = Label(details_frame, text=head, bg=self.main_window.card_color, fg=self.main_window.muted_color)
            value_label = Label(details_frame, text=value, bg=self.main_window.card_color, fg=self.main_window.text_color)
            head_label.grid(row=row, column=0, sticky="w", padx=(0, 25), pady=2)
            value_label.grid(row=row, column=1, sticky="w", pady=2)

        actions = Frame(card, bg=self.main_window.card_color)
        self.build_actions(actions, id, booking)

        card.columnconfigure(1, weight=1)
        image_label.grid(row=0, column=0, rowspan=3, padx=(0, 25), sticky="n")
        fac_name_label.grid(row=0, column=1, sticky="w")
        status_label.grid(row=0, column=2, sticky="e")
        details_frame.grid(row=1, column=1, columnspan=2, sticky="w", pady=(10, 0))
        actions.grid(row=2, column=1, columnspan=2, sticky="se", pady=(10, 0))
        return card

    @abc.abstractmethod
    def build_actions(self, parent, id, booking):
        pass

    def log_out(self):
        self.main_window.current_account = None
        self.main_window.display(LogIn)

    def open_tab(self, tab_method):
        self.current_tab = tab_method
        self.highlight_tab()
        tab_method()

    def refresh(self):
        scroll_position = self.canvas.yview()[0]
        self.current_tab()
        self.update_idletasks()
        self.update_scroll_region()
        self.canvas.yview_moveto(scroll_position)

    def on_show(self):
        self.username_label.config(text=f"{self.role}: {self.main_window.current_account.username}")
        self.open_tab(getattr(self, self.default_tab))

class UserMode(ModePage):
    def __init__(self, main_window):
        self.tabs = [("Booking", self.show_booking), ("My Bookings", self.show_my_bookings)]
        self.default_tab = "show_booking"
        super().__init__(main_window, "User")

    def show_booking(self, *args):
        self.clear_view()
        if not self.main_window.facilities_data:
            self.empty_state("No facilities available yet.")
            return
        for i, fac in enumerate(self.main_window.facilities_data):
            current_row, current_column = divmod(i, 3)
            self.book_fac_card(fac, True).grid(row=current_row, column=current_column, padx=12, pady=12, sticky="n")

    def show_my_bookings(self, *args):
        self.clear_view()
        if not self.main_window.current_account.getBookings():
            self.empty_state("You have no bookings yet.")
            return
        self.content_frame.columnconfigure(0, minsize=700)
        for current_row, (id, booking) in enumerate(self.main_window.current_account.getBookings().items()):
            self.booking_card(id, booking).grid(row=current_row, column=0, pady=10, sticky="ew")

    def build_actions(self, parent, id, booking):
        if booking.getStatus() != "Rejected" and booking.getStatus() != "Cancelled":
            self.main_window.make_button(parent, "Cancel", "danger", command=lambda: self.cancel_booking(id)).pack()

    def book_fac_card(self, facility, button_on, parent=None):
        card = self.main_window.make_card(parent or self.content_frame)
        fac_image = self.load_image(facility.image)
        self.images.append(fac_image)
        image_label = Label(card, image=fac_image, bg=self.main_window.card_color, bd=0)
        fac_name_label = Label(card, text=facility.name, font=self.main_window.title_font, bg=self.main_window.card_color, fg=self.main_window.text_color, wraplength=self.main_window.card_image_size)
        hours = facility.getOpeningHours()
        info_label = Label(card, text=f"{hours[0]:02d}:00 - {hours[1]:02d}:00 | ฿{facility.getHourlyRate():.2f}/hr", font=self.main_window.small_font, bg=self.main_window.card_color, fg=self.main_window.muted_color)

        image_label.grid(row=0, column=0)
        fac_name_label.grid(row=1, column=0, pady=(12, 2))
        info_label.grid(row=2, column=0)
        if button_on:
            self.main_window.make_button(card, "Book", "primary", command=lambda: self.show_fac_booking(facility)).grid(row=3, column=0, sticky="ew", pady=(12, 0))
        return card

    def show_fac_booking(self, facility):
        self.clear_view(False)
        self.booking_facility = facility
        self.slot_buttons = dict()
        self.slot_hours = list()
        self.selected_slots = list()

        left = Frame(self.content_frame, bg=self.main_window.content_color)
        right = Frame(self.content_frame, bg=self.main_window.content_color)
        left.grid(row=0, column=0, padx=(0, 30), sticky="n")
        right.grid(row=0, column=1, sticky="n")
        self.book_fac_card(facility, False, left).grid(row=0, column=0)
        self.main_window.make_button(left, "Back to facilities", "neutral", command=self.show_booking).grid(row=1, column=0, sticky="ew", pady=(15, 0))

        date_row = Frame(right, bg=self.main_window.content_color)
        date_row.grid(row=0, column=0, sticky="w", pady=(0, 10))
        date_label = Label(date_row, text="Date", font=self.main_window.subheader_font, bg=self.main_window.content_color, fg=self.main_window.text_color)
        date_label.grid(row=0, column=0, padx=(0, 12))
        self.date_selection = DateEntry(date_row, width=12, bg=self.main_window.accept_color, foreground="white", borderwidth=1, mindate=datetime.date.today(), font=("Bahnschrift", 13))
        self.date_selection.grid(row=0, column=1)
        self.current_date = self.date_selection.get_date()
        self.date_selection.bind("<<DateEntrySelected>>", lambda e: self.on_date_change(facility))
        self.date_selection.bind("<FocusOut>", lambda e: self.on_date_change(facility))

        legend = Frame(right, bg=self.main_window.content_color)
        legend.grid(row=1, column=0, sticky="w", pady=(0, 10))
        for column, (color, text) in enumerate([(self.main_window.accept_color, "Available"), (self.main_window.selected_color, "Selected"), (self.main_window.reject_color, "Booked")]):
            Frame(legend, width=16, height=16, bg=color).grid(row=0, column=column * 2, padx=(0, 6))
            Label(legend, text=text, font=self.main_window.small_font, bg=self.main_window.content_color, fg=self.main_window.muted_color).grid(row=0, column=column * 2 + 1, padx=(0, 20))

        slots_frame = Frame(right, bg=self.main_window.content_color)
        slots_frame.grid(row=2, column=0, sticky="w")

        start = int(facility.getOpeningHours()[0])
        end = int(facility.getOpeningHours()[1])
        if start == end:
            timeslot_per_day = 24
            current_hour = 0
        elif end == 0:
            timeslot_per_day = 24 - start
            current_hour = start
        elif start > end:
            timeslot_per_day = end + (24 - start)
            current_hour = 0
        else:
            timeslot_per_day = end - start
            current_hour = start

        for i in range(timeslot_per_day):
            next_hour = (current_hour + 1) % 24
            self.slot_hours.append((current_hour, next_hour))
            current_row, current_column = divmod(i, 4)
            timeslot_button = Button(slots_frame, text=f"{current_hour:02d}:00 - {next_hour:02d}:00",
                                     width=13, font=self.main_window.button_font, relief=FLAT, bd=0, padx=6, pady=6,
                                     command=lambda index=i: self.on_slot_click(index, facility))
            timeslot_button.grid(row=current_row, column=current_column, padx=5, pady=5)
            self.slot_buttons.update({i: timeslot_button})
            if next_hour == end and start > end:
                current_hour = start
            else:
                current_hour = next_hour

        self.summary_card(right, facility).grid(row=3, column=0, sticky="ew", pady=(20, 0))
        self.refresh_slots(facility)
        self.update_summary(facility)

    def refresh_slots(self, facility):
        for i, (start_hour, end_hour) in enumerate(self.slot_hours):
            if self.main_window.current_account.checkAvailability(facility, (self.date_selection.get_date(), [start_hour, end_hour])):
                self.set_slot_state(i, "free")
            else:
                self.set_slot_state(i, "taken")

    def summary_card(self, parent, facility):
        summary_frame = self.main_window.make_card(parent, padx=25, pady=18)
        summary_frame.columnconfigure(0, weight=1)
        self.sum_facility = Label(summary_frame, text=f"Facility: {facility.name}", font=self.main_window.subheader_font, bg=self.main_window.card_color, fg=self.main_window.text_color)
        self.sum_date = Label(summary_frame, text="Booking Date: -", font=self.main_window.subheader_font, bg=self.main_window.card_color, fg=self.main_window.text_color)
        self.sum_time = Label(summary_frame, text="Booking Time: -", font=self.main_window.subheader_font, bg=self.main_window.card_color, fg=self.main_window.text_color)
        self.sum_fee = Label(summary_frame, text="Total Fee: -", font=self.main_window.title_font, bg=self.main_window.card_color, fg=self.main_window.text_color)
        self.book_button = self.main_window.make_button(summary_frame, "Confirm Booking", "primary", padx=22, pady=8, command=lambda: self.submit_booking(facility))
        
        self.sum_facility.grid(row=0, column=0, sticky="w", pady=2)
        self.sum_date.grid(row=1, column=0, sticky="w", pady=2)
        self.sum_time.grid(row=2, column=0, sticky="w", pady=2)
        self.sum_fee.grid(row=3, column=0, sticky="w", pady=(6, 0))
        self.book_button.grid(row=0, column=1, rowspan=4, sticky="se", padx=(40, 0))
        return summary_frame

    def set_slot_state(self, index, state):
        button = self.slot_buttons[index]
        if state == "taken":
            button.config(bg=self.main_window.reject_color, fg="white", activebackground=self.main_window.reject_color,
                          disabledforeground="white", highlightthickness=0, state=DISABLED, cursor="arrow")
        elif state == "selected":
            button.config(bg=self.main_window.selected_color, fg="black", activebackground=self.main_window.selected_color,
                          highlightthickness=2, highlightbackground="black", state=NORMAL, cursor="hand2")
        else:
            button.config(bg=self.main_window.accept_color, fg="white", activebackground=self.main_window.accept_hover,
                          highlightthickness=0, state=NORMAL, cursor="hand2")

    def on_slot_click(self, index, facility):
        old = list(self.selected_slots)
        sel = list(old)
        if not sel:
            sel = [index]
        elif index in sel:
            if index == sel[0] and len(sel) > 1:
                sel.pop(0)
            elif index == sel[-1] and len(sel) > 1:
                sel.pop()
            elif len(sel) == 1:
                sel = []
            else:
                sel = [index]
        elif index == sel[0] - 1:
            sel.insert(0, index)
        elif index == sel[-1] + 1:
            sel.append(index)
        else:
            sel = [index]

        for i in old:
            self.set_slot_state(i, "free")
        for i in sel:
            self.set_slot_state(i, "selected")
        self.selected_slots = sel
        self.update_summary(facility)

    def on_date_change(self, facility):
        try:
            new_date = self.date_selection.get_date()
        except (ValueError, TclError):
            return
        if new_date == self.current_date:
            return
        self.current_date = new_date
        self.selected_slots = []
        self.refresh_slots(facility)
        self.update_summary(facility)

    def update_summary(self, facility):
        self.sum_date.config(text=f"Booking Date: {self.date_selection.get_date()}")
        if self.selected_slots:
            start_hour = self.slot_hours[self.selected_slots[0]][0]
            end_hour = self.slot_hours[self.selected_slots[-1]][1]
            self.sum_time.config(text=f"Booking Time: {start_hour:02d}:00 - {end_hour:02d}:00")
            self.sum_fee.config(text=f"Total Fee: ฿{self.main_window.current_account.calculateFee(facility, (self.date_selection.get_date(), [start_hour, end_hour])):.2f}")
        else:
            self.sum_time.config(text="Booking Time: -")
            self.sum_fee.config(text=f"Total Fee: -")

    def submit_booking(self, facility):
        if self.selected_slots:
            start_hour = self.slot_hours[self.selected_slots[0]][0]
            end_hour = self.slot_hours[self.selected_slots[-1]][1]
            self.main_window.current_account.book(facility, (self.date_selection.get_date(), [start_hour, end_hour]))
            self.open_tab(self.show_booking)
            messagebox.showinfo("Booking successful", "Your booking is submitted.")
        else:
            messagebox.showerror("Booking failed", "Please select the time.")

    def cancel_booking(self, id):
        self.main_window.current_account.cancelBooking(id)
        self.refresh()

class AdminMode(ModePage):
    def __init__(self, main_window):
        self.tabs = [("All Request", self.show_all_req), ("Pending Request", self.show_pending_req), ("Facilities", self.show_facilities), ("Add Facility", self.show_add_fac)]
        self.default_tab = "show_all_req"
        self.input_img_path = str()
        super().__init__(main_window, "Admin")

    def show_requests(self, requests, empty_text):
        self.clear_view()
        if not requests:
            self.empty_state(empty_text)
            return
        self.content_frame.columnconfigure(0, minsize=700)
        for current_row, (id, request) in enumerate(requests.items()):
            self.booking_card(id, request).grid(row=current_row, column=0, pady=10, sticky="ew")

    def show_all_req(self, *args):
        self.show_requests(self.main_window.current_account.getBookings(), "No booking requests yet.")

    def show_pending_req(self, *args):
        self.show_requests(self.main_window.current_account.getPending(), "No pending requests.")

    def show_facilities(self, *args):
        self.clear_view()
        if not self.main_window.current_account.facilities:
            self.empty_state("No facilities yet. Add one from the Add Facility tab.")
            return
        self.content_frame.columnconfigure(0, minsize=700)
        for current_row, facility in enumerate(self.main_window.current_account.facilities):
            self.facility_card(facility).grid(row=current_row, column=0, pady=10, sticky="ew")

    def show_add_fac(self, *args):
        self.clear_view(False)
        input_fac_name = StringVar()
        self.input_img_path = str()
        self.img_name = StringVar(value="No file selected")
        input_abbrev = StringVar()
        input_descrip = StringVar()
        input_hourly_rate = DoubleVar()

        card = self.main_window.make_card(self.content_frame, padx=40, pady=30)
        card.grid(row=0, column=0)
        add_fac_label = Label(card, text="Add Facility", font=self.main_window.header_font, bg=self.main_window.card_color, fg=self.main_window.text_color)
        add_fac_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        def custom_label(text, row):
            Label(card, text=text, bg=self.main_window.card_color, fg=self.main_window.muted_color).grid(row=row, column=0, sticky="w", padx=(0, 25), pady=8)

        custom_label("Facility Name", 1)
        self.main_window.make_entry(card, input_fac_name, width=30).grid(row=1, column=1, columnspan=2, sticky="ew", pady=8, ipady=4)
        custom_label("Image", 2)
        self.main_window.make_button(card, "Select file", "neutral", command=self.select_file, padx=12, pady=3).grid(row=2, column=1, sticky="w", pady=8)
        img_label = Label(card, textvariable=self.img_name, font=self.main_window.small_font, bg=self.main_window.card_color, fg=self.main_window.muted_color)
        img_label.grid(row=2, column=2, sticky="w", padx=(10, 0))
        custom_label("Abbreviation", 3)
        self.main_window.make_entry(card, input_abbrev, width=30).grid(row=3, column=1, columnspan=2, sticky="ew", pady=8, ipady=4)
        custom_label("Description", 4)
        self.main_window.make_entry(card, input_descrip, width=30).grid(row=4, column=1, columnspan=2, sticky="ew", pady=8, ipady=4)
        custom_label("Opening Hours (Start - End)", 5)
        hours_frame = Frame(card, bg=self.main_window.card_color)
        hours_frame.grid(row=5, column=1, columnspan=2, sticky="w", pady=8)
        start_open = Spinbox(hours_frame, from_=0, to=23, wrap=True, format="%02.0f", state="readonly", bg="white", width=5, relief=FLAT, readonlybackground="white", highlightthickness=1, highlightbackground=self.main_window.border_color, font=("Bahnschrift", 13))
        end_time = Spinbox(hours_frame, from_=0, to=23, wrap=True, format="%02.0f", state="readonly", bg="white", width=5, relief=FLAT, readonlybackground="white", highlightthickness=1, highlightbackground=self.main_window.border_color, font=("Bahnschrift", 13))
        start_open.grid(row=0, column=0)
        to_label = Label(hours_frame, text="to", bg=self.main_window.card_color, fg=self.main_window.muted_color)
        to_label.grid(row=0, column=1, padx=10)
        end_time.grid(row=0, column=2)
        custom_label("Hourly Rate (฿)", 6)
        self.main_window.make_entry(card, input_hourly_rate, width=30).grid(row=6, column=1, columnspan=2, sticky="ew", pady=8, ipady=4)
        self.main_window.make_button(card, "Submit", "primary", command=lambda: self.add_fac(input_fac_name, self.input_img_path, input_abbrev, input_descrip, [int(start_open.get()), int(end_time.get())], input_hourly_rate)).grid(row=7, column=0, columnspan=3, sticky="ew", pady=(25, 0))

    def build_actions(self, parent, id, booking):
        if booking.getStatus() == "Pending":
            self.main_window.make_button(parent, "Accept", "primary", command=lambda: self.accept_booking(id)).pack(side=LEFT, padx=(0, 8))
            self.main_window.make_button(parent, "Reject", "danger", command=lambda: self.reject_booking(id)).pack(side=LEFT)
        elif booking.getStatus() == "Approved":
            self.main_window.make_button(parent, "Cancel", "danger", command=lambda: self.cancel_booking(id)).pack()

    def facility_card(self, facility):
        card = self.main_window.make_card(self.content_frame)
        fac_image = self.load_image(facility.image)
        self.images.append(fac_image)
        image_label = Label(card, image=fac_image, bg=self.main_window.card_color, bd=0)
        fac_name_label = Label(card, text=facility.name, font=self.main_window.title_font, bg=self.main_window.card_color, fg=self.main_window.text_color)
        descrip_label = Label(card, text=facility.description, bg=self.main_window.card_color, fg=self.main_window.muted_color, wraplength=420, justify=LEFT)
        opening_label = Label(card, text=f"Opening Hours: {int(facility.getOpeningHours()[0]):02d}:00 - {int(facility.getOpeningHours()[1]):02d}:00", bg=self.main_window.card_color, fg=self.main_window.text_color)
        fee_label = Label(card, text=f"Hourly Rate: ฿{facility.getHourlyRate():.2f}", bg=self.main_window.card_color, fg=self.main_window.text_color)

        card.columnconfigure(1, weight=1)
        image_label.grid(row=0, column=0, rowspan=4, padx=(0, 25))
        fac_name_label.grid(row=0, column=1, sticky="w")
        descrip_label.grid(row=1, column=1, sticky="w", pady=(4, 8))
        opening_label.grid(row=2, column=1, sticky="w", pady=2)
        fee_label.grid(row=3, column=1, sticky="w", pady=2)
        return card

    def accept_booking(self, booking_id):
        self.main_window.current_account.approve(booking_id)
        overlap_bookings = [id for id, booking in self.main_window.booking_data.items() if not self.main_window.current_account.checkAvailability(booking.site, booking.getTimeSlot()) and booking.getStatus() == "Pending"]
        for id in overlap_bookings:
            self.main_window.current_account.reject(id)
        self.refresh()

    def reject_booking(self, booking_id):
        self.main_window.current_account.reject(booking_id)
        self.refresh()

    def cancel_booking(self, booking_id):
        self.main_window.current_account.cancel(booking_id)
        self.refresh()

    def select_file(self):
        path = filedialog.askopenfilename(title="Select the file", filetypes=(("Image files", "*.png *.jpg *.jpeg"),))
        if path:
            self.input_img_path = path
            self.img_name.set(os.path.basename(path))

    def add_fac(self, name, image, abbrev, description, opening_hours, hourly_rate):
        try:
            rate = hourly_rate.get()
        except TclError:
            messagebox.showerror("Adding failed", "Hourly rate must be a number.")
            return
        if not name.get().strip() or not image or not abbrev.get().strip() or not description.get().strip() or len(opening_hours) != 2 or rate < 0:
            messagebox.showerror("Adding failed", "Please fill in correctly.")
        else:
            self.main_window.current_account.addFacilities(name.get(), image, abbrev.get(), description.get(), opening_hours, rate)
            messagebox.showinfo("Adding successful", "The new facility has been added.")

def main():
    BookMyPlay()

if __name__ == "__main__":
    main()