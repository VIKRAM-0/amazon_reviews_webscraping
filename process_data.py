import pandas as pd

# Load the CSV file
df = pd.read_csv('reviews.csv')
df['Color'].fillna("", inplace=True)
df['Style Name'].fillna("", inplace=True)

# Function to split the 'Color' field into separate attributes
def split_color_field(row):
    color = ""
    size = ""
    product_name = ""
    
    # Split by the known delimiters
    parts = row['Color'].split("Pattern Name:")
    if len(parts) > 1:
        product_name = parts[1].strip()
    other_parts = parts[0].split("Size:")
    
    if len(other_parts) > 1:
        size = other_parts[1].strip()
    color_parts = other_parts[0].split("Colour:")
    
    if len(color_parts) > 1:
        color = color_parts[1].strip()
    
    return pd.Series([color, size, product_name])

# Apply the function to the DataFrame and create new columns
df[['product_color', 'product_size', 'product_name']] = df.apply(split_color_field, axis=1)

# Drop the original 'Color' and 'Style Name' columns if no longer needed
df = df.drop(columns=['Color', 'Style Name'])

# Save the updated DataFrame back to the same CSV file
df.to_csv('reviews.csv', index=False)

print("Transformed data saved back to reviews.csv")
