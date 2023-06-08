import tkinter as tk
from tkinter import ttk
# Business cards data
business_cards = [
    {"Paper": "Art Matt", "GSM": 300, "dhs/sheet": 0.37},
    {"Paper": "Art Matt", "GSM": 350, "dhs/sheet": 0.4},
    {"Paper": "Linen", "GSM": 350, "dhs/sheet": 0.75},
    {"Paper": "Sona", "GSM": 300, "dhs/sheet": 0.8},
    {"Paper": "Sona", "GSM": 350, "dhs/sheet": 0.9}
]

printing_options = {
    "Colored": {
        "Double Side Per Sheet": 0.4,
        "Single Side Per Sheet": 0.2
    },
    "Black & White": {
        "Double Side Per Sheet": 0.2,
        "Single Side Per Sheet": 0.1
    }
}

lamination_options = {
    "Colored": {
        "Double Side Per Sheet": 0.4,
        "Single Side Per Sheet": 0.2
    },
    "Black & White": {
        "Double Side Per Sheet": 0.2,
        "Single Side Per Sheet": 0.1
    }
}

spot_uv_options = {
    "Double Side Per Sheet": 15.625,
    "Single Side Per Sheet": 15.625
}

foiling_options = {
    "Double Side Per Sheet": 21,
    "Single Side Per Sheet": 21
}


def calculate_cost_from_selections(paper_combobox, gsm_combobox, quantity_entry, color_listbox, side_combobox, cost_label):
    # Get the selected options from the widgets
    paper = paper_combobox.get()
    gsm = gsm_combobox.get()
    quantity = int(quantity_entry.get())
    color_option = color_listbox.get(tk.ACTIVE)
    side_option = side_combobox.get()

    # Calculate the cost based on the selected options
    cost = calculate_cost(paper, gsm, quantity, color_option, side_option)

    # Update the cost label with the calculated cost
    cost_label.config(text=f"Total Cost: {cost:.2f} AED")

# Create the main window
root = tk.Tk()
root.title("Business Card Cost Calculator")

# Create a Combobox for paper selection
paper_label = ttk.Label(root, text="Paper:")
paper_label.grid(row=0, column=0, padx=10, pady=5)

paper_combobox = ttk.Combobox(root)
paper_combobox.grid(row=0, column=1, padx=10, pady=5)

# Create a Combobox for GSM selection
gsm_label = ttk.Label(root, text="GSM:")
gsm_label.grid(row=1, column=0, padx=10, pady=5)

gsm_combobox = ttk.Combobox(root)
gsm_combobox.grid(row=1, column=1, padx=10, pady=5)

# Create an Entry for quantity input
quantity_label = ttk.Label(root, text="Quantity:")
quantity_label.grid(row=2, column=0, padx=10, pady=5)

quantity_entry = ttk.Entry(root)
quantity_entry.grid(row=2, column=1, padx=10, pady=5)

# Create a label for the color option
color_label = tk.Label(root, text="Color Option:")
color_label.grid(row=3, column=0, padx=10, pady=10)

# Create a listbox for the color option
color_listbox = tk.Listbox(root, height=5, width=20)
color_listbox.grid(row=3, column=1, padx=10, pady=10)

for color_option in printing_options.keys():
    color_listbox.insert(tk.END, color_option)

# Create a label for the side option
side_label = tk.Label(root, text="Side Option:")
side_label.grid(row=4, column=0, padx=10, pady=10)

# Create a Combobox for the side option
side_combobox = ttk.Combobox(root)
side_combobox.grid(row=4, column=1, padx=10, pady=10)

# Insert the values into the Combobox
side_combobox['values'] = ["Double Side Per Sheet", "Single Side Per Sheet"]
side_combobox.current(0)

foiling_Checkbox = tk.BooleanVar()
checkbox = tk.Checkbutton(root, text="Foiling", variable=foiling_Checkbox)
checkbox.grid(row=8, column=0, padx=10, pady=10)



# Create a label for the total cost
cost_label = ttk.Label(root, text="Total Cost: 0.00 AED")
cost_label.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

def populate_comboboxes():
    # Get unique paper and GSM values from the business_cards dictionary
    papers = set(card["Paper"] for card in business_cards)
    gsms = set(card["GSM"] for card in business_cards)

    # Set the values in the Comboboxes
    paper_combobox['values'] = list(papers)
    gsm_combobox['values'] = list(gsms)

    paper_combobox.current(0)
    gsm_combobox.current(0)


def calculate_sheet_quantity(quantity_entry):
    quantity = int(quantity_entry.get())
    sheet_quantity = quantity / 21
    return sheet_quantity


def calculate_price_per_sheet(paper, gsm):
    price_per_sheet = None
    for card in business_cards:
        if card["Paper"] == paper and card["GSM"] == gsm:
            price_per_sheet = card["dhs/sheet"]
            break
    return price_per_sheet


def calculate_cost(paper, gsm, quantity, color_option, side_option):
    # Find the price per sheet based on the user's selections
    price_per_sheet = calculate_price_per_sheet(paper, gsm)


    # Calculate the cost of printing based on the user's color and side options
    printing_cost = quantity * price_per_sheet * printing_options[color_option][side_option]
    lamination_cost = quantity * lamination_options[color_option][side_option]
    spot_uv_cost = quantity * spot_uv_options[side_option]
    foiling_cost = foiling_options[side_option]
    cutting_Packing = 20

    # Calculate the total cost
    total_cost = printing_cost + lamination_cost + spot_uv_cost + foiling_cost + cutting_Packing

    return total_cost

# Populate the Comboboxes with data
populate_comboboxes()


def calculate_cost_from_selections(paper_combobox, gsm_combobox, quantity_entry, color_listbox, side_combobox, cost_label):
    # Get the user's selections from the GUI widgets
    paper = paper_combobox.get()
    gsm = int(gsm_combobox.get())
    quantity = int(quantity_entry.get())
    color_option = color_listbox.get(color_listbox.curselection())
    side_option = side_combobox.get()

    # Calculate the cost based on the user's selections
    cost = calculate_cost(paper, gsm, quantity, color_option, side_option)
    # Update the cost label with the calculated cost
    cost_label.config(text=f"Total Cost: {cost:.2f} AED")

def create_summary(paper_combobox, gsm_combobox, quantity_entry, color_listbox, side_combobox):
    # Get the user's selections from the GUI widgets
    paper = paper_combobox.get()
    gsm = int(gsm_combobox.get())
    quantity = int(quantity_entry.get())
    color_option = color_listbox.get(color_listbox.curselection())
    side_option = side_combobox.get()

    # Create a summary of the variables and their values
    summary = f"Summary:\n"
    summary += f"Paper: {paper}\n"
    summary += f"GSM: {gsm}\n"
    summary += f"Quantity: {quantity}\n"
    summary += f"Color Option: {color_option}\n"
    summary += f"Side Option: {side_option}\n"
    summary += f"{calculate_cost(paper, gsm, quantity, color_option, side_option)}\n"


    print(summary)

# Create the "Calculate Cost" button
calculate_button = ttk.Button(root, text="Calculate Cost", command=lambda: calculate_cost_from_selections(
    paper_combobox,
    gsm_combobox,
    quantity_entry,
    color_listbox,
    side_combobox,
    cost_label
))
calculate_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)
 
# Create the "Calculate Cost" button
calculate_button = ttk.Button(root, text="Summary Cost", command=lambda: create_summary(
    paper_combobox,
    gsm_combobox,
    quantity_entry,
    color_listbox,
    side_combobox
))
calculate_button.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

# Start the Tkinter event loop
root.mainloop()


