import csv
import os

# Directory where your CSV files are stored
csv_directory = r"E:\Swiggy"

# Function to generate a table name based on the file name
def generate_table_name(file_name):
    # Remove the "zomato-schema" part and split by hyphen
    parts = file_name.replace("zomato-schema", "").split("-")
    # Join everything after the second hyphen and remove spaces
    if len(parts) > 2:
        table_name = "".join(parts[2:]).replace(" ", "")
    else:
        table_name = "".join(parts).replace(" ", "")
    return table_name

# Loop over each CSV file in the directory
for csv_file in os.listdir(csv_directory):
    if csv_file.endswith(".csv"):
        # Generate the table name from the file name
        table_name = f"`{generate_table_name(os.path.splitext(csv_file)[0])}`"
        
        # Open the CSV file
        with open(os.path.join(csv_directory, csv_file), 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            headers = next(reader)  # Get column headers
            
            # Start writing the SQL statements
            sql_statements = []
            create_table_sql = f"CREATE TABLE {table_name} (\n"
            create_table_sql += ",\n".join([f"  `{header}` TEXT" for header in headers])  # Enclose column names in backticks
            create_table_sql += "\n);\n"
            sql_statements.append(create_table_sql)
            
            for row in reader:
                # Skip empty rows
                if not any(row):
                    continue
                
                # Escape single quotes in data
                values = ', '.join([f"'{value.replace('\'', '\'\'')}'" for value in row])
                insert_sql = f"INSERT INTO {table_name} ({', '.join([f'`{header}`' for header in headers])}) VALUES ({values});"
                sql_statements.append(insert_sql)
        
        # Write SQL statements to a file
        with open(os.path.join(csv_directory, f"{table_name.strip('`')}.sql"), 'w', encoding='utf-8') as sql_file:
            sql_file.write('\n'.join(sql_statements))

print("SQL files created successfully.")
