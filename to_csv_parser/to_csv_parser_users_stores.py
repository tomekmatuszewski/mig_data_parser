import numpy as np
import pandas as pd

# path to xlsx file
path = "permissions.xlsx"

users = pd.read_excel(path, sheet_name="Users")
stores = pd.read_excel(path, sheet_name="Stores")
users.rename(columns={"Unnamed: 0": "user_id"}, inplace=True)
stores.rename(columns={"Unnamed: 0": "store_id"}, inplace=True)
users.set_index("user_id", inplace=True)
stores.set_index("store_id", inplace=True)

empty_dict = {"user_id": [], "store_id": [], "flag": []}


def create_new_table(new_dict: dict, users: pd.DataFrame, stores: pd.DataFrame) -> dict:
    for user in users.index:
        temp_user = users[users.index == user].dropna(axis=1)
        if "Region" in temp_user.columns:
            temp_user["Region"] = temp_user["Region"].astype(np.int64)
        for store in stores.index:
            temp_store = stores[stores.index == store].filter(items=temp_user.columns)
            new_dict["user_id"].append(user)
            new_dict["store_id"].append(store)
            if temp_user.loc[user].equals(temp_store.loc[store]):
                new_dict["flag"].append(True)
            else:
                new_dict["flag"].append(False)
    return new_dict


def df_to_csv(df: pd.DataFrame) -> None:
    df.to_csv("results_users/permissions_user.csv", sep=",", header=False, index=False)


if __name__ == "__main__":
    dict_result = create_new_table(empty_dict, users, stores)
    final_df = pd.DataFrame(dict_result)
    df_to_csv(final_df)
