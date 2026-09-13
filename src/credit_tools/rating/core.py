from collections.abc import Sequence


def assign_rating(
    borrower_ids: Sequence[str],
    ml_scores: Sequence[float],
    defaulted: Sequence[bool],
    rating_scale: dict[str, float],
) -> dict[str, str]:
    if not (len(borrower_ids) == len(ml_scores) == len(defaulted)):
        raise ValueError("borrower_ids, ml_scores, and defaulted must have the same length")
    if not rating_scale:
        raise ValueError("rating_scale must not be empty")

    order = sorted(range(len(ml_scores)), key=lambda i: ml_scores[i])
    sorted_scores = [ml_scores[i] for i in order]
    sorted_targets = [float(defaulted[i]) for i in order]

    calibrated_pd = _isotonic_regression(sorted_scores, sorted_targets)
    ratings_by_edr = sorted(rating_scale.items(), key=lambda item: item[1])

    assigned: dict[str, str] = {}
    for i, pd in zip(order, calibrated_pd):
        rating, _ = min(ratings_by_edr, key=lambda item: abs(item[1] - pd))
        assigned[borrower_ids[i]] = rating
    return assigned


def _isotonic_regression(sorted_scores: Sequence[float], sorted_targets: Sequence[float]) -> list[float]:
    """Pool-adjacent-violators fit of an increasing curve through (score, target)."""
    unique_scores: list[float] = []
    group_sums: list[float] = []
    group_weights: list[float] = []
    for score, target in zip(sorted_scores, sorted_targets):
        if unique_scores and unique_scores[-1] == score:
            group_sums[-1] += target
            group_weights[-1] += 1
        else:
            unique_scores.append(score)
            group_sums.append(target)
            group_weights.append(1)

    values = [s / w for s, w in zip(group_sums, group_weights)]
    weights = list(group_weights)
    sizes = [1] * len(values)

    i = 0
    while i < len(values) - 1:
        if values[i] <= values[i + 1]:
            i += 1
            continue
        merged_weight = weights[i] + weights[i + 1]
        merged_value = (values[i] * weights[i] + values[i + 1] * weights[i + 1]) / merged_weight
        values[i : i + 2] = [merged_value]
        weights[i : i + 2] = [merged_weight]
        sizes[i : i + 2] = [sizes[i] + sizes[i + 1]]
        i = max(i - 1, 0)

    fitted_by_group: list[float] = []
    for value, size in zip(values, sizes):
        fitted_by_group.extend([value] * size)

    fitted_by_score = dict(zip(unique_scores, fitted_by_group))
    return [fitted_by_score[score] for score in sorted_scores]
