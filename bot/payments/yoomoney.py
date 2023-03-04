import random
import string

from yoomoney import Authorize, Client, Quickpay

def get_token(client_id: str, redirect_uri: str):
    Authorize(
        client_id=client_id,
        redirect_uri=redirect_uri,
        scope=["account-info",
                "operation-history",
                "operation-details",
                "incoming-transfers",
                "payment-p2p",
                "payment-shop",
                ]
        )

async def create_invoice(yoomoney_account_number: str | int, amount: int) -> str:
    letters_and_digits = string.ascii_lowercase + string.digits
    label = ''.join(random.sample(letters_and_digits, 10))
    quickpay = Quickpay(
            receiver=yoomoney_account_number,
            quickpay_form="shop",
            targets="Replenishment of the balance",
            paymentType="SB",
            sum=amount,
            label=label
            )
    return quickpay.redirected_url, label

async def check_invoice(label: str, yoomoney_token: str):
    client = Client(yoomoney_token)
    history = client.operation_history(label=label)
    try:
        return history.operations[0].status
    except IndexError:
        return False
