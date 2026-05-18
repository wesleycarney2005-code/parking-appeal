"""Generate parking fine appeal letters from user inputs."""
from datetime import datetime

FINE_TYPES = {
    "council_pcn":    "Penalty Charge Notice (Council)",
    "private_parking": "Private Parking Charge Notice",
    "bus_lane":       "Bus Lane Penalty Charge Notice",
    "cctv_parking":   "CCTV Parking Penalty Charge Notice",
    "moving_traffic": "Moving Traffic Contravention",
}

GROUNDS = {
    "no_sign":       "The signage was inadequate, unclear or missing",
    "paid_correctly": "I had paid the correct charge and complied with all conditions",
    "medical":       "I was attending to a medical emergency",
    "loading":       "I was loading or unloading goods",
    "broken_meter":  "The pay and display machine was faulty or out of order",
    "incorrect_pcn": "The Penalty Charge Notice contains errors",
    "not_driver":    "I was not the driver of the vehicle at the time",
    "already_paid":  "The charge has already been paid",
    "mitigating":    "There were exceptional mitigating circumstances",
    "no_bay":        "There were no available spaces in the designated bays",
}

_COUNCIL_ADDRESS = {
    "council_pcn": "The Parking Adjudications Service",
    "bus_lane": "The Parking Adjudications Service",
    "cctv_parking": "The Parking Adjudications Service",
    "moving_traffic": "The Traffic Penalty Tribunal",
    "private_parking": "POPLA (Parking on Private Land Appeals)",
}

_GROUNDS_PARAGRAPHS = {
    "no_sign": """On the date in question, I carefully inspected the area for any signage indicating the parking restrictions in force. The signage was either absent, obscured, or so inadequate that a reasonable motorist exercising due care could not reasonably have been expected to understand the restrictions that applied. Under the relevant regulations, clear and conspicuous signage is a mandatory requirement. Where signage fails to meet this standard, any resulting Penalty Charge Notice is unlawfully issued and must be cancelled.

I would draw your attention to the Traffic Signs Regulations and General Directions 2016, which prescribe the minimum standards for parking restriction signage. In this case, those standards were not met.""",

    "paid_correctly": """I had paid the correct parking charge in full and complied with all conditions applicable to the parking location on the date in question. I am therefore at a complete loss to understand why a Penalty Charge Notice has been issued.

I respectfully submit that the evidence upon which this Notice has been issued is incorrect. I attach [evidence of payment — please insert: a photograph of the pay-and-display ticket, a bank transaction, or a receipt]. I trust that upon reviewing this evidence you will agree that this Notice has been issued in error and should be cancelled forthwith.""",

    "medical": """On the date and time in question, I was attending to a genuine and urgent medical emergency that required my immediate attention. The circumstances were entirely beyond my control and left me with no reasonable alternative but to leave my vehicle where it was.

[Please insert a brief description of the emergency here, e.g.: "A family member suffered a sudden health episode requiring immediate assistance."]

I am sure you will appreciate that in such exceptional circumstances, the strict application of parking regulations would produce a wholly disproportionate and unjust result. I respectfully request that you exercise the discretion afforded to you and cancel this Notice on compassionate grounds.""",

    "loading": """At the time the Notice was issued, I was actively loading and unloading goods at the location in question. Loading and unloading operations are generally exempt from many parking restrictions, and the operation I was undertaking was genuine, necessary, and completed with all reasonable speed.

The relevant legislation and Department for Transport guidance make clear that a vehicle that is continuously loading or unloading is not in contravention of waiting restrictions. I was present with my vehicle for the purposes of this lawful activity and should not have been issued a Penalty Charge Notice.""",

    "broken_meter": """On the date in question, I attempted to pay the appropriate parking charge but was unable to do so because the pay-and-display machine at the location was not functioning correctly. [Please specify: e.g., "The machine displayed an 'Out of Order' message / refused to accept coins / would not issue a ticket."]

Where a payment facility is faulty and a motorist is thereby unable to comply, it would be wholly unreasonable and disproportionate to issue a Penalty Charge Notice. I made every reasonable effort to comply with the conditions. I respectfully request that you cancel this Notice on this basis.""",

    "incorrect_pcn": """Upon examining the Penalty Charge Notice issued to me, I have identified material errors in the information it contains. Specifically: [Please specify the error, e.g., "The vehicle registration number recorded is incorrect / the date is wrong / the location code does not correspond to the alleged contravention location."]

A Penalty Charge Notice that contains material errors is invalid and unenforceable. I therefore invite you to cancel this Notice immediately and confirm in writing that no further action will be taken.""",

    "not_driver": """I write to inform you that I was not the driver of the vehicle at the time the alleged contravention took place. As the registered keeper, I am making this representation on my own behalf.

Under the statutory provisions applicable to this Notice, liability may only be transferred to the driver if the keeper is able to provide the driver's details. I [am/am not] in a position to provide the driver's name and address. [If able to provide: "I hereby provide the driver's details as follows: [name and address]. I respectfully request that you reissue the Notice to that individual." / If unable: "I respectfully submit that in these circumstances it would be inappropriate to pursue me as keeper."]""",

    "already_paid": """I can confirm that this Penalty Charge Notice has already been paid in full. I enclose evidence of payment [please attach proof of payment]. The continued pursuit of this matter is therefore incorrect and I respectfully request that you update your records accordingly and confirm that no further action will be taken.""",

    "mitigating": """I wish to draw your attention to exceptional mitigating circumstances that existed at the time of the alleged contravention. [Please describe your specific circumstances in detail here, e.g.: "I was required to remain with my vehicle due to a vehicle breakdown / I was assisting a vulnerable individual who required immediate help."]

I trust that upon consideration of the full circumstances of this case, you will agree that the strict enforcement of this Notice would lead to a disproportionate and unjust outcome. I respectfully ask that you exercise your discretion and cancel this Notice.""",

    "no_bay": """At the time I parked my vehicle, all designated parking spaces in the area were occupied and no lawful alternative was available to me. I had a legitimate reason to be in the area and parked in the nearest available location while making every reasonable effort to avoid causing obstruction or inconvenience.

It would be wholly unreasonable to penalise a motorist for a situation entirely outside their control. I respectfully request that you cancel this Notice.""",
}


