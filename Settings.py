# List of columns we want in our dataset
column_list=['Department Name', 'Supplier Code',
            'Supplier Name',
            'Item Name', 'Item Description',
            'Quantity', 'Unit Price', 'Total Price']

# List of pricing columns to perform data manipulation
pricing_columns=['Unit Price', 'Total Price']

# List of keywords to help identify services
services_keywords_list=['Services', 'services', 'Clubs',
                    'Amendment', 'amendment',
                    'Agreement', 'agreement']

# List of keywords to help identify stop_words
vendor_stopwords=['biz', 'bv', 'co', 'comp', 'company', 
                'corp','corporation', 'dba', 
                'inc', 'incorp', 'incorporat', 
                'incorporate', 'incorporated', 'incorporation', 
                'international', 'intl', 'intnl', 
                'limited' ,'llc', 'ltd', 'llp', 
                'machines', 'pvt', 'pte', 'private', 'unknown']

# List of columns to use when aggregating spend by vendor
vendor=['Supplier Code', 'Supplier Name']

# List of columns to use when aggregating spend by category
category=['Segment Name', 'Segment Code']
