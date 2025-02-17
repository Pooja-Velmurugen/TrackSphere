import phonenumbers
from phonenumbers import carrier, geocoder, timezone
import customtkinter as ctk
from tkinter import messagebox

#set default theme
ctk.set_appearance_mode("Dark") 
ctk.set_default_color_theme("blue")
 
class AdvancedMobileTracker(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Number Tracker ")
        self.geometry("700x550")    
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        
        self.create_widgets()
        
    def create_widgets(self):
        
        #header frame section
        header_frame = ctk.CTkFrame(self, corner_radius=0)
        header_frame.grid(row=0, column=0, sticky="nsew")
        ctk.CTkLabel(header_frame,text="Number Tracker",font=("Arial", 24, "bold"),compound="left").pack(pady=15)
        self.theme_mode = ctk.StringVar(value="Dark")
        self.theme_switch=ctk.CTkSwitch(header_frame,text="Dark Mode", variable=self.theme_mode,onvalue="Dark", offvalue="Light",command=self.change_theme)
        self.theme_switch.pack(pady=15)
        
        #input frame section
        input_frame = ctk.CTkFrame(self)
        input_frame.grid(row=1, column=0, sticky="nsew",padx=20, pady=10 )
        ctk.CTkLabel(input_frame,text="Enter International Phone Number:",font=("Arial", 14)).pack(pady=5)
        self.entry = ctk.CTkEntry(input_frame,placeholder_text="+CountryCode PhoneNumber",width=300,font=("Arial", 14))
        self.entry.pack(pady=10)
        ctk.CTkButton(input_frame,text="Track Location",command=self.track_number,corner_radius=8,fg_color="#2AAA8A",hover_color="#207A60").pack(pady=10)
        

        #resule frame section
        self.results_frame = ctk.CTkFrame(self)
        self.results_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)             
        self.create_info_labels()
        
           
    def create_info_labels(self):
        info = [
            ("📱 Valid Number:", "valid", 0),
            ("🌍 Country:", "country", 1),
            ("🏢 Service Provider:", "carrier", 2),
            ("⏰ Time Zone:", "timezone", 3),
            ("📍 Region:", "region", 4),
            ("📡 Number Type:", "type", 5)
        ]
        
        for label_text, attr, row in info:

            label = ctk.CTkLabel(self.results_frame,text=label_text,font=("Arial", 12, "bold"))
            label.grid(row=row, column=0, padx=10, pady=5)
            value_label = ctk.CTkLabel(self.results_frame,text="",font=("Arial", 12))
            value_label.grid(row=row, column=1, padx=10, pady=5)

            #assigns a new attribute to an object(it can be any data type )
            setattr(self, f"{attr}_label", value_label) 


    def track_number(self):
        
        number = self.entry.get().strip()
        if not number:
            self.show_error("Input Error", "Please enter a phone number")
            return
            
        try:
            parsed_num = phonenumbers.parse(number, None)
        except Exception as e:
            self.show_error("Parse Error", f"Invalid format: {str(e)}")
            return
            
        if not phonenumbers.is_valid_number(parsed_num):
            self.show_error("Validation Error", "Invalid phone number")
            return
            
        self.valid_label.configure(text=str(phonenumbers.is_valid_number(parsed_num)))
        self.country_label.configure(text=geocoder.country_name_for_number(parsed_num, "en"))
        self.carrier_label.configure(text=carrier.name_for_number(parsed_num, "en"))
        self.timezone_label.configure(text=", ".join(timezone.time_zones_for_number(parsed_num)))
        self.region_label.configure(text=geocoder.description_for_number(parsed_num, "en"))
        self.type_label.configure(text=self.get_number_type(parsed_num))
        
        
    def get_number_type(self, number):
        type_map = { 0: "Fixed Line",1: "Mobile",2: "Fixed/Mobile",3: "Toll Free",4: "Premium Rate",5: "Shared Cost",6: "VOIP",7: "Personal Number",8: "Pager",9: "UAN",10: "Unknown"}
        return type_map.get(phonenumbers.number_type(number), "Unknown")
    
    def change_theme(self):
        theme = self.theme_mode.get()
        if theme in ["Dark", "Light"]:
            ctk.set_appearance_mode(theme)
            self.update_theme_text(theme)

    def update_theme_text(self, theme):
        if theme == "Dark":
            self.theme_switch.configure(text="Dark Mode")
        else:
            self.theme_switch.configure(text="Light Mode")            
    
    def show_error(self, title, message):
        messagebox.showerror(title, message)
    
app = AdvancedMobileTracker()
app.mainloop()