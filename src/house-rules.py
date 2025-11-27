# F-string for Appendix A & B Markdown
appendix_a_b_md = f"""
# Appendices A & B: Facilities, Services and House Rules

## Appendix A: Included Facilities and Services

### Facilities

The house comprises:

- {num_bedrooms} fully furnished bedrooms with a bed, mattress, bedside table, Fan, cupboard, desk and chair;
- Fully equipped kitchen with all the basics, including fridge, dishwasher, oven, microwave, toaster, kettle, cutlery, pots and pans as well as other basic cooking utensils.
- Fully furnished sitting room with sofa, 1 armchair, 1 bean bag, coffee table, dining room table with {dining_chairs} chairs and carpet
- The bathroom has a shower and a bath.
- The kitchen has a washing machine and a clothes line outside as well as a clothes rack for indoor drying.

An inventory list will be placed in the bedrooms and will be confirmed with tenants at the start of the lease.

### Services

The house has {wifi_type}.

The tenants are responsible for putting the rubbish out for the municipal waste removal.

The property is cleaned on {cleaning_day} {cleaning_frequency}. The cleaning staff will clean all communal areas and rooms only on special request. Please be courteous and don't leave the kitchen in a mess. Tenants are responsible for their own washing up. The staff will only tidy and clear everything away. Tenants are responsible for keeping the house clean on every other day.

The house has an electricity meter. The electricity is prepaid and is the responsibility of the tenants and is additional to the rental.

The house has three gas bottles, one for the Geyser and the other for the oven and stove the third is spare to keep the gas on while plans are made to refill. It is the responsibility of the tenants to split the costs of refilling the bottles.

### Security

{security_company} is a small local firm and pride themselves in offering a personalised, efficient service. The house has an alarm and if the alarm goes off {security_company} will be at the property within 5-10 minutes. There are cameras to the front and rear of the property. Tenants will be listed as key holders and will be expected to respond to calls from the security call-centre to ensure safety. Should Tenants feel unsafe getting out of their vehicles into the premises, {security_company} do offer a meet and greet service where they will meet you at the premises to ensure your safety. This service is subject to availability of their response units.

### Insurance

All tenants are requested to take out their own personal insurance. The property insurance covers the items owned by the lessor. It is highly recommended that tenants also have private medical cover.

### Maintenance

Any maintenance issues that need to be attended to can be communicated with the property manager via a google form that will be sent out to all the tenants on arrival.

Please ensure that you do not overload the washing machine. If a faulty machine is reported and the contractor finds that the problem has been caused by overloading/abuse of the machine the cost of the callout and repair will be deducted from the deposits received from all the tenants.

### Keys

If any tenant loses their keys it will be their responsibility to make a copy from the master set that is kept by the property manager. The master set must be returned within 24 hours.

### Heating

Cape Town has a fairly mild climate but if tenants wish to heat their bedrooms please purchase blow heaters. Electric bar heaters and gas heaters are not permitted as they pose a potential fire risk.

### Water

As stated in the lease, Cape Town is experiencing a chronic water shortage. Tenants must comply with the city's water restrictions or will be liable for any additional charges.

### Support

We offer a hands-on approach when working with our tenants. If at any time, anyone has a concern, question or problem that the property manager cannot help you with we are only a phone call away and will do our best to answer any questions and rectify any problems as quickly as possible.

Please feel free to contact us at any time: {property_manager_name} ({property_manager_phone}); {helping_contact_name} ({helping_contact_phone})

---

## Appendix B: House Rules

### Noise

We ask that because there are other residential properties in the area, the noise be kept under control. If you are going to be socialising, please make sure that everyone is inside from {noise_weekday_cutoff} onwards during the week and {noise_weekend_cutoff} on the weekends. This is out of respect for others in the area. Loud music is not permitted.

### Hygiene

It can be difficult sharing accommodation. It needs a high level of respect in terms of acceptable behaviour and in particular hygiene. Please ensure that you leave the communal areas how you find them and keep your kitchens and bathrooms clean at all times. Washing up must be done immediately after cooking so that the pots and shared kitchen equipment are clean and ready for other housemates to use.

### Visitors

If any tenant would like a visitor to stay with them in their room they must clear it with their housemates first. Casual visitors can stay a maximum of {visitor_max_nights} nights.

Please note that each tenant is responsible for their visitor's conduct. In the event that a tenant does not feel comfortable with a visitor's behaviour, they are free to contact the property manager who will ask the visitor to leave. Our ethos is to create a relaxing and comfortable space for all tenants and we do not want this environment to be compromised.

### Room Entry

Rooms are private and may not be entered without notifying the tenant. In the case of maintenance requested inside a room, the tenant must make arrangements that they or a friend will be present when a contractor comes to attend to the problem. If this is not possible the lessor is not liable for any loss. Should a contractor arrive and is unable to gain access, the tenant will be charged for the callout.

Towards the end of the year the Lessor may wish to show the room to prospective tenants for the following year. Tenants will be given notice in advance and will be asked to ensure that their room is clean and tidy. The tenant does not reserve the right to refuse entry when advance warning of the visit has been given.

### Smoking

The entire property is a no smoking zone. Please leave the premises if you wish to smoke.

### Unlawful Substances

No unlawful substances are allowed on the premises. Any infringement of this rule may result in the tenant being asked to leave.

### Alcohol Abuse

Abuse of alcohol negatively affects housemates and can put the individual at risk. Please be courteous to your housemates and neighbours at all times and ensure that you do not create a disturbance.

**If tenants do not adhere to the house rules they will be given {warnings_before_eviction} written warnings and on the third transgression will be asked to leave.**

---

**I have read the above details of the facilities and services provided and I agree to the house rules:**

**Signed at:** __________________________ **Date:** _________________________

**Lessee:** ______________________________ **Witness:** ______________________

**Lessee's Full Name (PLEASE PRINT CLEARLY):** {lessee_name}

**Lessor's Full Name:** {lessor_name}
"""