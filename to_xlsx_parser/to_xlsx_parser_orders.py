from datetime import date, datetime

import pandas as pd

from to_xlsx_parser.utlis.utils_functions import style_table

# path to csv file with orders
path = "orders.csv"

# set date to datetime.now() if you want to select orders after current date
current_date = date(2020, 5, 20)

orders = pd.read_csv(path, sep=";")
orders = orders.drop(orders.index[0]).replace(to_replace="#N/D", value="Not_allocated")


def parse_data(orders: pd.DataFrame) -> pd.DataFrame:
    for column in orders.columns.tolist():
        new_col = column.strip()
        orders.rename(columns={column: new_col}, inplace=True)
        orders[new_col] = orders[new_col].apply(lambda element: element.strip())
        if new_col == "Units":
            orders[new_col] = orders[new_col].apply(
                lambda unit: unit.split(".")[0] if unit.split(".")[0] != "" else "0"
            )
        elif new_col == "Order Date":
            orders[new_col] = pd.to_datetime(orders[new_col], errors="coerce").dt.date
    orders_filtered = orders[
        (orders["Order Date"] > pd.to_datetime(current_date))
        & (orders["order type code"] == "ZT")
    ]
    return orders_filtered


def create_xlsx_files(orders: pd.DataFrame) -> None:
    for group in orders.groupby(by=["Brand Code"]):
        with pd.ExcelWriter(
            f"results_orders/{group[0]}_{datetime.now().strftime('%d%m%Y')}.xlsx",
            date_format="dd/mm/YYYY",
            engine="xlsxwriter",
        ) as writer:
            group[1].to_excel(
                writer, index=False, sheet_name="orders", header=False, startrow=1
            )

            style_table(writer, group)


if __name__ == "__main__":
    parsed_orders = parse_data(orders)
    create_xlsx_files(parsed_orders)
