"""Central colour palette for all EDNpopdyn figures.

    from edn_popdyn import colors
    ax.plot(x, y, color=colors.valid)
    ax.plot(x, y, color=colors.invalid)

"""

# ===========================================================================
# Core cue-validity colours  (your original colors.py)
# ===========================================================================
valid = "#157b7b"          # valid cue
invalid = "#953730"        # invalid cue
no_cue = "#b07ba2"         # no-cue (NC)
cue = "#704d6b"            # generic "cue present"

# Cue / target identities
cue_a = "#f15b2a"
cue_b = "#046938"
target_a = "#f89521"
target_b = "#6aa84f"

# Alternative invalid shades used in some panels 
invalid_accent = "#B1361E"     
invalid_fallback = "#b5651d"   

# ===========================================================================
# Effect-direction colours 
#   delta_neg : valid < invalid (significant)
#   delta_pos : valid > invalid (significant)
#   delta_ns  : not significant
# ===========================================================================
delta_neg = "#576b30"
delta_pos = "#94644e"
delta_ns = "#4d4d4e"

delta_pos_fallback = "#2c7fb8"
delta_neg_fallback = "#d95f0e"
delta_ns_fallback = "#9e9e9e"

# ===========================================================================
# Population-geometry panels
# ===========================================================================
null_fraction = "#6daa9f"      # null-space fraction bars
potent_fraction = "#c05d5d"    # potent-space fraction bars
src_valid = "#1F425E"          # SRC_COLS[0]
src_invalid = "#2E6A2C"        # SRC_COLS[1]
nc_gray = "#888888"            # COL_NC in 3.1

# ===========================================================================
# Behaviour / expectation panels
# ===========================================================================
err_dark = "#2f4f4f"           # darkslategray  (error band, dark)
err_light = "#7da9a9"          # error band, light
correct = "#3a6b6b"            # correct trials (task-potent axis)
incorrect = "#8fb6b3"          # incorrect trials
correct_dark = "#5e6e5c"       # "4B" correct shade

# Likelihood-ratio colouring  (r<1, r≈1, r>1)
ratio_low = "#6A1B9A"
ratio_mid = "#E0A33E"
ratio_high = "#C42E7A"

# ===========================================================================
# Decoding strength ramp
# ===========================================================================
strength = ["#08519c", "#6baed6", "#fc9272", "#cb181d"]

# ===========================================================================
# Psychometric 
# ===========================================================================
cue_cr = cue_a            # CR cue (orange) — note: distinct from cue_a
cue_cl = cue_b           # CL cue
cue_nc = no_cue            # NC (psychometric panels)
prior = "#8a6f2d"              # prior (brown/gold)
gray_mid = "#666666"
neutral = "#555555"

# ===========================================================================
# Convenience groupings
# ===========================================================================

cue_colors = {"NC": cue_nc, "CL": cue_cl, "CR": cue_cr}

# Effect-direction
delta = {"neg": delta_neg, "pos": delta_pos, "ns": delta_ns}

# Full palette 
PALETTE = {
    "valid": valid, "invalid": invalid, "no_cue": no_cue, "cue": cue,
    "cue_a": cue_a, "cue_b": cue_b, "target_a": target_a, "target_b": target_b,
    "invalid_accent": invalid_accent, "invalid_fallback": invalid_fallback,
    "delta_neg": delta_neg, "delta_pos": delta_pos, "delta_ns": delta_ns,
    "null_fraction": null_fraction, "potent_fraction": potent_fraction,
    "src_valid": src_valid, "src_invalid": src_invalid, "nc_gray": nc_gray,
    "err_dark": err_dark, "err_light": err_light, "correct": correct,
    "incorrect": incorrect, "correct_dark": correct_dark,
    "ratio_low": ratio_low, "ratio_mid": ratio_mid, "ratio_high": ratio_high,
    "cue_cr": cue_cr, "prior": prior, "gray_mid": gray_mid, "neutral": neutral,
}

