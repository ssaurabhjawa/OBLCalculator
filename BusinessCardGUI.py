import tkinter as tk
from tkinter import ttk
import math
import os

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

# Create the main window
root = tk.Tk()
root.title("Business Card Cost Calculator")

# Create a frame to hold the grid of labels
grid_frame = tk.Frame(root, borderwidth=2, relief="groove")
grid_frame.grid(row=0, column=0, rowspan=10, columnspan=4)

# Configure rows and columns with grid_columnconfigure and grid_rowconfigure
for i in range(10):
    grid_frame.grid_rowconfigure(i, weight=1, minsize=50)
for j in range(4):
    grid_frame.grid_columnconfigure(j, weight=1, minsize=50)

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

foiling_var = tk.BooleanVar()
foiling_Checkbox = tk.Checkbutton(root, text="Foiling", variable=foiling_var)
foiling_Checkbox.grid(row=5, column=1, padx=10, pady=10, sticky="w")

lamination_var = tk.BooleanVar()
lamination_Checkbox = tk.Checkbutton(root, text="Lamination", variable=lamination_var)
lamination_Checkbox.grid(row=6, column=1, padx=10, pady=10, sticky="w")

spot_uv_var = tk.BooleanVar()
spot_uv_checkbox = tk.Checkbutton(root, text="Spot UV", variable=spot_uv_var)
spot_uv_checkbox.grid(row=7, column=1, padx=10, pady=10, sticky="w")

# Create a label for the total cost
cost_label_window = ttk.Label(root, text="Total Cost: 0.00 AED")
cost_label_window.grid(row=9, column=1, padx=10, pady=10)


# Define a function to update the GSM combobox when the paper combobox is changed
def update_gsm_options(*args):
    selected_paper = paper_combobox.get()
    available_gsm_options = [card["GSM"] for card in business_cards if card["Paper"] == selected_paper]
    gsm_combobox.config(values=available_gsm_options)

# Bind the update_gsm_options function to the paper combobox
paper_combobox.bind("<<ComboboxSelected>>", update_gsm_options)

def populate_comboboxes():
    # Get unique paper and GSM values from the business_cards dictionary
    papers = set(card["Paper"] for card in business_cards)
    gsms = set(card["GSM"] for card in business_cards)

    # Set the values in the Comboboxes
    paper_combobox['values'] = list(papers)
    paper_combobox.current(0)

    # Define a function to update the GSM combobox when the paper combobox is changed
    def update_gsm_options(*args):
        selected_paper = paper_combobox.get()
        available_gsm_options = [card["GSM"] for card in business_cards if card["Paper"] == selected_paper]
        gsm_combobox.config(values=available_gsm_options)
        gsm_combobox.current(0)

    # Bind the update_gsm_options function to the paper combobox
    paper_combobox.bind("<<ComboboxSelected>>", update_gsm_options)

    # Set the initial values of the GSM combobox based on the selected paper type
    initial_paper = paper_combobox.get()
    initial_gsms = [card["GSM"] for card in business_cards if card["Paper"] == initial_paper]
    gsm_combobox['values'] = initial_gsms
    gsm_combobox.current(0)

 
def calculate_sheet_quantity():
    quantity = int(quantity_entry.get())
    sheet_quantity = math.ceil(quantity / 21)
    return sheet_quantity


def calculate_price_per_sheet(paper, gsm):
    price_per_sheet = None
    for card in business_cards:
        if card["Paper"] == paper and card["GSM"] == gsm:
            price_per_sheet = card["dhs/sheet"]
            break
    return price_per_sheet



def calculate_cost(paper, gsm, color_option, side_option, lamination_checked, spot_uv_checked, foiling_checked):
    # Find the price per sheet based on the user's selections
    price_per_sheet = calculate_price_per_sheet(paper, gsm)
    quantity = calculate_sheet_quantity()

    # Calculate the cost of printing based on the user's color and side options
    printing_cost_basic = quantity * price_per_sheet * printing_options[color_option][side_option]
    cutting_Packing = 20

    # Calculate the cost of lamination, spot UV, and foiling if their corresponding checkboxes are checked
    lamination_cost = 0
    spot_uv_cost = 0
    foiling_cost = 0
    if lamination_checked:
        lamination_cost = quantity * lamination_options[color_option][side_option]
    if spot_uv_checked:
        spot_uv_cost = quantity * spot_uv_options[side_option]
    if foiling_checked:
        foiling_cost = quantity * foiling_options[side_option]

    # Calculate the total cost
    printing_cost = printing_cost_basic + lamination_cost + spot_uv_cost + foiling_cost + cutting_Packing
    total_cost = 2 * printing_cost

    # Print the variables to help catch any errors in the addition logic
    print(f"price_per_sheet: {price_per_sheet}")
    print(f"quantity: {quantity}")
    print(f"printing_cost_basic: {printing_cost_basic}")
    print(f"cutting_Packing: {cutting_Packing}")
    print(f"lamination_cost: {lamination_cost}")
    print(f"spot_uv_cost: {spot_uv_cost}")
    print(f"foiling_cost: {foiling_cost}")
    print(f"printing_cost: {printing_cost}")
    print(f"total_cost: {total_cost}")

    return total_cost

