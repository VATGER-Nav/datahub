def frequency_validator(frequency_str: str) -> str:
    """
    frequency: The frequency value to validate, in MHz.
    """
    frequency = float(frequency_str)

    # Check if the value is in VHF band
    if not (118 <= frequency < 138):
        raise ValueError("Frequency must be between 118 MHz and 138 MHz.")

    formatted_frequency = f"{frequency:.3f}"

    # Convert the formatted string back to a float for further calculations
    frequency = float(formatted_frequency)

    # check if the frequency is a valid 8.33 frequency
    # we are checking in kHz to counter floating-point precision errors
    # (e.g. 0.015 % 0.005 returning 0.00499 instead of 0)
    fractional_part_khz = round(frequency - int(frequency), 3) * 1e3

    if fractional_part_khz % 5 != 0 or fractional_part_khz in {20, 70}:
        raise ValueError("Frequency must be using 8.33kHz spacing")

    # Return the frequency as a string with exactly 3 decimal places
    return formatted_frequency
