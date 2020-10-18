import re


class ReplaceDict:
    """Replaces a series of keys to values."""

    def __init__(self, rep_dict: dict):
        """

        :param rep_dict: A dict, in which all keys and values must be str.
        """
        self.rep_dict = rep_dict
        self.pattern = re.compile(
            '|'.join(map(re.escape, self.rep_dict.keys())), re.M)

    def replace(self, string: str) -> str:
        """Replaces the given str according to the pattern."""
        return self.pattern.sub(lambda key: self.rep_dict[key.group()], string)