populate_comboboxes()

def calculate_cost_from_selections(paper_combobox, gsm_combobox, color_listbox, side_combobox, lamination_var, spot_uv_var, foiling_var):
    # Get the user's selections from the GUI widgets
    paper = paper_combobox.get()
    gsm = int(gsm_combobox.get())
    color_option = color_listbox.get(color_listbox.curselection())
    side_option = side_combobox.get()

    # Calculate the cost based on the user's selections
    cost = calculate_cost(paper, gsm, color_option, side_option, lamination_var.get(), spot_uv_var.get(), foiling_var.get())
    print(cost)
    # Create the description for the invoice
    description = f"Product: Business Cards\nPaper: {paper}\nGSM: {gsm}\nColor: {color_option}\nSides: {side_option}\nLamination: {lamination_var.get()}\nSpot UV: {spot_uv_var.get()}\nFoiling: {foiling_var.get()}"

    # Create the dictionary with description and total cost
    invoice = {
        'description': description,
        'total_cost': cost
    }

    # Write the invoice information to a file
    filename = 'invoice.txt'
    with open(filename, 'w') as f:
        f.write(f"Invoice:\n{invoice['description']}\nTotal Cost: {invoice['total_cost']}\n\n")

    # Auto-download the text file
    os.system(f'start {filename}')


def create_summary(paper_combobox, gsm_combobox, quantity_entry, color_listbox, side_combobox, lamination_var, spot_uv_var, foiling_var):
    # Get the user's selections from the GUI widgets
    paper = paper_combobox.get()
    gsm = int(gsm_combobox.get())
    quantity = calculate_sheet_quantity()
    color_option = color_listbox.get(color_listbox.curselection())
    side_option = side_combobox.get()

    price_per_sheet = calculate_price_per_sheet(paper, gsm)

    # Calculate the cost of printing based on the user's color and side options
    printing_cost = quantity * price_per_sheet * printing_options[color_option][side_option]
    cutting_packing_cost = 20

    # Calculate the cost of lamination, spot UV, and foiling if their corresponding checkboxes are checked
    lamination_cost = quantity * lamination_options[color_option][side_option] if lamination_var.get() else 0
    spot_uv_cost = quantity * spot_uv_options[side_option] if spot_uv_var.get() else 0
    foiling_cost = quantity* foiling_options[side_option] if foiling_var.get() else 0

    printing_cost_with_all_option = printing_cost + lamination_cost + spot_uv_cost + foiling_cost + cutting_packing_cost

    # Calculate the total cost
    total_cost = 2 * printing_cost_with_all_option

    # Create a summary of the variables and their values
    summary = f"Summary:\n"
    summary += f"Paper: {paper}\n"
    summary += f"GSM: {gsm}\n"
    summary += f"Quantity: {quantity}\n"
    summary += f"Color Option: {color_option}\n"
    summary += f"Side Option: {side_option}\n"
    summary += f"Printing Cost: {printing_cost:.2f} AED\n"
    if lamination_var.get():
        summary += f"Lamination Cost: {quantity} * {lamination_options[color_option][side_option]} = {lamination_cost:.2f} AED\n"
    if spot_uv_var.get():
        summary += f"Spot UV Cost: {quantity} * {spot_uv_options[side_option]} = {spot_uv_cost:.2f} AED\n"
    if foiling_var.get():
        summary += f"Foiling Cost: {quantity} * {foiling_options[side_option]} = {foiling_cost:.2f} AED\n"
    summary += f"Cutting and Packing Cost: {cutting_packing_cost:.2f} AED\n"
    summary += f"Printing Cost with all option: {printing_cost_with_all_option:.2f} AED\n"
    summary += f"Total Cost: {total_cost:.2f} AED\n"

    # Update the cost label window with the total cost
    cost_label_window.config(text=f"Total Cost: {total_cost:.2f} AED")

    # Create a text file with the summary information
    filename = "business_card_summary.txt"
    with open(filename, "w") as f:
        f.write(summary)

    # Auto-download the text file
    os.system(f'start {filename}')

# Create the "Summary Cost" button
calculate_button = ttk.Button(root, text="Summary Cost", command=lambda: create_summary(
    paper_combobox,
    gsm_combobox,
    quantity_entry,
    color_listbox,
    side_combobox,
    lamination_var,
    spot_uv_var,
    foiling_var
))
calculate_button.grid(row=9, column=0,padx=10, pady=10)

# Create the "Calculate Cost" button
calculate_button = ttk.Button(root, text="Create Description & Total Cost", command=lambda: calculate_cost_from_selections(
    paper_combobox,
    gsm_combobox,
    color_listbox,
    side_combobox,
    lamination_var,
    spot_uv_var,
    foiling_var
))
calculate_button.grid(row=9, column=2, padx=10, pady=10)
 


# Start the Tkinter event loop
root.mainloop()


