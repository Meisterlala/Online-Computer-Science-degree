import re

pattern_s = r"(?<=<!--- LOC_START --->\n).*(?=<!--- LOC_END --->)"
pattern = re.compile(pattern_s, re.M|re.S)

# Read table data
table = open(".github/loc_table.html", "r")
table_data = table.read()
table.close()

# Read Readme
readme = open("README.md", "r+")
readme_data = readme.read()

# Update Readme
readme_new = re.sub(pattern, table_data, readme_data)

# Write Readme
readme.seek(0)
readme.write(readme_new)
readme.flush()
readme.close()
