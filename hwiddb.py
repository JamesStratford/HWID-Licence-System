import sqlite3 as sl

class Database():
    """
    SQLite database setup for validating user HWIDs.
    If a user exists in the database, return a key to unlock
    software application via the web API.
    """
    __con = sl.connect('database.db', check_same_thread=False)

    def __init__(self):
        # Users table for users who will have access to the files.
        if not self.check_existing("USER"):
            self.__con.execute(
                """
                CREATE TABLE USER (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                hwid TEXT NOT NULL UNIQUE,
                date TEXT,
                date_end TEXT
                );
                """)

        # Requests table for handling users not in the database trying to
        # access the files.
        if not self.check_existing("REQUESTS"):
            self.__con.execute(
                """
                CREATE TABLE REQUESTS (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                hwid TEXT NOT NULL UNIQUE,
                date TEXT
                );
                """)
            self.__con.commit()

    def get_connection(self):
        return self.__con
    
    def check_existing(self, table) -> bool:
        """
        Checks database for existing table\n
        Parameters:\n
            table -> table name\n
        Returns: 
            True if table exists; False if not
        """
        result = self.__con.execute(
            """
            SELECT count(*) FROM sqlite_master 
            WHERE type='table' AND name=(?);
            """, (table,)
        )
        return result.fetchone()[0] == 1

    def delete_row(self, id, table):
        """
        Remove row from table.\n
        Parameters:\n
            id -> Users id\n
            table -> Database table\n
        """
        self.__con.execute(
            """
            DELETE FROM {}
            WHERE id = ?;
            """.format(table), (id,)
        )
        self.__con.commit()
    
    def put(self, name, hwid, table="USER"):
        """
        Puts new user's information into database and
        setting end-date.
        on subscription to 1 month from now\n
        Parameters:\n
            name -> Users name,\n
            hwid -> unique computer ID\n
        """
        if not self.check_hwid_exists(hwid, table):
            if (table == "USER"):
                self.__con.execute(
                    """
                    INSERT INTO {} (name, hwid, date, date_end)
                    VALUES 
                    (?, ?, date(), (date('now','+1 month')))
                    """.format(table), (name, hwid)
                )
            elif (table == "REQUESTS"):
                self.__con.execute(
                    """
                    INSERT INTO {} (name, hwid, date)
                    VALUES 
                    (?, ?, date())
                    """.format(table), (name, hwid)
                )
        else:
            self.__con.execute(
                """
                UPDATE {} 
                SET name = ?,
                hwid = ?
                WHERE hwid = ?;
                """.format(table), (name, hwid, hwid)
            )
        self.__con.commit()
        
    
    def check_hwid_exists(self, hwid, table="USER") -> bool:
        """
        Checks user's hwid against database\n
        Parameters:\n
            hwid -> unique computer ID\n
        Returns:\n
            True if HWID is in database; False if not
        """
        result = self.__con.execute(
            """
            SELECT count(*) FROM {}
            WHERE hwid = ?
            """.format(table), (hwid,)
        )
        return result.fetchone()[0] > 0
   
    def approve_access(self, id):
        """
        Approves access from REQUESTS and moves to USERS.\n
        Parameters:
            id -> REQUESTS table id to move to USER.\n
        """
        user = self.__con.execute(
            """
            SELECT name, hwid FROM REQUESTS
            WHERE id = ?
            """, (id,)
        ).fetchone()
        self.put(user[0], user[1])
        self.delete_row(id, "REQUESTS")
        self.__con.commit()
    
    def check_subscription_valid(self, hwid) -> bool:
        """
        Checks user's subscription end date against 
        today's date\n
        Parameters:\n
            hwid -> unique computer ID\n
        Returns:\n
            True if valid subscription; False if invalid
        """
        result = self.__con.execute(
            """
            SELECT julianday('now') - julianday(date_end) FROM USER
            WHERE hwid = ?
            """, (hwid,)
        )
        # check how many days are remaining for subscription
        if result.fetchone()[0] < 0.0:
            return True
        return False

    def set_subscription_end_date(self, name, date_end):
        """
        Updates users subscription end date.\n
        Parameters:\n
            name -> Users name in database,\n
            date_end -> new end date ("YYYY-MM-DD").\n
        """
        self.__con.execute(
            """
            UPDATE USER 
            SET date_end = ?
            WHERE name = ?;
            """, (date_end, name)
        )
        self.__con.commit()
        

    def print_table(self, table="USER"):
        column_names = self.__con.execute(
            """
            SELECT name FROM 
            pragma_table_info('{}')
            ORDER BY cid;
            """.format(table)
        )
        result = self.__con.execute(
            """
            SELECT * FROM {}
            """.format(table))
        for col in column_names.fetchall():
            print(col, end='')
        print()
        for row in result.fetchall():
            print(row)

    def close(self):
        self.__con.close()