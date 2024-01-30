from flask import Flask, render_template, request, send_file, flash, redirect, url_for
import sqlite3, openai, nltk, pandas as pd, PyPDF2, fitz, re
from nltk.tokenize.treebank import TreebankWordDetokenizer

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"

categories = ["companies", "general", "specifics", "people", "summary"]
records = []
category = ""
main_document = ""
document = ""
expression = ""
sum_expression = ""
contexts = []
final_contexts = []
summarys = []
summary = ""


class summary:
    """In the first version of the system this class was used to generate the summary of the text selected by the user"""

    def count_tokens(prompt):
        """Counts the number of tokens in the text selected by the user

        Args:
            prompt (string): text selected by the user

        Returns:
            int: returns the number of tokens the text has
        """
        tokens = nltk.word_tokenize(prompt, language="portuguese")
        return len(tokens)

    def generate_response(prompt):
        """Requests to ChatGPT to summary the text selected by the user

        Args:
            prompt (string): text selected by the user

        Returns:
            string: returns the summary of the selected text
        """
        prompt_request = "Resumo em português o texto seguinte: " + prompt

        messages = [{"role": "system", "content": "Isto é resumir o texto."}]
        messages.append({"role": "user", "content": prompt_request})
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.5,
                max_tokens=500,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
            )

            return response["choices"][0]["message"]["content"]
        except openai.error.Timeout as e:
            # if ChatGPT times out
            print(f"OpenAI API request timed out: {e}")
            flash("O ChatGPT não está a funcionar de momento.")


@app.before_first_request
def before_start():
    drop_table()
    create_table()
    insert_data()


def get_results(filename):
    """Gets the results of a category for the selected document

    Args:
        filename (string): document's file path

    Returns:
        string []: list with all the results for a category
    """
    data = []
    with open(filename, "r", encoding="utf-8") as f:
        if "summary" in filename:
            data.append(f.read())
        else:
            for line in f:
                data.append(line.rstrip("\n"))
    return data


def get_count_results(filename):
    """Gets the amount of times each result of a category is mentioned in the selected document

    Args:
        filename (string): document file path

    Returns:
        int []: list with the amount of times each result of a category is mentioned
    """
    results = []
    df = pd.read_fwf(filename, encoding="utf-8")
    results = df["Count"].values.tolist()
    return results


def sqlite_connect():
    """Connection to the database"""
    try:
        conn = sqlite3.connect("saacdb.db")
    except sqlite3.Error:
        print("Error connecting to the database saacdb.db")
    finally:
        return conn


def create_table():
    """Creates the tables for each category and for the summary"""
    connection = sqlite_connect()
    cursor = connection.cursor()

    for i in range(len(categories)):
        if categories[i] == "summary":
            sql_create_table_query = f"""
            CREATE TABLE {categories[i]} (name TEXT NOT NULL);
            """
            cursor.execute(sql_create_table_query)
        else:
            sql_create_table_query = f"""
            CREATE TABLE {categories[i]} (name TEXT NOT NULL, count INTEGER);
            """
            cursor.execute(sql_create_table_query)

    connection.commit()
    connection.close()


def drop_table():
    """Drops every table previous created in the system"""
    connection = sqlite_connect()
    cursor = connection.cursor()
    for i in range(len(categories)):
        sql_drop_table_query = f"""
        DROP TABLE IF EXISTS {categories[i]};
        """
        cursor.execute(sql_drop_table_query)
    cursor.execute(sql_drop_table_query)
    connection.commit()
    connection.close()


