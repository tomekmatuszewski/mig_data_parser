from datetime import date, datetime

import pandas as pd

orders = pd.read_csv("orders.csv", sep=";")
orders = orders.drop(orders.index[0]).replace(to_replace="#N/D", value="Not_allocated")

# set date to datetime.now() if you want to select orders after current date

current_date = date(2020, 5, 20)


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
            date_format="dd/mm/YYYY", engine="xlsxwriter"
        ) as writer:
            group[1].to_excel(writer, index=False, sheet_name="orders")

if __name__ == "__main__":
    parsed_orders = parse_data(orders)
    create_xlsx_files(parsed_orders)
