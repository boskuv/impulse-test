# impulse-test

### Description
'impulse-test' allows to get list of campaigns from [direct.yandex.ru](https://direct.yandex.ru/) by API (v5).
Allowed data manipulation:    
:white_check_mark: insert(table_name: str, column_values: Dict);    
:white_check_mark: fetchall(table_name: str, columns: List = None), 'None' is for fetching all the columns from the table.    

### Instruction
1. Add your token to env and name it "token" (perhaps you will need to reboot your machine).
2. Run the project by next command: "python main.py".
