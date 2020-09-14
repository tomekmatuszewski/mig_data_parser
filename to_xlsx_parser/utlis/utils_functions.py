import pandas as pd


def style_table(writer: pd.ExcelWriter, df: pd.DataFrame) -> None:
    """Function to style xlsx file"""
    workbook = writer.book
    worksheet = writer.sheets["orders"]

    header_format = workbook.add_format(
        {"bold": False, "text_wrap": True, "border": False}
    )

    for col_num, value in enumerate(df[1].columns.values):
        worksheet.write(0, col_num, value, header_format)
        worksheet.set_column(
            col_num, col_num, len(df[1].columns.to_list()[col_num]) * 1.1
        )
    worksheet.set_column("A:A", 8)