def insert_data():
    """Inserts the results into the tables on the database"""
    try:
        connection = sqlite_connect()
        print("Connected to the database saacdb.db")
        cursor = connection.cursor()

        for i in range(len(categories)):
            if categories[i] == "summary":
                sqlite_insert_query = f"""
                INSERT INTO {categories[i]} (name) VALUES (?)
                """
                results = get_results(
                    f"./api/static/results_13/final_{categories[i]}.txt"
                )
                if "13" in main_document:
                    results = get_results(
                        f"./api/static/results_13/final_{categories[i]}.txt"
                    )
                if "636" in main_document:
                    results = get_results(
                        f"./api/static/results_636/final_{categories[i]}.txt"
                    )
                if "_en" in main_document:
                    results = get_results(
                        f"./api/static/results_en/final_{categories[i]}.txt"
                    )

                for i in range(len(results)):
                    cursor.execute(sqlite_insert_query, (results[i],))
            else:
                sqlite_insert_query = f"""
                INSERT INTO {categories[i]} (name, count) VALUES (?, ?)
                """
                results = get_results(f"./api/static/results_13/{categories[i]}.txt")
                count_results = get_count_results(
                    f"./api/static/results_13/nltk/matches_{categories[i]}.txt"
                )
                if "13" in main_document:
                    results = get_results(
                        f"./api/static/results_13/{categories[i]}.txt"
                    )
                    count_results = get_count_results(
                        f"./api/static/results_13/nltk/matches_{categories[i]}.txt"
                    )
                if "636" in main_document:
                    results = get_results(
                        f"./api/static/results_636/{categories[i]}.txt"
                    )
                    count_results = get_count_results(
                        f"./api/static/results_636/nltk/matches_{categories[i]}.txt"
                    )
                if "_en" in main_document:
                    results = get_results(
                        f"./api/static/results_en/{categories[i]}.txt"
                    )
                    count_results = get_count_results(
                        f"./api/static/results_en/nltk/matches_{categories[i]}.txt"
                    )

                for i in range(len(results)):
                    cursor.execute(
                        sqlite_insert_query,
                        (
                            results[i],
                            count_results[i],
                        ),
                    )

        connection.commit()
        print("Inserted successfully")
        cursor.close()
    except sqlite3.Error as error:
        print("Failed insert into the table.", error)
    finally:
        if connection:
            connection.close()
            print("Connection closed")


def get_records(category):
    """Gets the results from a category's table in the database

    Args:
        category (string): selected category
    """
    try:
        connection = sqlite_connect()
        print("Connected to the database saacdb.db")

        cursor = connection.cursor()

        sql_fetch_query = f"""
        SELECT * from {category}
        """

        cursor.execute(sql_fetch_query)
        result = cursor.fetchall()
        records.clear()
        for row in result:
            if category == "summary":
                records.append([row[0]])
            else:
                records.append([row[0], row[1]])
        records.sort()
        connection.commit()
        print("Retrieve successfully")
        cursor.close()
    except sqlite3.Error as error:
        print("Failed retrieving from the table", error)
    finally:
        if connection:
            connection.close()
            print("Connection closed")


def write_file(text):
    """Writes a file to be downloaded with the user notes

    Args:
        text (string): user notes

    Returns:
        string: user notes file path
    """
    with open("./api/notes.txt", "w", encoding="utf-8") as f:
        f.write(text)
    f.close
    file = "./notes.txt"
    return file


def update_document(expression):
    """Generates a new document to be displayed when the user selects one of the results

    Args:
        expression (string): result selected by the user

    Returns:
        string: new document file path
    """
    original_exp = expression
    if "13" in main_document:
        reader = PyPDF2.PdfReader("./api/static/document_13.pdf")
    if "636" in main_document:
        reader = PyPDF2.PdfReader("./api/static/document_636.pdf")
    if "_en" in main_document:
        reader = PyPDF2.PdfReader("./api/static/document_en.pdf")
    writer = PyPDF2.PdfWriter()

    for p in range(len(reader.pages)):
        text = reader.pages[p].extract_text()
        text = text.lower()
        text = text.replace("\n", " ")
        text = text.replace(" ", "")
        text = text.replace("-", "")
        expression = expression.replace(" ", "")
        expression = expression.replace("-", "")
        if expression in text:
            writer.add_page(reader.pages[p])

    with open("./api/static/document_tmp.pdf", "wb") as pdf:
        writer.write(pdf)

    doc = fitz.open("./api/static/document_tmp.pdf")
    for page in doc:
        text_instances = page.search_for(original_exp)
        for inst in text_instances:
            highlight = page.add_highlight_annot(inst)
            highlight.update()

    doc.saveIncr()
    file = "./static/document_tmp.pdf"
    return file


