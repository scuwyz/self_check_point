import logging
from flask import Flask, request, send_file
from check import login, parse
import arrow
import requests

app = Flask(__name__)
app.config["DOWNLOAD_FOLDER"] = "download"

logging.basicConfig(filename="scuwyz.log", level=logging.INFO)


@app.route("/", methods=["GET", "POST"])
def index():
    real_ip = request.headers.getlist("X-Forwarded-For")
    log = f"{request.url} / {arrow.now().format('YYYYMMDD-HH:mm:ss')} {str(real_ip)}"
    logging.info(log)
    if request.method == 'POST':
        stuid = request.form['stuid']
        passwd = request.form['passwd']
        log += stuid
        # print("{} {}".format(stuid, passwd))
        if len(stuid) == 13 and stuid[:4] == '2015' and len(passwd) < 20:
            try:
                session = requests.Session()
                status, session = login(session, stuid, passwd)
                if status == "success":
                    log = "-> log in success ->"
                    out_file_name = "download/{}-{}.xls".format(stuid,
                                                                arrow.now("Asia/Shanghai").format("YYYYMMDD-HHmmss"))
                    status, out_file_name = parse(session, stuid, out_file_name)
                    if not status:
                        logging.error("教务处欠费或者出现其他问题")
                        return "教务处欠费 :(  或者出现其他问题"
                    log += out_file_name
                    logging.info(log)
                    return send_file(out_file_name, as_attachment=True)

                else:
                    logging.error(status)
                    return status

            except IOError:
                # print("error")
                error = "系统提了一个问题，QAQ 请稍等片刻重试   如果情况持续，请戳 Les1ie"
                logging.error(error)
                return error

    log = " return index.html "

    log += f"{request.user_agent.string}"
    logging.info(log)
    # log += real_ip

    with open('index.html', encoding='utf8') as f:
        con = f.read()
    return con


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=80)
