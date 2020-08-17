from typing import Final
from decimal import Decimal

from hypothesis import settings, strategies as st

PROFILE_NO_INCREMENTAL: Final[str] = "no-incremental"

# Use no incremental mode due to multiple issues with hypothesis
# shrinking mechanism which eventually leads to random tests hanging
settings.register_profile(PROFILE_NO_INCREMENTAL, database=None)
settings.load_profile(PROFILE_NO_INCREMENTAL)

# Do not generate NaN value in Decimal since it does not support
# comparison and raises InvalidOperation exception upon comparison
st.register_type_strategy(Decimal, st.decimals(allow_nan=False))
