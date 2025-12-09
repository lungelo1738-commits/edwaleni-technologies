#!/usr/bin/env python3
"""
Lease Agreement Generator
Imports landlord_config and tenant_config to generate complete lease
"""

import sys
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta  # pip install python-dateutil

# Import configurations
try:
    from config_landlord import *
    from tenant_config import *
except ImportError as e:
    print(f"Error importing config files: {e}")
    print("Make sure config_landlord.py and tenant_config.py are in the same directory")
    sys.exit(1)

# Import Templates
try:
    from lease-blank import *
    from house-rules.py import *
except ImportError as e:
    print(f"Error importing config files: {e}")
    print("Make sure house-rules.py and lease-blank.py are in the same directory")
    sys.exit(1)


# Auto-calculate termination date and period words
def calculate_lease_details():
    start_date = datetime.strptime(commencement_date, "%d %B %Y")
    end_date = start_date + relativedelta(months=lease_months)

    # Auto-set period words
    period_words_map = {1: "one", 6: "six", 12: "twelve"}
    global lease_period_words
    lease_period_words = period_words_map.get(lease_months, f"{lease_months}")

    # Format termination date
    global termination_date
    termination_date = end_date.strftime("%d %B %Y")

    print(f"✅ Lease calculated: {commencement_date} → {termination_date} ({lease_months} months)")


# Generate complete lease
def generate_complete_lease():
    calculate_lease_details()

    # Main lease F-string (your updated version from previous message)
    lease_agreement_md = f"""[YOUR FULL LEASE F-STRING HERE - paste the complete one]"""

    # Appendix A&B F-string (your version from previous message)
    appendix_a_b_md = f"""[YOUR APPENDIX A&B F-STRING HERE - paste the complete one]"""

    complete_lease = lease_agreement_md + "\n\n" + appendix_a_b_md

    # Filename with tenant name and dates
    filename = f"{lessee_name.replace(' ', '_')}_Lease_{commencement_date.replace(' ', '_').replace(',', '')}.md"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(complete_lease)

    print(f"✅ Lease generated: {filename}")
    print(f"   Tenant: {lessee_name}")
    print(f"   Period: {commencement_date} to {termination_date}")
    print(f"   Rental: R{rental_amount}/month")


if __name__ == "__main__":
    generate_complete_lease()