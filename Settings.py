# List of columns we want in our dataset
column_list=['Supplier Code', 'Supplier Name',
            'Item Name', 'Item Description',
            'Quantity', 'Unit Price', 'Total Price', 
            'Segment', 'Segment Title']

# List of pricing columns to perform data manipulation
pricing_columns=['Unit Price', 'Total Price']

# List of primary keys
primary_keys=['Supplier Code', 'Segment']

# List of keywords to help identify services
services_keywords_list=['amendment', 'agreement', 'bill', 'clubs', 'Clubs', 
                    'government', 'govt', 'license', 'maintenance', 'membership',
                    'rent', 'service', 'Services', 'services','utility', 'utilities']

# List of keywords to help identify stop_words
vendor_stopwords=['biz', 'bv', 'blank','co', 'comp', 'company', 
                'corp','corporation', 'confidential','dba', 
                'inc', 'incorp', 'incorporat', 
                'incorporate', 'incorporated', 'incorporation', 
                'international', 'intl', 'intnl', 
                'limited' ,'llc', 'ltd', 'llp', 
                'machines', 'pvt', 'pte', 'private', 'unknown']

# List of columns to use when aggregating spend by vendor
vendor=['Supplier Code', 'Supplier Name']

# List of columns to use when aggregating spend by category
category=['Segment Title']

# List of columns containing textual data
textual_data=['supplier_cleaned', 'item_desc', 'item_name']

# List of Target Labels and Label Codes (Generated via Spend Grouper Function. Need not change)
target=['Segment Title', 'Final_Category', 'Final_Code']

# List of columns for training model (Can change anything except 'Is_Service' & 'Final_Code')
train_columns=['Quantity', 'Unit Price', 'Total Price', 'Is_Service', 'Final_Code']

# List of target label for training model (Generated via Spend Grouper Function. Need not change)
train_target=['Final_Code']

# List of columns for test/unseen data
test_columns=['Quantity', 'Unit Price', 'Total Price', 'Is_Service']

# Max length for padding equences (Customize according to training needs)
max_length=15
