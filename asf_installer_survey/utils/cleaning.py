from re import escape, finditer
from typing import Optional, Sequence, Union
from warnings import warn
from pandas import DataFrame
from pyarrow.parquet.core import filters_to_expression


def _clean_other_responses(
    items: Sequence, responses: Sequence, other_text: str, other_replace: str
) -> Sequence:
    """Remove free-text other responses from responses and renames Other category.

    Args:
      items: A list of responses (categories) for an individual record.
      responses: A list of valid responses for the question.
      other_text: The other category.
      other_replace: The new other category name.

    Returns:
      Cleaned list of responses without free-text 'Other' responses.
    """
    new_items = []
    for item in items:
        if item in responses:
            new_items.append(item)
        elif item == other_text:
            new_items.append(other_replace)
        else:
            # Don't add free text answers to new items.
            pass
    return new_items


def _extract_other_text(
    items: Sequence, responses: Sequence, other_text: str
) -> Sequence:
    """Capture free-text other responses from responses.

    Args:
      items: A list of responses (categories) for an individual record.
      responses: A list of valid responses for the question.
      other_text: The other category.

    Returns:
      Cleaned list of responses without free-text 'Other' responses.
    """
    new_items = []
    for item in items:
        if item in responses:
            pass
        elif item == other_text:
            pass
        else:
            # Add free text answers to new items.
            new_items.append(item)
    return new_items[0] if len(new_items) == 1 else None


def _collapse_list(items: Sequence) -> Sequence:
    """Create new list of categories removing nulls.

    Assumes categories are strings and missing are non-string (e.g. float NaNs).

    Args:
      items: A list of responses (categories) for an individual record, including NaNs.

    Returns:
      Cleaned list of responses without missing NaN values.
    """
    return [item for item in items.to_list() if isinstance(item, str)]


def collapse_select_all(
    df: DataFrame,
    select_all_columns: str,
    collapsed_column_name: str,
    remove_collapsed_columns: bool = False,
    responses: Optional[Sequence] = None,
    recode_other: bool = False,
    save_other_as_new_column: bool = False,
    new_other_column_name: Optional[str] = None,
    other_text: str = "Other (please specify)",
    other_replace: str = "Other",
):
    # Collapse fields to list of items.
    df[collapsed_column_name] = df[
        df.columns[df.columns.str.contains(select_all_columns)]
    ].apply(_collapse_list, axis=1)

    if save_other_as_new_column:
        # Check for column name and create if not provided
        if not new_other_column_name:
            warn(
                f"new_other_column_name not provided, using {collapsed_column_name}: Other"
            )
            new_other_column_name = collapsed_column_name + ": Other"

        # Store free text in new field.
        df.loc[
            lambda df: (
                df[collapsed_column_name].apply(
                    lambda xs: any(["Other" in x for x in xs])
                )
            ),
            new_other_column_name,
        ] = df.loc[
            lambda df: (
                df[collapsed_column_name].apply(
                    lambda xs: any(["Other" in x for x in xs])
                )
            ),
            collapsed_column_name,
        ].apply(
            _extract_other_text, args=(responses, other_text)
        )

    if recode_other:
        # Recode the other column
        df.loc[
            lambda df: (
                df[collapsed_column_name].apply(
                    lambda xs: any(["Other" in x for x in xs])
                )
            ),
            collapsed_column_name,
        ] = df.loc[
            lambda df: (
                df[collapsed_column_name].apply(
                    lambda xs: any(["Other" in x for x in xs])
                )
            ),
            collapsed_column_name,
        ].apply(
            _clean_other_responses, args=(responses, other_text, other_replace)
        )

    if remove_collapsed_columns:
        columns = df.columns[df.columns.str.contains(select_all_columns)].tolist()
        # Remove response and optional other column in case they are included
        try:
            columns.remove(collapsed_column_name)
        except ValueError:
            # value errors are thrown when the item to remove doesn't exist in the list.
            # we can ignore these as it means we're not drop the column we created.
            pass
        if save_other_as_new_column:
            try:
                columns.remove(new_other_column_name)
            except ValueError:
                # value errors are thrown when the item to remove doesn't exist in the list.
                # we can ignore these as it means we're not drop the column we created.
                pass
        df = df.drop(columns=columns)

    return df


def _insert_into_string(source_str, insert_str, pos):
    return source_str[:pos] + insert_str + source_str[pos:]


def set_not_asked_responses(
    df: DataFrame,
    column: str,
    filters: Sequence,
    exclusion_cols: Sequence,
    not_asked_value: Union[str, int, Sequence],
) -> DataFrame:
    # Convert filters to expression
    expression = "lambda df: " + str(filters_to_expression(filters))
    # add in pandas components
    for exclusion_col in exclusion_cols:
        # Get indices for exclusion_col in expression
        indices = [
            (m.start(0), m.end(0)) for m in finditer(escape(exclusion_col), expression)
        ]
        index_offset = 0
        # Insert pandas bits into string at
        for start, end in indices:
            expression = _insert_into_string(expression, 'df["', start + index_offset)
            index_offset += 4
            expression = _insert_into_string(expression, '"]', end + index_offset)
            index_offset += 2

    # fix boolean 'or'
    or_locs = [(m.start(0), m.end(0)) for m in finditer("\) or \(", expression)]
    or_offset = 0
    for start, end in or_locs:
        expression = (
            expression[: start + 2 + or_offset]
            + "|"
            + expression[end + or_offset - 2 :]
        )
        or_offset -= 1

    # fix boolean 'and'
    and_locs = [(m.start(0), m.end(0)) for m in finditer("\) and \(", expression)]
    and_offset = 0
    for start, end in and_locs:
        expression = (
            expression[: start + and_offset + 2]
            + "&"
            + expression[end + and_offset - 2 :]
        )
        and_offset -= 2

    # Update not asked responses (nb had to do this to allow setting with an iterable)
    if isinstance(not_asked_value, str) | isinstance(not_asked_value, int):
        df.loc[eval(expression), column] = not_asked_value
    else:
        df.loc[eval(expression), column] = df.loc[eval(expression), column].apply(
            lambda _: not_asked_value
        )

    return df


def merge_two_questions(
    df: DataFrame,
    merge_column_1: str,
    merge_column_2: str,
    merge_column_name: str,
    remove_merge_columns: bool = False,
) -> DataFrame:
    def _merge(row):
        """Get's non-nan (float) value. Returns error if both non-nan."""
        if row[0] and isinstance(row[1], float):
            return row[0]
        elif isinstance(row[0], float) and row[1]:
            return row[1]
        elif isinstance(row[0], float) and isinstance(row[1], float):
            return row[0]
        else:
            raise ValueError("At least 1 row has 2 non null values.")

    df[merge_column_name] = df[[merge_column_1, merge_column_2]].apply(_merge, axis=1)

    if remove_merge_columns:
        columns = [merge_column_1, merge_column_2]
        # Remove response and optional other column in case they are included
        try:
            columns.remove(merge_column_name)
        except ValueError:
            pass
        df = df.drop(columns=columns)
    return df
