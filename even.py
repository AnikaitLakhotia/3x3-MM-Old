def create_even(a, b, c, d):
    """
        Create even clauses for SAT encoding.

        Args:
            a (int): First variable index.
            b (int): Second variable index.
            c (int): Third variable index.
            d (int): Fourth variable index.

        Returns:
            list: List of lists containing even clauses.
        """

    return [[a, b, c, -d], [a, b, -c, d], [a, -b, c, d], [-a, b, c, d],
            [a, -b, -c, -d], [-a, b, -c, -d], [-a, -b, c, -d], [-a, -b, -c, d]]
