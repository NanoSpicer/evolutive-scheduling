"""
Our basic error class
"""

#
# Constants
#

# Code_errors

ERR_LOADER_JSON_NOT_FOUND = 11
ERR_LOADER_INCOHERENT_INPUT_SET = 12
ERR_GENOTYPE_UNDER_SIZED = 21
ERR_POPULATION_NOT_STABLISHED = 31

def _get_err_dict() -> dict:
    err_dict = {
        ERR_LOADER_JSON_NOT_FOUND: "JSON file not found",
        ERR_LOADER_INCOHERENT_INPUT_SET: "The inputs set has incoherent info. See additional info.",
        ERR_GENOTYPE_UNDER_SIZED: "Genotype needs more free slots. Please review professor or center availability.",
        ERR_POPULATION_NOT_STABLISHED: "Population not stablished, due to prior errors. Please see error above."
    }
    return err_dict

def _get_err_msg(code: int) -> str:

    return _get_err_dict()[code]


class OurError:
    def __init__(self):
        self.err_code = 0
        self.err_msg = None
        self.err_add_info = None
        pass

    def has_error(self) -> bool:

        return self.err_code != 0

    def set_error(self, code: int, add_info: str = None):
        self.err_code = code
        if code != 0:
            self.err_msg = _get_err_msg(code)
            self.err_add_info = add_info
        else:
            self.err_msg = None
            self.err_add_info = None
        pass

    def print(self):
        if type(self.err_msg) == str:
            print(f"Error {self.err_code}: {self.err_msg}")
        if type(self.err_add_info) == str:
            print(f"Additional info: {self.err_add_info}")
        pass
