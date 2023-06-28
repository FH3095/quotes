
import textwrap, MySQLdb, secrets

def _formatQuote(config, quote):
    result = textwrap.wrap(quote, width = config["QUOTE_WORDWRAP_LENGTH"], expand_tabs = False, replace_whitespace = False, drop_whitespace = True,
                           break_long_words = False, break_on_hyphens = False)
    result = "\n".join(result)
    return result

def getQuote(config):
    db = MySQLdb.connect(host = config["DB_HOST"], user = config["DB_USER"], password = config["DB_PASS"], database = config["DB_NAME"])
    try:
        db.autocommit(False)
        selectedRow = None
        quote = None
        with db.cursor() as c:
            c.execute("SELECT count(id) FROM quote WHERE blocked = 0")
            numRows = c.fetchone()[0]
            if numRows < 1:
                raise RuntimeError("Quotes-Table is empty")
            selectedRow = secrets.randbelow(min(numRows, config["QUOTE_RND_OF_LOWEST"]))
            c.execute("SELECT id, text FROM quote WHERE blocked = 0 ORDER BY last_used ASC, id ASC LIMIT 1 OFFSET " + str(selectedRow))
            quoteRow = c.fetchone()
            c.execute("UPDATE quote SET last_used = NOW() WHERE id = " + str(quoteRow[0]))
            quote = quoteRow[1]
        if not config["TEST_MODE"]:
            db.commit()
        else:
            db.rollback()
        return _formatQuote(config, quote).strip()
    finally:
        db.close()
