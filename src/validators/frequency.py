def frequency_validator(frequency: float) -> float:
    """
    frequency (float): The frequency value to validate, in MHz.
    """

    # enforce consistent formatting with 3 digits
    frequency = round(frequency, 3)

    # Check if the value is in VHF band
    if not (118 <= frequency < 138):
        raise ValueError(
            "The value must be greater or equal to 118MHz and smaller than 138 MHz."
        )

    # check if the frequency is a valid 8.33 frequency
    # we are checking in kHz to counter floating-point precision errors
    # (e.g. 0.015 % 0.005 returning 0.00499 instead of 0)
    fractional_part_khz = round(frequency - int(frequency), 3) * 1e3

    if fractional_part_khz % 5 != 0 or fractional_part_khz in {20, 70}:
        raise ValueError("Frequency must be using 8.33kHz spacing")

    return frequency
