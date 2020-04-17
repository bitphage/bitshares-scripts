bitshares-scripts
=================

This is a small scripts collection for doing various stuff in Bitshares

* `balances_as_btc.py` - Summarize all assets on all accounts and show BTC value
* `cancel_all_orders.py` - Cancel all orders on the specified account
* `create_account.py` - Create new account with random password and providing all keys to stdout
* `get_account.py` - Display account object
* `get_worker.py` - Display worker object
* `get_asset.py` - Display asset object
* `get_balance.py` - Display account balances
* `get_balance_multi.py` - Display summarized balance of multiple accounts
* `get_feeds.py` - Show price feeds for specified asset
* `get_keys.py` - Generate private and public keys from account name and password
* `get_op_id.py` - Display operation id numbers and corresponding name
* `get_witness.py` - Display witness object
* `update_keys.py` - Change account keys using generated random password and providing all keys to stdout

**Note:** some scripts are sending transactions, you need to add private active keys for your accounts via `uptick addkey`

Installation via poetry
-----------------------

1. Make sure you have installed required packages: `apt-get install gcc make libssl-dev`
2. Install [poetry](https://python-poetry.org/docs/)
3. Run `poetry install` to install the dependencies
4. Copy `common.yml.example` to `common.yml` and change variables according to your needs
5. Now you're ready to run scripts:


```
poetry shell
./script.py
```

Reusable parts
--------------

Reusable parts are being moved slowly into `bitsharesscripts` package namespace. It can be installed via `pip install bitsharesscripts`.
