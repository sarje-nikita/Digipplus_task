import pandas as pd


def save_businesses(business_list, excel_filename="business_data.xlsx"):
    for i in business_list:
        print(i)
    columns = ["Name", "State", "City", "Main Business", "Sub Business", "Hash ID", "Address", "Website",
               "Phone Number", "Reviews Average", "Reviews Count", "Map"]
    data = []

    for business in business_list:
        data.append([business.name, business.state, business.city, business.main_business, business.sub_business,
                     business.hash_value, business.address, business.website, business.phone_number,
                     business.reviews_average, business.reviews_count, business.map])

    df = pd.DataFrame(data, columns=columns)

    # Try to read the existing Excel file, if it exists
    try:
        existing_df = pd.read_excel(excel_filename)
        df = pd.concat([existing_df, df], ignore_index=True)
    except FileNotFoundError:
        pass

    # Save DataFrame to Excel file
    df.to_excel(excel_filename, index=False)
    print(f"Data saved to {excel_filename}")