def get_contexts(expression):
    """Gets the local summaries of the result selected by the user

    Args:
        expression (string): result selected by the user
    """
    chunks = []
    global summarys
    summarys = []

    doc = ""
    if "13" in main_document:
        doc = "./api/static/results_13/summary_chunks.txt"
    if "636" in main_document:
        doc = "./api/static/results_636/summary_chunks.txt"
    if "_en" in main_document:
        doc = "./api/static/results_en/summary_chunks.txt"

    with open(doc, "r", encoding="utf-8") as f:
        tmp_chunk = []
        for line in f:
            if "Resumo: " in line:
                text = " ".join(tmp_chunk)
                chunks.append(text)
                tmp_chunk.clear()
                summarys.append(line.split("Resumo: ")[1])
            else:
                tmp_chunk.append(line)

    tmp_expression = expression
    global contexts
    contexts = []

    for i in range(len(chunks)):
        tmp_chunk = chunks[i].lower()
        chunks[i] = chunks[i].lower()
        chunks[i] = chunks[i].replace("\n", " ")
        chunks[i] = chunks[i].replace(" ", "")
        chunks[i] = chunks[i].replace("-", "")
        expression = expression.replace(" ", "")
        expression = expression.replace("-", "")
        if expression in chunks[i]:
            chunk_tokens = nltk.word_tokenize(tmp_chunk, language="portuguese")
            ngrams = list(nltk.collocations.ngrams(chunk_tokens, 50))
            for k in range(len(ngrams)):
                untokenize_txt = TreebankWordDetokenizer().detokenize(ngrams[k])
                untokenize_txt = re.sub(r'\s+([?.!"…])', r"\1", untokenize_txt)
                tmp_gram = untokenize_txt
                untokenize_txt = untokenize_txt.lower()
                untokenize_txt = untokenize_txt.replace("\n", " ")
                untokenize_txt = untokenize_txt.replace(" ", "")
                untokenize_txt = untokenize_txt.replace("-", "")
                if expression in untokenize_txt:
                    if k == 0:
                        contexts.append((tmp_gram, i))
                    if k == len(ngrams) - 1:
                        contexts.append((tmp_gram, i))

                    if len(tmp_expression.split(" ")) > 1:
                        if (
                            tmp_expression.split(" ")[0]
                            == ngrams[k][int(len(ngrams[k]) / 2 - 1)]
                            and tmp_expression.split(" ")[1]
                            == ngrams[k][int(len(ngrams[k]) / 2)]
                        ):
                            contexts.append((tmp_gram, i))
                    else:
                        if (
                            tmp_expression.split(" ")[0]
                            == ngrams[k][int(len(ngrams[k]) / 2 - 1)]
                        ):
                            contexts.append((tmp_gram, i))


@app.route("/", methods=["POST", "GET"])
def home():
    """Resets the variables when the user lands on the Home Page"""
    global records
    records = []
    global category
    category = ""
    global main_document
    main_document = ""
    global document
    document = ""
    global expression
    expression = ""
    global contexts
    contexts = []
    global final_contexts
    final_contexts = []
    global sum_expression
    sum_expression = ""
    global summary
    summary = ""
    global summarys
    summarys = []
    if request.method == "POST":
        if "docselector" in request.form:
            name_document = request.form["docselector"]
            return redirect(url_for("index", name=name_document))

    return render_template("home.html")


@app.route("/<name>", methods=["POST", "GET"])
def index(name):
    """Makes the connection with the interface functionalities

    Args:
        name (string): document's name
    """
    global main_document
    global document
    if not main_document:
        if "13" in name:
            main_document = "./static/document_13.pdf"
        if "636" in name:
            main_document = "./static/document_636.pdf"
        if "bruen" in name:
            main_document = "./static/document_en.pdf"

        document = main_document
        before_start()
    if request.method == "POST":
        global category
        global expression
        global contexts
        global summarys
        global sum_expression
        global summary
        global final_contexts

        # change selected category
        if "optradio" in request.form:
            category = request.form["optradio"]
            get_records(request.form["optradio"])

        # download user notes
        if "notepad" in request.form:
            text = request.form["notepad"]
            f = write_file(text)
            return send_file(f, as_attachment=True)

        # update the document being displayed
        if "updatedoc" in request.form:
            expression = request.form["updatedoc"]
            f = update_document(expression)
            document = f

        # display the original document
        if "resetdoc" in request.form:
            document = main_document
            expression = ""

        # get the local summaries of an expression
        if "getcontexts" in request.form:
            sum_expression = request.form["getcontexts"]
            get_contexts(sum_expression)
            final_contexts = [c[0] for c in contexts]

        # get the selected local summary
        if "getsummarys" in request.form:
            i = request.form["getsummarys"]
            summary_index = contexts[int(i)][1]
            summary = summarys[int(summary_index)]

        # reset the selected local summary
        if "closesummary" in request.form:
            summary = ""

    return render_template(
        "index.html",
        main=name,
        results=records,
        category=category,
        doc=document,
        exp=expression,
        ctxts=final_contexts,
        sum_exp=sum_expression,
        sum=summary,
    )


if __name__ == "__main__":
    app.run(debug=True)
