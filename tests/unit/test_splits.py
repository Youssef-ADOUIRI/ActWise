from actwise.evaluation.splits import make_splits, split_of

ARTICLES = [f"AIA-Art{n}" for n in range(1, 101)] + [f"GDPR-Rec{n}" for n in range(1, 21)]


def test_splits_partition_the_articles():
    """Every article lands in exactly one split."""
    splits = make_splits(ARTICLES)
    parts = [set(splits[name]) for name in ("train", "dev", "test")]

    assert set().union(*parts) == set(ARTICLES)
    assert sum(len(p) for p in parts) == len(ARTICLES)


def test_split_sizes_are_70_15_15():
    """120 articles split 84 / 18 / 18."""
    splits = make_splits(ARTICLES)

    assert [len(splits[name]) for name in ("train", "dev", "test")] == [84, 18, 18]


def test_splits_depend_only_on_the_seed():
    """The input order does not change the splits; the seed does."""
    assert make_splits(ARTICLES) == make_splits(reversed(ARTICLES))
    assert make_splits(ARTICLES, seed=1) != make_splits(ARTICLES, seed=2)


def test_split_of_maps_each_article_to_its_split():
    """`split_of()` inverts the splits: article id -> split name."""
    splits = {"train": ["AIA-Art1"], "dev": ["AIA-Art2"], "test": ["GDPR-Art9"]}

    assert split_of(splits) == {"AIA-Art1": "train", "AIA-Art2": "dev", "GDPR-Art9": "test"}
