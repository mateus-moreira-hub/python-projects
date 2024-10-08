from dataclasses import dataclass
import datetime as dt
from enum import Enum
import json
from types import SimpleNamespace

CONFIG_FILEPATH = "configs/reconcile_accounts.json"

class MatchingStatus(Enum):
    FOUND = "FOUND"
    MISSING = "MISSING"

class AccountsReadingConfig:
    columns_order: list[str]
    date_format: str

class AccountsMatchingConfig:
    float_decimal_places: int
    is_case_sensitive: bool
    plus_or_minus_days_tolerance: int
    
class ReconcileAccountsConfig:
    accounts_reading_config: AccountsReadingConfig
    accounts_matching_config: AccountsMatchingConfig

@dataclass
class Account:
    date: dt.date = dt.date(1, 1, 1)
    department: str = ""
    value: float = 0.0
    beneficiary: str = ""
    matching_status: MatchingStatus = MatchingStatus.MISSING
    order: int = 0

    # cria o objeto partindo de uma lista e da config de leitura
    def from_list(
        self, 
        data: list, 
        config: AccountsReadingConfig, 
        order: int
    ) -> "Account":
        self.date = dt.datetime.strptime(
            data[config.columns_order.index("date")], 
            config.date_format
        ).date()
        self.department = data[config.columns_order.index("department")]
        self.value = float(data[config.columns_order.index("value")])
        self.beneficiary = data[config.columns_order.index("beneficiary")]
        self.order = order
        return self

    # retorna o objeto como uma lista
    def to_list(self) -> list:
        return [
            str(self.date), 
            self.department, 
            str(self.value), 
            self.beneficiary, 
            self.matching_status.value
        ]
    
    # recebe um outro objeto Account e retorna um booleano 
    # indicando a correspondência entre ambos
    def match(
        self, 
        account: "Account", 
        matching_config: AccountsMatchingConfig
    ) -> bool:
        return (
            self.date <= account.date + \
                dt.timedelta(days=matching_config.plus_or_minus_days_tolerance) and
            self.date >= account.date + \
                dt.timedelta(days=(-1)+matching_config.plus_or_minus_days_tolerance) and
            round(self.value, matching_config.float_decimal_places) == \
                round(account.value, matching_config.float_decimal_places) and (
                (
                    matching_config.is_case_sensitive and
                    self.department == account.department and
                    self.beneficiary == account.beneficiary
                ) or (
                    not matching_config.is_case_sensitive and
                    self.department.lower() == account.department.lower() and
                    self.beneficiary.lower() == account.beneficiary.lower()
                )
            )
        )

def read_config() -> ReconcileAccountsConfig:
    with open(CONFIG_FILEPATH) as f:
        return json.load(f, object_hook=lambda d: SimpleNamespace(**d))
    
def data_to_accounts(data: list, config: AccountsReadingConfig) -> list[Account]:
    return sorted(
        [Account().from_list(acc, config, i) for i, acc in enumerate(data)],
        key=lambda x: x.date
    )

def accounts_to_data(accounts: list[Account]) -> list:
    return [acc.to_list() for acc in sorted(accounts, key=lambda x: x.order)]

def reconcile_accounts(transactions1: list, transactions2: list) -> tuple[list, list]:

    # lê a configuração da função
    config = read_config()

    # cria duas listas de objetos Account
    accounts1, accounts2 = (
        data_to_accounts(transactions1, config.accounts_reading_config),
        data_to_accounts(transactions2, config.accounts_reading_config)
    )

    # itera sobre as listas e, caso haja correspondência, 
    # separa o objeto da segunda lista numa lista separada,
    # para que não se tenha que iterar sobre ele novamente
    matched_accounts2 = []
    for acc1 in accounts1:
        for i, acc2 in enumerate(accounts2):
            if acc1.match(acc2, config.accounts_matching_config):
                acc1.matching_status = MatchingStatus.FOUND
                acc2.matching_status = MatchingStatus.FOUND
                matched_accounts2.append(accounts2.pop(i))
                break

    # retorna as listas ao formato original e na ordem 
    # original, agora com o status de correspondência
    accounts1, accounts2 = (
        accounts_to_data(accounts1),
        accounts_to_data(accounts2 + matched_accounts2)
    )
    return accounts1, accounts2