# ========================================
# TENANT CONFIGURATION
# ========================================

# Primary Tenant Details
lessee_name = "Chad Van Rensburg"
lessee_id = "9404020237082"
lessee_email = "chad@example.com"
lessee_phone = "+27 83 965 6885"

# Domicilium (Legal Address for Notices)
lessee_domicilium_physical = "4 Arendblom, Middleton, Caledon, South Africa, 7230"
lessee_domicilium_email = lessee_email  # Usually same as lessee_email

# Payment Responsible Person (can be same as tenant or guarantor)
person_responsible_name = "Danielle Scheepers"
person_responsible_id = "9404020237082"  # Same as lessee_id or different
person_responsible_email = lessee_email
person_responsible_phone = lessee_phone

# Lease Dates (Tenant-specific)
commencement_date = "1 December 2023"
termination_date = "31 May 2024"  # Auto-calculate based on lease_months