def generate_letter(data: dict) -> str:
    """Generate a complete appeal letter from form data."""
    fine_type   = data.get("fine_type", "council_pcn")
    ground      = data.get("ground", "no_sign")
    pcn_ref     = data.get("pcn_ref", "[PCN REFERENCE]").upper().strip()
    vehicle_reg = data.get("vehicle_reg", "[VEHICLE REGISTRATION]").upper().strip()
    fine_date   = data.get("fine_date", "[DATE OF FINE]")
    location    = data.get("location", "[LOCATION]").strip()
    your_name   = data.get("your_name", "[YOUR NAME]").strip()
    your_addr   = data.get("your_address", "[YOUR ADDRESS]").strip().replace("\n", "\n")
    issuer_name = data.get("issuer_name", "[ISSUING AUTHORITY]").strip()
    extra_info  = data.get("extra_info", "").strip()

    today = datetime.today().strftime("%d %B %Y").lstrip("0")
    fine_type_label  = FINE_TYPES.get(fine_type, "Penalty Charge Notice")
    body_para        = _GROUNDS_PARAGRAPHS.get(ground, _GROUNDS_PARAGRAPHS["mitigating"])
    adjudicator      = _COUNCIL_ADDRESS.get(fine_type, "The Parking Adjudications Service")
    formal_ground    = GROUNDS.get(ground, "Mitigating circumstances")

    extra_section = ""
    if extra_info:
        extra_section = f"\nBy way of further context, I wish to add the following:\n\n{extra_info}\n"

    letter = f"""{your_name}
{your_addr}

{today}

Appeals Department
{issuer_name}

---

Dear Sir or Madam,

RE: FORMAL APPEAL — {fine_type_label}
PCN Reference: {pcn_ref}
Vehicle Registration: {vehicle_reg}
Date of Alleged Contravention: {fine_date}
Location: {location}

I write to formally appeal against the above-referenced {fine_type_label} issued in respect of the above vehicle.

GROUNDS OF APPEAL: {formal_ground.upper()}

{body_para}
{extra_section}
CONCLUSION

For the reasons set out above, I respectfully submit that this {fine_type_label} was issued unlawfully / in error / in circumstances that do not justify enforcement, and I request that it be cancelled in full without delay.

I expect a written response to this appeal within 56 days. Should you reject this appeal, I request full written reasons and information regarding my right to an independent adjudication before {adjudicator}.

Please note that I am keeping a full record of all correspondence relating to this matter.

Yours faithfully,

{your_name}

---
Note: This letter has been prepared using a professional template. Where indicated in [brackets], please insert your specific details before sending.
"""
    return letter
